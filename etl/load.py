# etl/load.py
import os
from pathlib import Path
import pandas as pd
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv

log = logging.getLogger(__name__)
load_dotenv()

def save_processed(df: pd.DataFrame, processed_dir: str = "data/processed", filename: str = "processed_dataset.parquet"):
    Path(processed_dir).mkdir(parents=True, exist_ok=True)
    out = Path(processed_dir) / filename
    try:
        df.to_parquet(out, index=False)
        log.info("Saved parquet to %s", out)
    except Exception as e:
        csv_out = Path(processed_dir) / filename.replace(".parquet", ".csv")
        df.to_csv(csv_out, index=False)
        log.warning("Parquet write failed (%s). Saved CSV to %s", e, csv_out)
        out = csv_out
    return out

def load_to_db(df: pd.DataFrame, max_rows: int = 100):
    """
    Попытка подключиться к Postgres по .env. Если env-переменных нет — fallback на sqlite.
    Загружаем не более max_rows строк (head).
    """
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")
    TABLE_NAME = os.getenv("TABLE_NAME", "molecules")

    if DB_USER and DB_PASSWORD and DB_HOST and DB_NAME:
        DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(DATABASE_URL)
        log.info("Using Postgres DB: %s", DB_HOST)
    else:
        sqlite_path = Path("data") / "etl.db"
        engine = create_engine(f"sqlite:///{sqlite_path}")
        log.info("Using sqlite fallback at %s", sqlite_path)

    to_write = df.head(max_rows)
    to_write.to_sql(name=TABLE_NAME, con=engine, if_exists="append", index=False)
    log.info("Wrote %d rows to table %s", len(to_write), TABLE_NAME)
