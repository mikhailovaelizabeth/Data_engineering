import requests
import pandas as pd
import time
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

PROPERTIES = ",".join([
    "MolecularFormula", "MolecularWeight", "CanonicalSMILES",
    "IsomericSMILES", "InChIKey", "XLogP", "TPSA",
    "HBondDonorCount", "HBondAcceptorCount", "RotatableBondCount",
    "ExactMass", "MonoisotopicMass", "HeavyAtomCount",
    "Charge", "Complexity"
])

def fetch_properties(cids):
    cid_str = ",".join(map(str, cids))
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid_str}/property/{PROPERTIES}/JSON"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()["PropertyTable"]["Properties"]
    except requests.RequestException as e:
        log.warning(f"Ошибка при запросе CIDs {cid_str}: {e}")
        return []

def main():
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    all_cids = list(range(1, 2001))
    records = []

    for i in range(0, len(all_cids), 20):
        batch = all_cids[i:i+20]
        props = fetch_properties(batch)
        records.extend(props)
        log.info(f"Обработано {i+len(batch)} / {len(all_cids)} CID")
        time.sleep(0.2)

    df = pd.DataFrame(records)
    output_path = "data/raw/pubchem_raw.csv"
    df.to_csv(output_path, index=False)
    log.info(f"Собрано {len(df)} записей, сохранено в {output_path}")

if __name__ == "__main__":
    main()
