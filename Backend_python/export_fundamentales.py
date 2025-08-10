"""
Exporta la base fundamental generada a la tabla `fundamentals` (MySQL) usando UPSERT.
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

from Backend_python.db import init_schema, upsert_fundamental


def ejecutar_export_fundamental(path_csv: str) -> None:
    if not os.path.exists(path_csv):
        raise FileNotFoundError(f"No existe el archivo: {path_csv}")

    init_schema()
    df = pd.read_csv(path_csv, sep=";", decimal=",")
    df.columns = [c.strip().lower() for c in df.columns]

    registros = 0
    for _, row in df.iterrows():
        upsert_fundamental({
            "ticker": str(row["ticker"]).strip(),
            "year": int(row["year"]),
            "pe_ratio": float(row.get("pe_ratio")) if not pd.isna(row.get("pe_ratio")) else None,
            "pb_ratio": float(row.get("pb_ratio")) if not pd.isna(row.get("pb_ratio")) else None,
            "roe": float(row.get("roe")) if not pd.isna(row.get("roe")) else None,
            "debt_to_equity": float(row.get("debt_to_equity")) if not pd.isna(row.get("debt_to_equity")) else None,
            "current_ratio": float(row.get("current_ratio")) if not pd.isna(row.get("current_ratio")) else None,
            "dividend_yield": float(row.get("dividend_yield")) if not pd.isna(row.get("dividend_yield")) else None,
            "salud_financiera": None if pd.isna(row.get("salud_financiera")) else str(row.get("salud_financiera")),
        })
        registros += 1
    print(f"Exportación completada. Registros procesados: {registros}")


if __name__ == "__main__":
    ejecutar_export_fundamental(config.ARCHIVO_FUNDAMENTAL)


