import requests
import pandas as pd
import time

#Список запрашиваемых параметров с pubchem

PROPERTIES = ",".join([
    "MolecularFormula", "MolecularWeight", "CanonicalSMILES",
    "IsomericSMILES", "InChIKey", "XLogP", "TPSA",
    "HBondDonorCount", "HBondAcceptorCount", "RotatableBondCount",
    "ExactMass", "MonoisotopicMass", "HeavyAtomCount",
    "Charge", "Complexity"
])
#Функция, которая запрашивает данные
def fetch_properties(cids):
    cid_str = ",".join(map(str, cids))
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid_str}/property/{PROPERTIES}/JSON"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()["PropertyTable"]["Properties"]
    else:
        print(f"Ошибка {r.status_code} для CIDs {cid_str}")
        return []


def main():
    #Создание списка ID
    all_cids = list(range(1, 2001))

    #Пустой список, куда записываются полученные данные
    records = []
    #Запрос данных с определенным шагом и временной задержкой
    for i in range(0, len(all_cids), 100):
        batch = all_cids[i:i+100]
        props = fetch_properties(batch)
        records.extend(props)
        time.sleep(0.2)

    #Преобразование из нечитаемых данных в читаемые
    df = pd.DataFrame(records)
    df.to_csv("../data/pubchem_raw.csv", index=False)
    print(f"Собрано {len(df)} записей")

if __name__ == "__main__":
    main()