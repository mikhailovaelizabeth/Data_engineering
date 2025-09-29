import pandas as pd
import gdown

FILE_ID = "1ikuXF1TNjzX6-_GKWLaPh_9Jz0txgVDM"
FILE_URL = f"https://drive.google.com/uc?id={FILE_ID}"

def main():
    try:
        output = "dataset.csv"
        gdown.download(FILE_URL, output, quiet=False)
        print(f"Файл успешно скачан: {output}")

        raw_data = pd.read_csv(FILE_URL)

        print("Первые 10 строк датасета:")
        print(raw_data.head(10))

        # Автоматическое приведение типов
        # Категориальные
        cat_cols = [
            "MolecularFormula", "MolecularWeight", "CanonicalSMILES",
            "IsomericSMILES", "InChIKey", "XLogP", "TPSA",
            "HBondDonorCount", "HBondAcceptorCount", "RotatableBondCount",
            "ExactMass", "MonoisotopicMass", "HeavyAtomCount",
            "Charge", "Complexity"
        ]
        for col in cat_cols:
            if col in raw_data.columns:
                raw_data[col] = raw_data[col].astype("category")
        # Числовые
        for col in raw_data.select_dtypes(include="int64").columns:
            raw_data[col] = pd.to_numeric(raw_data[col], downcast="integer")
        for col in raw_data.select_dtypes(include="float64").columns:
            raw_data[col] = pd.to_numeric(raw_data[col], downcast="float")

        # --- Сохраняем результат ---
        processed_output = "processed_dataset.parquet"
        raw_data.to_parquet(processed_output, index=False)

        print(f"Датасет приведён к оптимальным типам и сохранён в {processed_output}")

    except Exception as e:
        print("Ошибка при загрузке файла:", e)


if __name__ == "__main__":
    main()


