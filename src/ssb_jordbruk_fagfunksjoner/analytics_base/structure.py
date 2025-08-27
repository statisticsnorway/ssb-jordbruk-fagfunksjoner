import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

environment = os.getenv("DAPLA_ENVIRONMENT").lower()
bruker = os.getenv("DAPLA_USER")[:3]
tjeneste = os.getenv("DAPLA_SERVICE").lower()

tz = ZoneInfo('Europe/Oslo')
timestamp = datetime.now(tz)

# Format as year_month_day_hour_minutes
timestamp = timestamp.strftime('%Y_%m_%d_%H_%M')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f"/buckets/produkt/temp/oppdragsbase/logs/analytics_assembly_{environment}_{bruker}_{tjeneste}_{timestamp}.log", mode="a") # Save log to bucket
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s",
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

db_path = "/home/onyxia/work/analytics.sqlite"
os.makedirs(os.path.dirname(db_path), exist_ok=True)
engine = create_engine(f"sqlite:///{db_path}", echo=True)


# Enable foreign keys for all connections
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


event.listen(engine, "connect", enable_foreign_keys)

Base = declarative_base()

# TODO lage en fill() metode i hver som leser inn data.

def read_and_log(path):
    data = pd.read_parquet(path)
    logger.info(f"Reading file: {path}\nShape: {data.shape}\nColumns: {data.columns}")
    return data


class Enheter(Base):
    __tablename__ = "enheter"

    orgnr = Column(String, primary_key=True)

    def fill(self): ...


class Slakt(Base):
    __tablename__ = "slakt"

    orgnr = Column(String, primary_key=True)  # ForeignKey("enheter.orgnr"),
    aar = Column(String, primary_key=True)
    kvartal = Column(String, primary_key=True)
    # maaned = Column(String, primary_key=True)
    # dag = Column(String, primary_key=True)
    dyr = Column(String, primary_key=True)
    økologisk = Column(String, primary_key=True)
    antall = Column(Integer)
    vekt = Column(Integer)

    def fill(self, session):
        logger.info("Starting insert into 'slakt'.")
        for _, row in (
            pd.read_parquet(
                "/buckets/produkt/leveranser/slakt/klargjorte-data/slakt_p2024_v1.parquet"
            )
            .groupby(["orgnr", "dyr", "økologisk", "aar", "kvartal"], as_index=False)
            .agg({"antall": "sum", "vekt": "sum"})
            .iterrows()
        ):
            if int(row["antall"]) > 0 or int(row["vekt"]) > 0:
                try:
                    session.add(
                        Slakt(
                            orgnr=str(row["orgnr"]),
                            aar=str(row["aar"]),
                            kvartal=str(row["kvartal"]),
                            dyr=str(row["dyr"]),
                            økologisk=str(row["økologisk"]),
                            antall=int(row["antall"]),
                            vekt=int(row["vekt"])
                        )
                    )
                    session.commit()
                    logger.debug("Comitted")
                except Exception as e:
                    logger.debug("OMG NO")
                    logger.debug(row)
                    session.rollback()
                    raise e
            logger.info("Successfully inserted into 'slakt'.")



class Melk(Base):
    __tablename__ = "melk"

    orgnr = Column(String, primary_key=True)  # ForeignKey("enheter.orgnr"),
    produkt = Column(String, primary_key=True)
    økologisk = Column(String, primary_key=True)
    liter = Column(Integer)

    def fill(self, session):
        logger.info("Starting insert into 'melk'.")
        for _, row in (
            pd.read_parquet(
                "/buckets/produkt/leveranser/melk/klargjorte-data/melkeleveranser_p2025_v1.parquet"
            )
            .groupby(["orgnr", "vare", "produkttype"], as_index=False)
            .agg({"mengde": "sum"})
            .iterrows()
        ):
            if int(row["mengde"]) > 0:
                try:
                    session.add(
                        Melk(
                            orgnr=str(row["orgnr"]),
                            produkt=str(row["vare"]),
                            økologisk=str(row["produkttype"]),
                            liter=int(row["mengde"]),
                        )
                    )
                    session.commit()
                    logger.debug("Comitted")
                except Exception as e:
                    logger.debug("OMG NO")
                    logger.debug(row[["orgnr", "vare", "produkttype", "mengde"]])
                    session.rollback()
                    raise e
        logger.info("Successfully inserted into 'melk'.")


class Korn(Base):
    __tablename__ = "korn"

    orgnr = Column(String, primary_key=True)  # ForeignKey("enheter.orgnr"),
    vekst = Column(String, primary_key=True)
    økologisk = Column(String, primary_key=True)
    matkvalitet = Column(String, primary_key=True)
    innleveringstype = Column(String, primary_key=True)
    vekt = Column(Integer)  # Kvantum tørr vare


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

with engine.connect() as conn:
    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
    print("Existing tables:")
    for row in result:
        print(row)


def assemble_database():
    Slakt().fill(session)
    Melk().fill(session)



def test_query():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM melk"))
        for row in result:
            print(row)


if __name__ == "__main__":
    assemble_database()
    test_query()
