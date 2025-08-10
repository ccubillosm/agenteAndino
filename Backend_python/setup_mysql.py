"""
Crea la base de datos MySQL configurada en `config.py` y levanta el esquema de tablas.
"""

import os
import pymysql

try:
    import sys
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if ROOT not in sys.path:
        sys.path.append(ROOT)
    import config
except Exception as exc:
    raise RuntimeError("No se pudo importar config.py desde la raíz del proyecto.") from exc

from Backend_python.db import init_schema


def ensure_database_exists() -> None:
    conn = pymysql.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        charset="utf8mb4",
        autocommit=True,
    )
    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{config.MYSQL_DATABASE}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    finally:
        conn.close()


def main() -> None:
    ensure_database_exists()
    init_schema()
    print("Base de datos y esquema listos.")


if __name__ == "__main__":
    main()


