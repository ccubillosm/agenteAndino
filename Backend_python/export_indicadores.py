"""
Exporta indicadores calculados por `motor_condor.py` a la tabla `indicators` (MySQL) usando UPSERT.

Lee `database_maestra_tecnica.csv` y mapea columnas relevantes.
"""

import os
import pandas as pd

try:
    import sys
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if ROOT not in sys.path:
        sys.path.append(ROOT)
    import config
except Exception as exc:
    raise RuntimeError("No se pudo importar config.py desde la raíz del proyecto.") from exc

from Backend_python.db import init_schema, upsert_indicator


COLUMN_MAP = {
    "rsi_14": "rsi",
    "macd_12_26_9": "macd",
    "macds_12_26_9": "macd_signal",
    "macdh_12_26_9": "macd_hist",
    "sma_20": "sma_20",
    "sma_50": "sma_50",
    "sma_200": "sma_200",
    "adx_14": "adx",
    "atr_14": "atr",
    "cci_20": "cci",
    "stochk_14_3_3": "stoch_k",
    "stochd_14_3_3": "stoch_d",
    "psar": "psar",
    "obv": "obv",
    "bbu_20_2.0": "bb_high",
    "bbm_20_2.0": "bb_mid",
    "bbl_20_2.0": "bb_low",
    "isa_9": "ichimoku_a",
    "isb_26": "ichimoku_b",
}


def ejecutar_export_indicadores(path_csv: str) -> None:
    if not os.path.exists(path_csv):
        raise FileNotFoundError(f"No existe el archivo: {path_csv}")

    init_schema()
    df = pd.read_csv(path_csv, sep=";", decimal=",")
    df.columns = [c.strip().lower() for c in df.columns]
    if "fecha" in df.columns and "date" not in df.columns:
        df.rename(columns={"fecha": "date"}, inplace=True)
    if "nemotecnico" in df.columns and "ticker" not in df.columns:
        df.rename(columns={"nemotecnico": "ticker"}, inplace=True)

    # Asegurar columnas esenciales
    required = {"ticker", "date"}
    if not required.issubset(set(df.columns)):
        missing = required - set(df.columns)
        raise ValueError(f"Faltan columnas requeridas: {missing}")

    # Iterar filas y mapear indicadores
    registros = 0
    for _, row in df.iterrows():
        payload = {
            "ticker": str(row["ticker"]).strip(),
            "trade_date": pd.to_datetime(row["date"], dayfirst=True).date(),
        }
        for csv_col, db_col in COLUMN_MAP.items():
            value = row.get(csv_col)
            if pd.isna(value):
                payload[db_col] = None
            else:
                try:
                    payload[db_col] = float(value)
                except Exception:
                    payload[db_col] = None
        upsert_indicator(payload)
        registros += 1
    print(f"Exportación completada. Registros procesados: {registros}")


if __name__ == "__main__":
    ejecutar_export_indicadores(config.ARCHIVO_TECNICO)


