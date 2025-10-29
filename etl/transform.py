# etl/transform.py
import pandas as pd
from typing import List

# предполагаемые числовые и категориальные колонки — подкорректируй при необходимости
NUMERIC_COLS = [
    "MolecularWeight","XLogP","TPSA","HBondDonorCount","HBondAcceptorCount",
    "RotatableBondCount","ExactMass","MonoisotopicMass","HeavyAtomCount","Charge","Complexity"
]
CAT_COLS = [
    "MolecularFormula","CanonicalSMILES","IsomericSMILES","InChIKey",
    "SMILES","ConnectivitySMILES"
]

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # убираем лишние пробелы в именах колонок
    df.columns = [c.strip() for c in df.columns]

    # numeric conversion
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            # downcast numeric types where possible
            if pd.api.types.is_float_dtype(df[col].dtype):
                try:
                    df[col] = pd.to_numeric(df[col], downcast="float")
                except Exception:
                    pass
            else:
                try:
                    df[col] = pd.to_numeric(df[col], downcast="integer")
                except Exception:
                    pass

    # categorical
    for col in CAT_COLS:
        if col in df.columns:
            df[col] = df[col].astype("category")

    # примеры чисток: удалить дубли, сбросить индекс
    df = df.drop_duplicates().reset_index(drop=True)
    return df
