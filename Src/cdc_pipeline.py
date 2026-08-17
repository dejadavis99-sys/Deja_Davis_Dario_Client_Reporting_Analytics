import requests
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

API_URL = "https://data.cdc.gov/resource/swc5-untb.json"

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "Data" / "raw"
PROCESSED_DIR = BASE_DIR / "Data" / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# EXTRACT
# --------------------------------------------------

def extract_cdc_data(limit=50000):
    """
    Extract selected cardiometabolic measures
    from the CDC PLACES public API.
    """

    print("Extracting CDC cardiometabolic data...")

    target_measure_ids = [
        "DIABETES",
        "OBESITY",
        "BPHIGH",
        "LPA"
    ]

    measure_filter = ",".join(
        f"'{measure}'" for measure in target_measure_ids
    )

    params = {
        "$limit": limit,
        "$where": f"measureid in ({measure_filter})"
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data)

    print(f"Successfully extracted {len(df):,} records.")
    print(f"Columns returned: {len(df.columns)}")

    return df


# --------------------------------------------------
# TRANSFORM
# --------------------------------------------------

def transform_cdc_data(df):
    """
    Filter and clean CDC PLACES data for
    cardiometabolic reporting.
    """

    print("\nTransforming CDC data...")

    target_measure_ids = [
        "DIABETES",
        "OBESITY",
        "BPHIGH",
        "LPA"
    ]

    filtered_df = df[
        df["measureid"].isin(target_measure_ids)
    ].copy()

    keep_columns = [
        "year",
        "stateabbr",
        "statedesc",
        "locationname",
        "locationid",
        "category",
        "measure",
        "measureid",
        "data_value_unit",
        "data_value_type",
        "data_value",
        "low_confidence_limit",
        "high_confidence_limit",
        "totalpopulation",
        "totalpop18plus"
    ]

    available_columns = [
        column
        for column in keep_columns
        if column in filtered_df.columns
    ]

    filtered_df = filtered_df[available_columns]

    numeric_columns = [
        "data_value",
        "low_confidence_limit",
        "high_confidence_limit",
        "totalpopulation",
        "totalpop18plus"
    ]

    for column in numeric_columns:
        if column in filtered_df.columns:
            filtered_df[column] = pd.to_numeric(
                filtered_df[column],
                errors="coerce"
            )

    print(f"Records after filtering: {len(filtered_df):,}")

    if "measureid" in filtered_df.columns:
        measures_retained = sorted(
            filtered_df["measureid"]
            .dropna()
            .unique()
        )

        print("Measures retained:", measures_retained)

    return filtered_df


# --------------------------------------------------
# VALIDATE
# --------------------------------------------------

def validate_data(df):
    """
    Perform basic validation checks on the processed CDC data.
    """

    print("\nValidating processed data...")

    if df.empty:
        raise ValueError("Processed dataset is empty.")

    required_columns = [
        "year",
        "stateabbr",
        "locationname",
        "measure",
        "measureid",
        "data_value"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    print(f"Validation passed.")
    print(f"Processed rows: {len(df):,}")
    print(f"Processed columns: {len(df.columns)}")


# --------------------------------------------------
# SAVE
# --------------------------------------------------

def save_data(raw_df, processed_df):
    """
    Save raw and processed CDC data as CSV files.
    """

    print("\nSaving data...")

    raw_file = RAW_DIR / "cdc_places_raw.csv"
    processed_file = PROCESSED_DIR / "cdc_places_processed.csv"

    raw_df.to_csv(
        raw_file,
        index=False
    )

    processed_df.to_csv(
        processed_file,
        index=False
    )

    print(f"Raw data saved to: {raw_file}")
    print(f"Processed data saved to: {processed_file}")


# --------------------------------------------------
# PIPELINE TEST
# --------------------------------------------------

if __name__ == "__main__":

    raw_df = extract_cdc_data()

    processed_df = transform_cdc_data(raw_df)

    validate_data(processed_df)

    save_data(
        raw_df,
        processed_df
        )

print("\n--- FINAL PIPELINE SUMMARY ---")
print(processed_df.head())

print("\nPipeline completed successfully.")


def save_data(raw_df, processed_df):
    """
    Save raw API data and processed analytical data locally.
    """

    raw_path = RAW_DIR / "cdc_places_raw.csv"
    processed_path = PROCESSED_DIR / "cdc_cardiometabolic_processed.csv"

    raw_df.to_csv(raw_path, index=False)
    processed_df.to_csv(processed_path, index=False)

    print(f"\nRaw data saved to: {raw_path}")
    print(f"Processed data saved to: {processed_path}")


def validate_data(df):
    """
    Run basic data-quality checks on the processed dataset.
    """

    print("\nRunning data-quality checks...")

    expected_measures = {
        "DIABETES",
        "OBESITY",
        "BPHIGH",
        "LPA"
    }

    actual_measures = set(
        df["measureid"]
        .dropna()
        .unique()
    )

    missing_measures = expected_measures - actual_measures

    print(f"Processed rows: {len(df):,}")
    print(f"Duplicate rows: {df.duplicated().sum():,}")
    print(
        f"Missing data values: "
        f"{df['data_value'].isna().sum():,}"
    )

    if missing_measures:
        raise ValueError(
            f"Expected measures missing: {missing_measures}"
        )

    if df["data_value"].dropna().between(0, 100).all():
        print("Prevalence values are within expected 0–100% range.")
    else:
        raise ValueError(
            "Unexpected prevalence value detected."
        )

    print("Required cardiometabolic measures are present.")
    print("Validation completed successfully.") 


      


  