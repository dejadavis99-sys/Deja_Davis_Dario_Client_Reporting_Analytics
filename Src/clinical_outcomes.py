import pandas as pd
from pathlib import Path

# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "Data"
    / "processed"
    / "synthetic_member_cohort.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "Data"
    / "processed"
    / "synthetic_clinical_outcomes_summary.csv"
)

# ============================================================
# LOAD SYNTHETIC MEMBER DATA
# ============================================================

df = pd.read_csv(DATA_PATH)

print("\n=== SYNTHETIC CLINICAL OUTCOMES ANALYSIS ===")
print("Synthetic / illustrative data — not real patient data")

# Keep only members with observed follow-up
followup_df = df[df["has_followup"] == True].copy()

print(f"\nTotal enrolled members: {len(df):,}")
print(f"Members with follow-up: {len(followup_df):,}")

# ============================================================
# DEFINE OUTCOMES
# ============================================================

outcomes = {
    "Weight (kg)": (
        "baseline_weight_kg",
        "followup_weight_kg"
    ),
    "BMI": (
        "baseline_bmi",
        "followup_bmi"
    ),
    "Systolic BP (mmHg)": (
        "baseline_sbp",
        "followup_sbp"
    ),
    "HbA1c (%)": (
        "baseline_hba1c",
        "followup_hba1c"
    ),
}

# ============================================================
# CALCULATE SUMMARY
# ============================================================

summary_rows = []

for outcome_name, (baseline_col, followup_col) in outcomes.items():

    analysis_df = followup_df[
        [baseline_col, followup_col]
    ].dropna()

    n = len(analysis_df)

    baseline_mean = analysis_df[baseline_col].mean()
    followup_mean = analysis_df[followup_col].mean()

    absolute_change = followup_mean - baseline_mean

    relative_change_pct = (
        absolute_change / baseline_mean
    ) * 100

    summary_rows.append({
        "outcome": outcome_name,
        "n_with_followup": n,
        "baseline_mean": round(baseline_mean, 2),
        "followup_mean": round(followup_mean, 2),
        "absolute_change": round(absolute_change, 2),
        "relative_change_pct": round(relative_change_pct, 2),
    })

clinical_summary = pd.DataFrame(summary_rows)

# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n=== CLINICAL OUTCOME SUMMARY ===")
print(clinical_summary.to_string(index=False))

# ============================================================
# SAVE RESULTS
# ============================================================

clinical_summary.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n=== ANALYSIS COMPLETE ===")
print(f"Saved summary to:\n{OUTPUT_PATH}")