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
    df_tecnico['year'] = pd.to_datetime(df_tecnico['date']).dt.year
    df_fusionado = pd.merge(df_tecnico, df_fundamental, on=['ticker', 'year'], how='left')
    
    columnas_a_rellenar = df_fundamental.columns.drop(['ticker', 'year'])
    df_fusionado[columnas_a_rellenar] = df_fusionado.groupby('ticker')[columnas_a_rellenar].ffill()
    df_fusionado.dropna(subset=['salud_financiera'], inplace=True)
    
    print("-> Buscando oportunidades de divergencia...")
    cond_tecnica = df_fusionado['rsi_14'] < 30
    cond_fundamental = df_fusionado['salud_financiera'] == 'Alta'
    return df_fusionado[cond_tecnica & cond_fundamental]

def main():
    df_tecnico = pd.read_csv(ARCHIVO_TECNICO, sep=';', decimal=',')
    df_fundamental = pd.read_csv(ARCHIVO_FUNDAMENTAL, sep=';', decimal=',')
    oportunidades = detectar_divergencias(df_tecnico, df_fundamental)
    
    if oportunidades.empty:
        print("\nNo se encontraron divergencias.")
    else:
        print("\nSe encontraron las siguientes OPORTUNIDADES DE DIVERGENCIA:")
        cols = ['date', 'ticker', 'close', 'rsi_14', 'salud_financiera', 'roe']
        print(oportunidades[cols].to_string(index=False))
        oportunidades[cols].to_csv(ARCHIVO_SALIDA_FUSION, index=False, sep=';', decimal=',')
        print(f"\n-> Oportunidades guardadas en '{ARCHIVO_SALIDA_FUSION}'")

if __name__ == "__main__":
    main()