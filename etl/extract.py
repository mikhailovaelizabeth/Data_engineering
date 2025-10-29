from pathlib import Path
import pandas as pd
import logging
import gdown

log = logging.getLogger(__name__)

def extract(source: str, raw_dir: str = "data/raw", filename: str = "dataset.csv") -> pd.DataFrame:
    Path(raw_dir).mkdir(parents=True, exist_ok=True)
    dest = Path(raw_dir) / filename

    log.info("Extract: source=%s", source)
    try:
        # special short form: gdrive:<id>
        if source.startswith("gdrive:"):
            file_id = source.split("gdrive:", 1)[1]
            url = f"https://drive.google.com/uc?id={file_id}"
            log.info("Downloading from Google Drive id=%s", file_id)
            gdown.download(url, str(dest), quiet=False)
            df = pd.read_csv(dest)
        elif "drive.google.com" in source or "uc?id=" in source:
            log.info("Downloading from Google Drive url")
            gdown.download(source, str(dest), quiet=False)
            df = pd.read_csv(dest)
        else:
            # local path or http(s)
            log.info("Reading CSV directly from %s", source)
            df = pd.read_csv(source)
            # сохраняем копию
            df.to_csv(dest, index=False)
        if df.empty:
            raise ValueError("Extract: dataframe is empty")
        log.info("Extract done, saved raw to %s", dest)
        return df
    except Exception:
        log.exception("Error in extract")
        raise