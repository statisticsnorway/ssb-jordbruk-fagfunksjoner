"""Node struktur"""

import logging
from typing import ClassVar
from pathlib import Path
import re
import pandas as pd

from .data.get_prodtil_codes import YEARS

logger = logging.getLogger(__name__)



class Produksjonstilskudd:

    def __init__(self, years: list[str] | None = None) -> None:
        if not years:
            years = YEARS
        if not isinstance(years, list):
            years = [years]
        for year in years:
            if not re.fullmatch(r"\d{4}", str(year)):
                raise ValueError(f"Invalid year '{year}': must be a 4-digit string")
            self.codes_from_csv(year)
            self.debio_extra_codes(year)


    
    @staticmethod
    def codes_from_csv(year: str):
        # Get the directory of the current file
        current_dir = Path(__file__).parent
        # Build the path to the CSV relative to this file
        csv_path = current_dir / f"data/produksjonstilskudd_koder_{year}.csv"

        # Read CSV
        codes = pd.read_csv(csv_path)
        pattern = re.compile(r"^p\d{3}$", re.IGNORECASE)

        for _, row in codes.iterrows():
            name = row["name"]
            if pattern.match(name):
                Produksjonskode(code=str(row["name"]).lower(), description=row["content"])
    
    def debio_extra_codes(self, year):
        DEBIO_CODES = {
            "tallkode": {
                "description": "",
                "valid_years": [""]
            }
        }
        for key, value in DEBIO_CODES.items():
            
            Produksjonskode(code=, description=)
    




class Produksjonskode:
    

    _registry: ClassVar[list["Produksjonskode"]] = []

    def __init__(self, code, description) -> None:
        self.code = code
        self.description = description
        self.parents = set()
        self.valid_years = set()


        Produksjonskode._registry.append(self)  # Registers itself in the registry
        logger.debug(f"Initialized self: {self}")

    def add_parent(self, parent):
        self.parents.append(parent)
        parent.append(self)
    
    def remove_parent(self, parent):
        self.parents.discard(parent)
        parent.discard(self)


    def __str__(self) -> str:
        return f"{self.code} - {self.description}"

class ProduksjonskodeGruppe:

    def __init__(self, name, description) -> None:
        self.name = name
        self.description = description
        self.parent = set()
        self.children = set()
        self.valid_years = set()

    def add(self, child):
        self.children.add(child)
        child.parents.add(self)

    def remove(self, child):
        self.children.discard(child)
        child.parents.discard(self)
    


Produksjonstilskudd(["2022"])
