import logging
from functools import lru_cache

import pandas as pd

logger = logging.getLogger(__name__) # Make sure it logs everything needed to figure out what was being done.

class AnalyticsConnection:

    path_to_database: str = "work/analytics.sqlite"
    connection = ...
    most_recent_query: str | None = None

    def __init__(self) -> None:
        ...
    
    def test_connection():
        ...

    def connect():
        ...
    
    @lru_cache(maxsize=1)
    def query(query, return_dataframe = True) -> pd.DataFrame | tuple[...]:
        logger.info(f"Running query:\n{query}")
        self.most_recent_query = query
        if return_dataframe:
            return pd.DataFrame()
        else:
            return columns, data
        
    def multiple_queries(*args) -> pd.DataFrame:
        data = pd.DataFrame
        for query in *args:
            data.merge(self.query(query))
        return data

    
    def describe_tables():
        """"""
        ... 

    def get_all_data():
        ...
    