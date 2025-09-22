import logging
from functools import lru_cache
import sqlite3
import os
from zoneinfo import ZoneInfo
from datetime import datetime
from typing import Any

import pandas as pd

logger = logging.getLogger(
    __name__
)  # Make sure it logs everything needed to figure out what was being done.

environment = os.getenv("DAPLA_ENVIRONMENT").lower()
bruker = os.getenv("DAPLA_USER")[:3]
tjeneste = os.getenv("DAPLA_SERVICE").lower()

tz = ZoneInfo("Europe/Oslo")
timestamp = datetime.now(tz)

# Format as year_month_day_hour_minutes
timestamp = timestamp.strftime("%Y_%m_%d_%H_%M")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(
    f"/buckets/produkt/temp/oppdragsbase/logs/analytics_userlog_{environment}_{bruker}_{tjeneste}_{timestamp}.log",
    mode="a",
)  # Save log to bucket
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s",
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class AnalyticsConnection:

    path_to_database: str = "/home/onyxia/work/analytics.sqlite"
    most_recent_query: str | None = None

    def __init__(self) -> None:
        self.conn = self.connect()

    def connect(self):
        return sqlite3.connect(self.path_to_database)

    def test_connection(self): ...

    @lru_cache(maxsize=1)
    def query(
        self, query, return_dataframe=True
    ) -> pd.DataFrame | tuple[list[str], list[Any]]:
        logger.info(f"Running query:\n{query}")
        self.most_recent_query = query
        cursor = self.conn.cursor()
        cursor.execute(query)
        columns: list[str] = [description[0] for description in cursor.description]
        data: list[Any] = cursor.fetchall()
        cursor.close()
        if return_dataframe:
            return pd.DataFrame(data=data, columns=columns)
        else:
            return columns, data

    def describe_tables(self):
        """"""
        ...

    def get_slakt(aar):
        data = (
            base.query(
                """
                SELECT * FROM slakt
                """
            )
            .groupby(["aar", "orgnr", "dyr"], as_index=False)
            .agg({"antall": "sum", "vekt": "sum"})
            .pivot_table(
                index=["aar", "orgnr"], columns="dyr", values=["antall", "vekt"]
            )
        )
        data.columns = [f"{dyr}_{val}" for val, dyr in data.columns]
        return data


if __name__ == "__main__":
    base = AnalyticsConnection()
    enheter = base.query("SELECT * FROM enheter")
    print(enheter)

    print(base.get_slakt())
