from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///:memory:", echo=True)  # Hvorfor ikke ha i work/???

# with engine.connect() as conn:
#    conn.execute("PRAGMA foreign_keys = ON;")

Base = declarative_base()

# TODO lage en fill() metode i hver som leser inn data.


class Enheter(Base):
    __tablename__ = "enheter"

    orgnr = Column(String, primary_key=True)


class Slakt(Base):
    __tablename__ = "slakt"

    orgnr = Column(String, ForeignKey("enheter.orgnr"), primary_key=True)
    dyr = Column(String, primary_key=True)
    økologisk = Column(String, primary_key=True)
    antall = Column(Integer)
    vekt = Column(Integer)


class Melk(Base):
    __tablename__ = "melk"

    orgnr = Column(String, ForeignKey("enheter.orgnr"), primary_key=True)
    produkt = Column(String, primary_key=True)
    økologisk = Column(String, primary_key=True)
    liter = Column(Integer)


class Korn(Base):
    __tablename__ = "korn"

    orgnr = Column(String, ForeignKey("enheter.orgnr"), primary_key=True)
    vekst = Column(String, primary_key=True)
    økologisk = Column(String, primary_key=True)
    matkvalitet = Column(String, primary_key=True)
    innleveringstype = Column(String, primary_key=True)
    vekt = Column(Integer)  # Kvantum tørr vare


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
