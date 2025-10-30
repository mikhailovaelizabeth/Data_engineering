from pathlib import Path
from etl.collect import main as collect_data
import pandas as pd
import logging
import gdown
import os

log = logging.getLogger(__name__)

def extract(source_type: str, raw_dir: str = "data/raw", filename: str = "dataset.csv") -> pd.DataFrame:
    Path(raw_dir).mkdir(parents=True, exist_ok=True)
    dest = Path(raw_dir) / filename

    LOCAL_SOURCE = os.getenv("LOCAL_SOURCE", "data/raw/pubchem_raw.csv")
    GDRIVE_SOURCE = os.getenv("GDRIVE_SOURCE", "https://drive.google.com/uc?id=1ikuXF1TNjzX6-_GKWLaPh_9Jz0txgVDM")

    try:
        if source_type == "gdrive":
            log.info("Extract: source=Google Drive (%s)", GDRIVE_SOURCE)
            gdown.download(GDRIVE_SOURCE, str(dest), quiet=False)
            df = pd.read_csv(dest)
        elif source_type == "local":
            if not os.path.exists(LOCAL_SOURCE):
                raise FileNotFoundError(LOCAL_SOURCE)
            log.info("Extract: source=Local (%s)", LOCAL_SOURCE)
            df = pd.read_csv(LOCAL_SOURCE)
            #копия в data/raw
            df.to_csv(dest, index=False)

        else:
            raise ValueError(f"Неизвестный тип источника: {source_type}")

        if df.empty:
            raise ValueError("Extract: dataframe is empty")

        log.info("Extract done, saved raw to %s", dest)
        return df


    except FileNotFoundError:
        print(f"\n Файл '{LOCAL_SOURCE}' не найден.")
        print("Выберите действие:")
        print("  0 — собрать данные с PubChem")
        print("  1 — скачать данные с Google Drive")
        print("  2 — завершить программу")

        choice = input("Ваш выбор: ").strip()

        if choice == "0":
            print("Собираем данные с PubChem...")
            collect_data()
            return pd.read_csv("data/raw/pubchem_raw.csv")

        elif choice == "1":
            url = GDRIVE_SOURCE
            print(f"Скачиваем с Google Drive ({url})...")
            gdown.download(url, str(dest), quiet=False)
            return pd.read_csv(dest)

        else:
            print("Завершаем работу. До встречи <3")
            exit(0)

    except Exception:
        log.exception("Error in extract")
        raise