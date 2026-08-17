import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "Data"
    / "processed"
    / "cdc_places_processed.csv"
)

df = pd.read_csv(DATA_PATH)


print("\n=== DATA VALUE TYPES ===")
print(df["data_value_type"].value_counts(dropna=False))


print("\n=== MEASURE + VALUE TYPE COUNTS ===")
print(
    df.groupby(
        ["measureid", "data_value_type"]
    )
    .size()
    .reset_index(name="records")
    .to_string(index=False)
)


print("\n=== SAMPLE GEOGRAPHY RECORDS ===")
print(
    df[
        [
            "stateabbr",
            "statedesc",
            "locationname",
            "locationid",
            "measureid",
            "measure",
            "data_value_type",
            "data_value",
        ]
    ]
    .head(20)
    .to_string(index=False)
)