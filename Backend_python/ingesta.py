"""
Ingesta de datos de precios desde CSV a MySQL con UPSERT.

Lee `acciones_master.csv` (OHLCV por ticker y fecha) y llena las tablas `prices`.
"""

import os
import pandas as pd
from datetime import datetime

try:
    import sys
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if ROOT not in sys.path:
        sys.path.append(ROOT)
    import config
except Exception as exc:
    raise RuntimeError("No se pudo importar config.py desde la raíz del proyecto.") from exc

from Backend_python.db import init_schema, upsert_price


def normalizar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    if "fecha" in df.columns and "date" not in df.columns:
        df.rename(columns={"fecha": "date"}, inplace=True)
    if "nemotecnico" in df.columns and "ticker" not in df.columns:
        df.rename(columns={"nemotecnico": "ticker"}, inplace=True)

    # Asegurar tipos
    df["date"] = pd.to_datetime(df["date"], dayfirst=True).dt.date
    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if "volume" in df.columns:
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0).astype(int)
    else:
        df["volume"] = 0
    df = df.dropna(subset=["ticker", "date", "open", "high", "low", "close"]) 
    return df


def ejecutar_ingesta_precio_desde_csv(path_csv: str) -> None:
    if not os.path.exists(path_csv):
        raise FileNotFoundError(f"No existe el archivo: {path_csv}")

    init_schema()
    df = pd.read_csv(path_csv, sep=";", decimal=",")
    df = normalizar_dataframe(df)

    registros = 0
    for _, row in df.iterrows():
        upsert_price({
            "ticker": str(row["ticker"]).strip(),
            "trade_date": row["date"],
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
            "volume": int(row.get("volume", 0)),
        })
        registros += 1
    print(f"Ingesta completada. Registros procesados: {registros}")


if __name__ == "__main__":
    ejecutar_ingesta_precio_desde_csv(config.ARCHIVO_ACCIONES_MASTER)


