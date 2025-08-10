import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from typing import Iterator

try:
    # Import local config from project root
    import sys
    import os
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if ROOT not in sys.path:
        sys.path.append(ROOT)
    import config
except Exception as exc:
    raise RuntimeError("No se pudo importar config.py. Asegúrate de crear y configurar el archivo en la raíz del proyecto.") from exc


def get_connection() -> pymysql.Connection:
    return pymysql.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DATABASE,
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=False,
    )


@contextmanager
def db_cursor() -> Iterator[pymysql.cursors.Cursor]:
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_schema() -> None:
    """Crea tablas necesarias si no existen."""
    create_prices = """
    CREATE TABLE IF NOT EXISTS prices (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        ticker VARCHAR(32) NOT NULL,
        trade_date DATE NOT NULL,
        open DECIMAL(18,6) NOT NULL,
        high DECIMAL(18,6) NOT NULL,
        low DECIMAL(18,6) NOT NULL,
        close DECIMAL(18,6) NOT NULL,
        volume BIGINT NULL,
        UNIQUE KEY uniq_ticker_date (ticker, trade_date)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    create_indicators = """
    CREATE TABLE IF NOT EXISTS indicators (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        ticker VARCHAR(32) NOT NULL,
        trade_date DATE NOT NULL,
        rsi DECIMAL(18,6) NULL,
        macd DECIMAL(18,6) NULL,
        macd_signal DECIMAL(18,6) NULL,
        macd_hist DECIMAL(18,6) NULL,
        sma_20 DECIMAL(18,6) NULL,
        sma_50 DECIMAL(18,6) NULL,
        sma_200 DECIMAL(18,6) NULL,
        adx DECIMAL(18,6) NULL,
        atr DECIMAL(18,6) NULL,
        cci DECIMAL(18,6) NULL,
        stoch_k DECIMAL(18,6) NULL,
        stoch_d DECIMAL(18,6) NULL,
        psar DECIMAL(18,6) NULL,
        obv DECIMAL(20,6) NULL,
        bb_high DECIMAL(18,6) NULL,
        bb_mid DECIMAL(18,6) NULL,
        bb_low DECIMAL(18,6) NULL,
        ichimoku_a DECIMAL(18,6) NULL,
        ichimoku_b DECIMAL(18,6) NULL,
        UNIQUE KEY uniq_ticker_date (ticker, trade_date)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    create_fundamental = """
    CREATE TABLE IF NOT EXISTS fundamentals (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        ticker VARCHAR(32) NOT NULL,
        year INT NOT NULL,
        pe_ratio DECIMAL(18,6) NULL,
        pb_ratio DECIMAL(18,6) NULL,
        roe DECIMAL(18,6) NULL,
        debt_to_equity DECIMAL(18,6) NULL,
        current_ratio DECIMAL(18,6) NULL,
        dividend_yield DECIMAL(18,6) NULL,
        salud_financiera VARCHAR(16) NULL,
        UNIQUE KEY uniq_ticker_year (ticker, year)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    with db_cursor() as cursor:
        cursor.execute(create_prices)
        cursor.execute(create_indicators)
        cursor.execute(create_fundamental)


def upsert_price(row: dict) -> None:
    sql = """
    INSERT INTO prices (ticker, trade_date, open, high, low, close, volume)
    VALUES (%(ticker)s, %(trade_date)s, %(open)s, %(high)s, %(low)s, %(close)s, %(volume)s)
    ON DUPLICATE KEY UPDATE
        open = VALUES(open),
        high = VALUES(high),
        low = VALUES(low),
        close = VALUES(close),
        volume = VALUES(volume)
    """
    with db_cursor() as cursor:
        cursor.execute(sql, row)


def upsert_indicator(row: dict) -> None:
    sql = """
    INSERT INTO indicators (
        ticker, trade_date, rsi, macd, macd_signal, macd_hist, sma_20, sma_50, sma_200,
        adx, atr, cci, stoch_k, stoch_d, psar, obv, bb_high, bb_mid, bb_low, ichimoku_a, ichimoku_b
    ) VALUES (
        %(ticker)s, %(trade_date)s, %(rsi)s, %(macd)s, %(macd_signal)s, %(macd_hist)s, %(sma_20)s, %(sma_50)s, %(sma_200)s,
        %(adx)s, %(atr)s, %(cci)s, %(stoch_k)s, %(stoch_d)s, %(psar)s, %(obv)s, %(bb_high)s, %(bb_mid)s, %(bb_low)s, %(ichimoku_a)s, %(ichimoku_b)s
    )
    ON DUPLICATE KEY UPDATE
        rsi = VALUES(rsi), macd = VALUES(macd), macd_signal = VALUES(macd_signal), macd_hist = VALUES(macd_hist),
        sma_20 = VALUES(sma_20), sma_50 = VALUES(sma_50), sma_200 = VALUES(sma_200),
        adx = VALUES(adx), atr = VALUES(atr), cci = VALUES(cci), stoch_k = VALUES(stoch_k), stoch_d = VALUES(stoch_d),
        psar = VALUES(psar), obv = VALUES(obv), bb_high = VALUES(bb_high), bb_mid = VALUES(bb_mid), bb_low = VALUES(bb_low),
        ichimoku_a = VALUES(ichimoku_a), ichimoku_b = VALUES(ichimoku_b)
    """
    with db_cursor() as cursor:
        cursor.execute(sql, row)


def upsert_fundamental(row: dict) -> None:
    sql = """
    INSERT INTO fundamentals (
        ticker, year, pe_ratio, pb_ratio, roe, debt_to_equity, current_ratio, dividend_yield, salud_financiera
    ) VALUES (
        %(ticker)s, %(year)s, %(pe_ratio)s, %(pb_ratio)s, %(roe)s, %(debt_to_equity)s, %(current_ratio)s, %(dividend_yield)s, %(salud_financiera)s
    )
    ON DUPLICATE KEY UPDATE
        pe_ratio = VALUES(pe_ratio), pb_ratio = VALUES(pb_ratio), roe = VALUES(roe),
        debt_to_equity = VALUES(debt_to_equity), current_ratio = VALUES(current_ratio),
        dividend_yield = VALUES(dividend_yield), salud_financiera = VALUES(salud_financiera)
    """
    with db_cursor() as cursor:
        cursor.execute(sql, row)


