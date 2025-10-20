import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

#обращение к переменным окружения
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
TABLE_NAME = os.getenv("TABLE_NAME")

#оздание ссылки
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

#создание базового класса для схемы
Base = declarative_base()

class ExampleTable(Base):
    __tablename__ = TABLE_NAME
    __table_args__ = {"schema": "public"}

    #создание схемы таблицы с колонками базы данных
    CID = Column(Integer, primary_key=True, autoincrement=True)
    MolecularFormula = Column(String)
    MolecularWeight = Column(Float)
    SMILES = Column(String)
    ConnectivitySMILES = Column(String)
    InChIKey = Column(String)
    XLogP = Column(Float)
    ExactMass = Column(Float)
    MonoisotopicMass = Column(Float)
    TPSA = Column(Float)
    Complexity = Column(Float)
    Charge = Column(Float)
    HBondDonorCount = Column(Float)
    HBondAcceptorCount = Column(Float)
    RotatableBondCount = Column(Float)
    HeavyAtomCount = Column(Float)

#создание таблицы без данных
Base.metadata.create_all(engine)

#создание сессии
Session = sessionmaker(bind=engine)
session = Session()

#бращение к паркет файлу
parquet_path = "/data/processed_dataset.parquet"
df = pd.read_parquet(parquet_path)

df_sample = df.head(100)

df_sample.to_sql(name=TABLE_NAME, con=engine, if_exists="append", index=False)

