"""
Descarga datos OHLCV de acciones chilenas (lista en CSV/acciones.csv) usando Yahoo Finance y genera `acciones_master.csv`.

Lee `CSV/acciones.csv` (columna NEMOTECNICO) y usa el sufijo configurado para Yahoo Finance (por defecto ".SN").
"""

import os
import time
from typing import List
import pandas as pd
import yfinance as yf

try:
    import sys
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if ROOT not in sys.path:
        sys.path.append(ROOT)
    import config
except Exception as exc:
    raise RuntimeError("No se pudo importar config.py desde la raíz del proyecto.") from exc


def cargar_lista_tickers(path_acciones_csv: str) -> List[str]:
    df = pd.read_csv(path_acciones_csv)
    col = "NEMOTECNICO" if "NEMOTECNICO" in df.columns else df.columns[0]
    tickers = df[col].dropna().astype(str).str.strip().tolist()
    return tickers


def descargar_ohlcv_para_ticker(nemo: str) -> pd.DataFrame:
    yf_ticker = f"{nemo}{config.YF_SANTIAGO_SUFFIX}"
    data = yf.download(yf_ticker, start=config.FECHA_INICIO, auto_adjust=False, progress=False)
    if data.empty:
        return pd.DataFrame()
    
    # Manejar columnas multinivel si existen
    if isinstance(data.columns, pd.MultiIndex):
        # Flatten columnas multinivel - tomar solo el nombre de la columna OHLCV
        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
    
    data = data.reset_index()
    
    # Verificar qué columnas están disponibles
    available_cols = data.columns.tolist()
    print(f"   Columnas disponibles para {nemo}: {available_cols}")
    
    # Mapear columnas disponibles
    col_mapping = {}
    if "Open" in available_cols:
        col_mapping["Open"] = "open"
    if "High" in available_cols:
        col_mapping["High"] = "high"
    if "Low" in available_cols:
        col_mapping["Low"] = "low"
    if "Close" in available_cols:
        col_mapping["Close"] = "close"
    if "Adj Close" in available_cols:
        col_mapping["Adj Close"] = "adj close"
    if "Volume" in available_cols:
        col_mapping["Volume"] = "volume"
    if "Date" in available_cols:
        col_mapping["Date"] = "date"
    
    data.rename(columns=col_mapping, inplace=True)
    data["ticker"] = nemo
    
    # Normalizar tipos
    data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
    
    
    # Seleccionar solo las columnas que existen
    required_cols = ["date", "ticker"]
    for col in ["open", "high", "low", "close", "adj close", "volume"]:
        if col in data.columns:
            required_cols.append(col)
    
    return data[required_cols]


def construir_master_desde_lista() -> pd.DataFrame:
    tickers = cargar_lista_tickers(config.CSV_ACCIONES)
    frames: List[pd.DataFrame] = []
    for nemo in tickers:
        try:
            print(f"Descargando {nemo}...")
            df_t = descargar_ohlcv_para_ticker(nemo)
            if not df_t.empty:
                frames.append(df_t)
            else:
                print(f"   Advertencia: sin datos para {nemo}")
        except Exception as e:
            print(f"   Error al descargar {nemo}: {e}")
        time.sleep(0.2)
    if not frames:
        return pd.DataFrame()
    df = pd.concat(frames, ignore_index=True)
    return df


def main() -> None:
    print("--- Descarga de acciones IPSA (Yahoo Finance) ---")
    df = construir_master_desde_lista()
    if df.empty:
        print("No se pudo construir el master de acciones.")
        return
    df.to_csv(config.ARCHIVO_ACCIONES_MASTER, index=False, sep=";", decimal=",")
    print(f"Guardado en {config.ARCHIVO_ACCIONES_MASTER}")


if __name__ == "__main__":
    main()


