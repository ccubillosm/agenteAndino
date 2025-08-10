import yfinance as yf
import pandas as pd
from datetime import datetime
import time
import os

# Cargar config desde la raíz del proyecto
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)
import config

ACTIVOS_MACRO = {
    'CHILE_ETF': 'ECH', 'SP500': '^GSPC', 'NASDAQ': '^IXIC', 'RUSSELL2000': '^RUT',
    'VIX': '^VIX', 'DAX_ALEMANIA': '^GDAXI', 'IBEX35_ESP': '^IBEX', 
    'SHANGHAI_CHINA': '000001.SS', 'NIKKEI_JAPON': '^N225', 'BOVESPA_BRASIL': '^BVSP',
    'COBRE': 'HG=F', 'PETROLEO_WTI': 'CL=F', 'ORO': 'GC=F', 'PLATA': 'SI=F',
    'GAS_NATURAL': 'NG=F', 'USD_CLP': 'CLP=X', 'DOLAR_INDEX': 'DX-Y.NYB',
    'EURO_USD': 'EURUSD=X', 'BITCOIN_USD': 'BTC-USD', 'BONO_10Y': '^TNX',
    'LIT_ETF': 'LIT'
}
FECHA_INICIO = config.FECHA_INICIO
ARCHIVO_SALIDA_MACRO = config.ARCHIVO_MACRO

def descargar_datos_macro():
    print("--- INICIANDO DESCARGA DE DATOS MACROECONÓMICOS (v3.1 - Robusta con ECH) ---")
    lista_data_macro = []
    tickers_fallidos = []
    for nombre_amigable, ticker_yf in ACTIVOS_MACRO.items():
        try:
            print(f"-> Descargando: {nombre_amigable} ({ticker_yf})...")
            data = yf.download(ticker_yf, start=FECHA_INICIO, progress=False, auto_adjust=True)
            if data.empty: raise ValueError("No se devolvieron datos.")
            serie_close = data[['Close']].rename(columns={'Close': nombre_amigable})
            lista_data_macro.append(serie_close)
            time.sleep(0.2)
        except Exception as e:
            print(f"   !! ADVERTENCIA: Falló la descarga para {nombre_amigable}. Razón: {e}")
            tickers_fallidos.append(nombre_amigable)
    if not lista_data_macro:
        print("\n!! ERROR: No se pudo descargar ningún dato.")
        return
    print("\n-> Consolidando todos los datos descargados...")
    df_final = pd.concat(lista_data_macro, axis=1)
    df_final.ffill(inplace=True)
    df_final.reset_index(inplace=True)
    df_final.rename(columns={'Date': 'date'}, inplace=True)
    df_final['date'] = df_final['date'].dt.tz_localize(None)
    print(f"\n-> Guardando datos macroeconómicos en '{ARCHIVO_SALIDA_MACRO}'...")
    df_final.to_csv(ARCHIVO_SALIDA_MACRO, index=False, sep=';', decimal=',')
    print("\n--- ¡PROCESO COMPLETADO CON ÉXITO! ---")
    if tickers_fallidos:
        print(f"\nADVERTENCIA: No se pudieron descargar los siguientes indicadores: {', '.join(tickers_fallidos)}")
    print("\n--- VISTA PREVIA DE LOS DATOS ---")
    print(df_final.tail())

if __name__ == "__main__":
    descargar_datos_macro()