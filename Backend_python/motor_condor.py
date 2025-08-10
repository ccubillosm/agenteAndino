import pandas as pd
import numpy as np
import pandas_ta as ta
import os

# Cargar config desde la raíz del proyecto
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)
import config

ARCHIVO_DE_ENTRADA = config.ARCHIVO_ACCIONES_MASTER
ARCHIVO_DE_SALIDA = config.ARCHIVO_TECNICO

def limpiar_y_estandarizar(df):
    print("-> Estandarizando y limpiando datos...")
    df.columns = df.columns.str.lower()
    if 'date' not in df.columns and 'fecha' in df.columns:
        df.rename(columns={'fecha': 'date'}, inplace=True)
    try:
        if 'date' not in df.columns:
             raise ValueError(f"La columna 'date' o 'fecha' no se encontró. Columnas disponibles: {df.columns.tolist()}")
        df['date'] = pd.to_datetime(df['date'], dayfirst=True).dt.normalize()
        print("   - Columna 'date' procesada y normalizada correctamente.")
    except Exception as e:
        print(f"!! ERROR al procesar la columna de fecha: {e}")
        return None
    if 'adj close' in df.columns:
        df = df.drop(columns=['adj close'])
    numeric_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in numeric_cols:
        if str(df[col].dtype) == 'object':
            df[col] = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=numeric_cols, inplace=True)
    if 'nemotecnico' in df.columns:
         df.rename(columns={'nemotecnico': 'ticker'}, inplace=True)
    print("-> Limpieza completada.")
    return df

def calcular_indicadores_y_senales(df):
    print("-> Calculando el set completo de indicadores y señales...")
    def process_group(group):
        group = group.sort_values(by='date')
        group.ta.ema(length=9, append=True); group.ta.ema(length=12, append=True); group.ta.ema(length=26, append=True)
        group.ta.sma(length=5, append=True); group.ta.sma(length=20, append=True); group.ta.sma(length=50, append=True); group.ta.sma(length=200, append=True)
        group.ta.rsi(length=14, append=True)
        group.ta.macd(fast=12, slow=26, signal=9, append=True)
        group.ta.bbands(length=20, std=2, append=True)
        group.ta.stoch(k=14, d=3, append=True)
        group.ta.cci(length=20, append=True)
        group.ta.adx(length=14, append=True)
        group.ta.psar(append=True)
        group.ta.atr(length=14, append=True)
        group.ta.obv(append=True)
        group.ta.ad(append=True)
        group.ta.ichimoku(append=True)
        group.rename(columns=lambda x: x.lower(), inplace=True)
        return group
    df_final = df.groupby('ticker').apply(process_group).reset_index(level=0, drop=True)
    print("-> Cálculo de indicadores y señales completado.")
    return df_final

def main():
    print("--- INICIANDO MOTOR CÓNDOR v4.2 (Procesador Maestro) ---")
    if not os.path.exists(ARCHIVO_DE_ENTRADA):
        print(f"!! ERROR: El archivo de entrada '{ARCHIVO_DE_ENTRADA}' no se encontró.")
        return
    try:
        df_input = pd.read_csv(ARCHIVO_DE_ENTRADA, delimiter=';')
        df_limpio = limpiar_y_estandarizar(df_input)
        if df_limpio is not None:
            df_final = calcular_indicadores_y_senales(df_limpio)
            print(f"Guardando resultados en '{ARCHIVO_DE_SALIDA}'...")
            df_final.to_csv(ARCHIVO_DE_SALIDA, index=False, decimal=',', sep=';')
            print(f"\n--- ¡PROCESO COMPLETADO CON ÉXITO! ---")
    except Exception as e:
        print(f"\n!! Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()