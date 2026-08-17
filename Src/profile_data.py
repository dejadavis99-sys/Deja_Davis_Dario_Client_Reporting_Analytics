import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# LOAD PROCESSED CDC DATA
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "Data"
    / "processed"
    / "cdc_places_processed.csv"
)

print("\n=== LOADING PROCESSED CDC DATA ===")

df = pd.read_csv(DATA_PATH)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")


# ---------------------------------------------------------
# BASIC DATASET INFORMATION
# ---------------------------------------------------------

print("\n=== DATASET OVERVIEW ===")

print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)


# ---------------------------------------------------------
# YEAR COVERAGE
# ---------------------------------------------------------

print("\n=== YEAR COVERAGE ===")

if "year" in df.columns:
    years = sorted(df["year"].dropna().unique())

    print("Years available:", years)
    print("Number of years:", len(years))


# ---------------------------------------------------------
# STATE COVERAGE
# ---------------------------------------------------------

print("\n=== STATE COVERAGE ===")

if "stateabbr" in df.columns:
    states = sorted(df["stateabbr"].dropna().unique())

    print("Number of state/territory abbreviations:", len(states))
    print("States/territories:")
    print(states)


# ---------------------------------------------------------
# LOCATION COVERAGE
# ---------------------------------------------------------

print("\n=== LOCATION COVERAGE ===")

if "locationid" in df.columns:
    print(
        "Unique locations:",
        df["locationid"].nunique()
    )

if "locationname" in df.columns:
    print(
        "Unique location names:",
        df["locationname"].nunique()
    )


# ---------------------------------------------------------
# MEASURE DISTRIBUTION
# ---------------------------------------------------------

print("\n=== RECORDS BY MEASURE ===")

if "measureid" in df.columns:
    measure_counts = (
        df["measureid"]
        .value_counts(dropna=False)
        .sort_index()
    )

    print(measure_counts)


# ---------------------------------------------------------
# CATEGORY DISTRIBUTION
# ---------------------------------------------------------

print("\n=== CATEGORY DISTRIBUTION ===")

if "category" in df.columns:
    print(df["category"].value_counts(dropna=False))


# ---------------------------------------------------------
# DATA VALUE TYPE
# ---------------------------------------------------------

print("\n=== DATA VALUE TYPES ===")

if "data_value_type" in df.columns:
    print(df["data_value_type"].value_counts(dropna=False))


# ---------------------------------------------------------
# MISSING VALUES
# ---------------------------------------------------------

print("\n=== MISSING VALUES ===")

missing = (
    df.isna()
    .sum()
    .sort_values(ascending=False)
)

missing_percent = (
    df.isna()
    .mean()
    .mul(100)
    .round(2)
)

missing_summary = pd.DataFrame(
    {
        "missing_count": missing,
        "missing_percent": missing_percent
    }
)

print(missing_summary)


