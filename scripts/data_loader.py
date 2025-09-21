import pandas as pd

FILE_ID = "1ikuXF1TNjzX6-_GKWLaPh_9Jz0txgVDM"
file_url = f"https://drive.google.com/uc?id={FILE_ID}"

def main():
    try:
        raw_data = pd.read_csv(file_url)

        print("Первые 10 строк датасета:")
        print(raw_data.head(10))

    except Exception as e:
        print("Ошибка при загрузке файла:", e)

if __name__ == "__main__":
    main()

