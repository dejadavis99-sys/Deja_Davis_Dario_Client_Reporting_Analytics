import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "Data" / "processed"
VIS_DIR = BASE_DIR / "Data" / "visualizations"

data_path = PROCESSED_DIR / "cdc_places_processed.csv"

print("\n=== FINAL PROJECT QA ===")

# --------------------------------------------------
# CHECK PROCESSED DATA
# --------------------------------------------------

df = pd.read_csv(data_path)

print(f"\nProcessed records: {len(df):,}")

assert len(df) > 0, "Processed dataset is empty."

required_columns = [
    "measureid",
    "measure",
    "data_value",
    "data_value_type",
    "stateabbr",
    "statedesc",
    "locationname",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

assert not missing_columns, (
    f"Missing required columns: {missing_columns}"
)

print("Required columns: PASS")


# --------------------------------------------------
# CHECK DATA VALUES
# --------------------------------------------------

assert df["data_value"].notna().any(), (
    "No valid data values found."
)

assert df["measureid"].nunique() >= 4, (
    "Expected at least four health measures."
)

print("Health measure check: PASS")


# --------------------------------------------------
# CHECK AGE-ADJUSTED RECORDS
# --------------------------------------------------

age_adjusted = df[
    df["data_value_type"] == "Age-adjusted prevalence"
]

assert len(age_adjusted) > 0, (
    "No age-adjusted prevalence records found."
)

print(
    f"Age-adjusted records: {len(age_adjusted):,}"
)

print("Age-adjusted data check: PASS")


# --------------------------------------------------
# CHECK VISUALIZATIONS
# --------------------------------------------------


expected_visuals = [
    "average_prevalence_by_measure.png",
    "figure_2_top_states_obesity.png",
    "figure_3_obesity_vs_inactivity.png",
    "figure_4_followup_by_engagement.png",
]


for filename in expected_visuals:

    path = VIS_DIR / filename

    assert path.exists(), (
        f"Missing visualization: {filename}"
    )

    assert path.stat().st_size > 0, (
        f"Visualization is empty: {filename}"
    )

    print(f"{filename}: PASS")


# ============================================================
# FINAL RESULT
# ============================================================

print("\n================================")
print("ALL QA CHECKS PASSED")
print("================================\n")