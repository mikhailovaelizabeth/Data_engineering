import argparse
import logging

from etl.extract import extract
from etl.transform import transform
from etl.validate import validate_basic
from etl.load import save_processed, load_to_db
from etl.collect import main as collect_data

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def run(source: str, max_rows: int = 100, to_db: bool = False):
    df = extract(source)
    df = transform(df)
    issues = validate_basic(df, max_rows_in_db=max_rows)
    log.info("Validation: %s", issues)
    processed_path = save_processed(df)
    log.info("Processed saved at %s", processed_path)
    if to_db:
        load_to_db(df, max_rows=max_rows)
    else:
        log.info("DB load skipped")

def main():

    parser = argparse.ArgumentParser(description="ETL runner")
    parser.add_argument(
        "--source-type",
        choices=["local", "gdrive", "collect"],
        default="local",
        help="Тип источника данных: 'local' — локальный файл, 'gdrive' — Google Drive, 'collect' — сбор данных с PubChem по API"
    )

    parser.add_argument("--to-db", action="store_true", help="загрузить данные в базу данных")
    parser.add_argument("--max-rows", type=int, default=100, help="максимальное колличество строк для записи в бд (по умолчанию 100)")

    args = parser.parse_args()

    if args.source_type == 'collect':
        print("Скачиваю данные с PubChem...")
        collect_data()
        args.source_type = 'local'
    elif args.source_type not in ["local", "gdrive"]:
        raise ValueError("Неизвестный тип источника данных!")

    run(args.source_type, max_rows=args.max_rows, to_db=args.to_db)


if __name__ == "__main__":
    main()
