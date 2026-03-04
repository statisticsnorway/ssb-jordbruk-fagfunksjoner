import pandas as pd

YEARS = list(range(2017, 2026))

def get_prodtil_codes():
    """Gathers prodtil codes as csv files copied from LDIR's repository."""
    global YEARS
    for year in YEARS:
        df = pd.read_csv(
            f"https://raw.githubusercontent.com/LandbruksdirektoratetGIT/opendata/refs/heads/main/datasets/produksjon-og-avlosertilskudd/{year}/fields.csv"
        )
        df.columns = [c.lower() for c in df.columns]
        expected_columns = ["shortname", "name", "content"]
        assert list(df.columns) == expected_columns, (
            f"Column mismatch!\n"
            f"Current columns: {list(df.columns)}\n"
            f"Expected columns: {expected_columns}"
        )
        df.to_csv(f"produksjonstilskudd_koder_{year}.csv")