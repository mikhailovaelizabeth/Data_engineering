import argparse
import logging
from etl.extract import extract
from etl.transform import transform
from etl.validate import validate_basic
from etl.load import save_processed, load_to_db
from etl.collect import main as collect_data   # 👈 добавлено

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def run(source: str, max_rows: int = 100, no_db: bool = False):
    df = extract(source)
    df = transform(df)
    issues = validate_basic(df, max_rows_in_db=max_rows)
    log.info("Validation: %s", issues)
    processed_path = save_processed(df)
    log.info("Processed saved at %s", processed_path)
    if not no_db:
        load_to_db(df, max_rows=max_rows)
    else:
        log.info("DB load skipped (--no-db)")

def main():
    parser = argparse.ArgumentParser(description="ETL runner")
    parser.add_argument("source", nargs="?", help="path or url to source CSV, or 'gdrive:<file_id>' for Google Drive")
    parser.add_argument("--max-rows", type=int, default=100, help="max rows to write to DB (default 100)")
    parser.add_argument("--no-db", action="store_true", help="skip DB load (only save processed file)")
    parser.add_argument("--collect", action="store_true", help="скачать данные с PubChem перед обработкой")  # 👈 добавлено
    args = parser.parse_args()

    if args.collect:
        print("🧩 Скачиваю данные с PubChem...")
        collect_data()
        source = "data/raw/pubchem_raw.csv"
    else:
        if not args.source:
            parser.error("нужно указать --collect или путь к файлу source")
        source = args.source

    run(source, max_rows=args.max_rows, no_db=args.no_db)

if __name__ == "__main__":
    main()
