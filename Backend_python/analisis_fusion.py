import pandas as pd
import os

# Cargar config desde la raíz del proyecto
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)
import config

ARCHIVO_TECNICO = config.ARCHIVO_TECNICO
ARCHIVO_FUNDAMENTAL = config.CSV_FUNDAMENTAL
ARCHIVO_SALIDA_FUSION = config.ARCHIVO_OPORTUNIDADES

def detectar_divergencias(df_tecnico, df_fundamental):
    print("-> Fusionando bases de datos...")
    
    # Convertir fechas y extraer año
    df_tecnico['year'] = pd.to_datetime(df_tecnico['date']).dt.year
    
    # Filtrar solo registros con RSI válido
    df_tecnico = df_tecnico[df_tecnico['rsi_14'].notna() & (df_tecnico['rsi_14'] != '')]
    print(f"   - Registros con RSI válido: {len(df_tecnico)}")
    
    # Hacer merge con datos fundamentales
    df_fusionado = pd.merge(df_tecnico, df_fundamental, on=['ticker', 'year'], how='left')
    print(f"   - Registros después del merge: {len(df_fusionado)}")
    
    # Rellenar datos fundamentales hacia adelante para cada ticker
    columnas_a_rellenar = df_fundamental.columns.drop(['ticker', 'year'])
    df_fusionado[columnas_a_rellenar] = df_fusionado.groupby('ticker')[columnas_a_rellenar].ffill()
    
    # Filtrar solo registros con datos fundamentales
    df_fusionado = df_fusionado.dropna(subset=['salud_financiera'])
    print(f"   - Registros con datos fundamentales: {len(df_fusionado)}")
    
    print("-> Buscando oportunidades de divergencia...")
    
    # Buscar oportunidades con criterios más flexibles
    oportunidades = []
    
    # 1. RSI < 30 (sobreventa) + Salud financiera Alta
    cond1 = (df_fusionado['rsi_14'] < 30) & (df_fusionado['salud_financiera'] == 'Alta')
    oportunidades_cond1 = df_fusionado[cond1]
    if not oportunidades_cond1.empty:
        oportunidades.append(("RSI < 30 + Salud Alta", oportunidades_cond1))
    
    # 2. RSI < 35 (casi sobreventa) + Salud financiera Alta
    cond2 = (df_fusionado['rsi_14'] < 35) & (df_fusionado['salud_financiera'] == 'Alta')
    oportunidades_cond2 = df_fusionado[cond2 & ~cond1]  # Excluir los ya capturados
    if not oportunidades_cond2.empty:
        oportunidades.append(("RSI < 35 + Salud Alta", oportunidades_cond2))
    
    # 3. RSI < 30 + Salud financiera Estable
    cond3 = (df_fusionado['rsi_14'] < 30) & (df_fusionado['salud_financiera'] == 'Estable')
    oportunidades_cond3 = df_fusionado[cond3]
    if not oportunidades_cond3.empty:
        oportunidades.append(("RSI < 30 + Salud Estable", oportunidades_cond3))
    
    return oportunidades

def main():
    df_tecnico = pd.read_csv(ARCHIVO_TECNICO, sep=';', decimal=',')
    df_fundamental = pd.read_csv(ARCHIVO_FUNDAMENTAL, sep=';', decimal=',')
    oportunidades = detectar_divergencias(df_tecnico, df_fundamental)
    
    if oportunidades:
        print("\nSe encontraron las siguientes OPORTUNIDADES DE DIVERGENCIA:")
        for nombre_oportunidad, df_oportunidad in oportunidades:
            print(f"\n{nombre_oportunidad}:")
            cols = ['date', 'ticker', 'close', 'rsi_14', 'salud_financiera', 'roe']
            print(df_oportunidad[cols].to_string(index=False))
            df_oportunidad[cols].to_csv(ARCHIVO_SALIDA_FUSION, index=False, sep=';', decimal=',')
            print(f"\n-> Oportunidades guardadas en '{ARCHIVO_SALIDA_FUSION}'")
    else:
        print("\nNo se encontraron divergencias.")

if __name__ == "__main__":
    main()