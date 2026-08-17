import pandas as pd
from pathlib import Path


# ============================================================
# LOAD PROCESSED CDC DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "Data"
    / "processed"
    / "cdc_places_processed.csv"
)

df = pd.read_csv(DATA_PATH)

print("\n=== CLIENT ANALYSIS ===")
print(f"Total processed records: {len(df):,}")


# ============================================================
# SELECT PRIMARY REPORTING POPULATION
# ============================================================

analysis_df = df[
    df["data_value_type"] == "Age-adjusted prevalence"
].copy()

print(f"Age-adjusted records selected: {len(analysis_df):,}")
print(f"Measures available: {analysis_df['measureid'].nunique()}")

print("\nMeasures:")
print(
    analysis_df[
        ["measureid", "measure"]
    ]
    .drop_duplicates()
    .sort_values("measureid")
    .to_string(index=False)
)


# ============================================================
# KPI SUMMARY BY HEALTH MEASURE
# ============================================================

print("\n=== KPI SUMMARY ===")

kpi_summary = (
    analysis_df
    .groupby(["measureid", "measure"])
    .agg(
        locations=("locationid", "nunique"),
        avg_prevalence=("data_value", "mean"),
        median_prevalence=("data_value", "median"),
        min_prevalence=("data_value", "min"),
        max_prevalence=("data_value", "max"),
    )
    .reset_index()
)

kpi_summary[
    [
        "avg_prevalence",
        "median_prevalence",
        "min_prevalence",
        "max_prevalence",
    ]
] = kpi_summary[
    [
        "avg_prevalence",
        "median_prevalence",
        "min_prevalence",
        "max_prevalence",
    ]
].round(2)

print(kpi_summary.to_string(index=False))


# ============================================================
# STATE-LEVEL PREVALENCE SUMMARY
# ============================================================

print("\n=== STATE-LEVEL PREVALENCE SUMMARY ===")

state_summary = (
    analysis_df
    .groupby(["stateabbr", "statedesc", "measureid", "measure"])
    .agg(
        locations=("locationid", "nunique"),
        avg_prevalence=("data_value", "mean"),
        median_prevalence=("data_value", "median"),
    )
    .reset_index()
)

state_summary[
    ["avg_prevalence", "median_prevalence"]
] = state_summary[
    ["avg_prevalence", "median_prevalence"]
].round(2)

print(
    state_summary
    .sort_values(
        ["measureid", "avg_prevalence"],
        ascending=[True, False]
    )
    .head(20)
    .to_string(index=False)
)


# ============================================================
# TOP 5 STATES BY HEALTH MEASURE
# ============================================================

print("\n=== TOP 5 STATES BY HEALTH MEASURE ===")

top_states = (
    state_summary
    .sort_values(
        ["measureid", "avg_prevalence"],
        ascending=[True, False]
    )
    .groupby("measureid")
    .head(5)
    .reset_index(drop=True)
)

print(
    top_states[
        [
            "measureid",
            "statedesc",
            "locations",
            "avg_prevalence",
            "median_prevalence",
        ]
    ].to_string(index=False)
)


# ============================================================
# TOP 5 INDIVIDUAL LOCATIONS BY HEALTH MEASURE
# ============================================================

print("\n=== TOP 5 INDIVIDUAL LOCATIONS BY HEALTH MEASURE ===")

top_locations = (
    analysis_df
    .sort_values(
        ["measureid", "data_value"],
        ascending=[True, False]
    )
    .groupby("measureid")
    .head(5)
    .reset_index(drop=True)
)

print(
    top_locations[
        [
            "measureid",
            "statedesc",
            "locationname",
            "data_value",
        ]
    ].to_string(index=False)
)


# ============================================================
# EXPORT CLIENT ANALYSIS TABLES
# ============================================================

OUTPUT_DIR = BASE_DIR / "Data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

kpi_path = OUTPUT_DIR / "client_kpi_summary.csv"
state_path = OUTPUT_DIR / "client_state_summary.csv"
top_states_path = OUTPUT_DIR / "client_top_states.csv"
top_locations_path = OUTPUT_DIR / "client_top_locations.csv"

kpi_summary.to_csv(kpi_path, index=False)
state_summary.to_csv(state_path, index=False)
top_states.to_csv(top_states_path, index=False)
top_locations.to_csv(top_locations_path, index=False)

print("\n=== ANALYSIS EXPORT COMPLETE ===")
print(f"Saved: {kpi_path}")
print(f"Saved: {state_path}")
print(f"Saved: {top_states_path}")
print(f"Saved: {top_locations_path}")