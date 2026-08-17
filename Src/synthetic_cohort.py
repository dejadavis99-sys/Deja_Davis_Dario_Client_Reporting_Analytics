import numpy as np
import pandas as pd
from pathlib import Path


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "Data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = OUTPUT_DIR / "synthetic_member_cohort.csv"


# ============================================================
# SETTINGS
# ============================================================

np.random.seed(42)

N_MEMBERS = 600


# ============================================================
# CREATE SYNTHETIC MEMBER COHORT
# ============================================================

member_id = [f"M{i:04d}" for i in range(1, N_MEMBERS + 1)]

age = np.random.randint(25, 66, N_MEMBERS)

engagement_tier = np.random.choice(
    ["Low", "Medium", "High"],
    size=N_MEMBERS,
    p=[0.30, 0.40, 0.30]
)

baseline_weight_kg = np.random.normal(
    loc=96,
    scale=16,
    size=N_MEMBERS
).round(1)

height_m = np.random.normal(
    loc=1.70,
    scale=0.10,
    size=N_MEMBERS
)

baseline_bmi = (
    baseline_weight_kg / (height_m ** 2)
).round(1)

baseline_sbp = np.random.normal(
    loc=137,
    scale=14,
    size=N_MEMBERS
).round(1)

baseline_hba1c = np.random.normal(
    loc=6.8,
    scale=1.1,
    size=N_MEMBERS
).round(1)


# ============================================================
# ENGAGEMENT-BASED IMPROVEMENT
# ============================================================

weight_change_map = {
    "Low": -1.0,
    "Medium": -3.0,
    "High": -5.5
}

sbp_change_map = {
    "Low": -1.5,
    "Medium": -4.0,
    "High": -7.0
}

hba1c_change_map = {
    "Low": -0.05,
    "Medium": -0.25,
    "High": -0.50
}


weight_change = np.array([
    weight_change_map[x]
    for x in engagement_tier
]) + np.random.normal(0, 2.0, N_MEMBERS)

sbp_change = np.array([
    sbp_change_map[x]
    for x in engagement_tier
]) + np.random.normal(0, 5.0, N_MEMBERS)

hba1c_change = np.array([
    hba1c_change_map[x]
    for x in engagement_tier
]) + np.random.normal(0, 0.25, N_MEMBERS)


followup_weight_kg = (
    baseline_weight_kg + weight_change
).round(1)

followup_bmi = (
    followup_weight_kg / (height_m ** 2)
).round(1)

followup_sbp = (
    baseline_sbp + sbp_change
).round(1)

followup_hba1c = (
    baseline_hba1c + hba1c_change
).round(1)


# ============================================================
# SIMULATE FOLLOW-UP COVERAGE
# ============================================================

coverage_probability = {
    "Low": 0.58,
    "Medium": 0.78,
    "High": 0.92
}

has_followup = np.array([
    np.random.random() < coverage_probability[x]
    for x in engagement_tier
])

followup_weight_kg[~has_followup] = np.nan
followup_bmi[~has_followup] = np.nan
followup_sbp[~has_followup] = np.nan
followup_hba1c[~has_followup] = np.nan


# ============================================================
# BUILD DATAFRAME
# ============================================================

df = pd.DataFrame({
    "member_id": member_id,
    "age": age,
    "engagement_tier": engagement_tier,
    "baseline_weight_kg": baseline_weight_kg,
    "followup_weight_kg": followup_weight_kg,
    "baseline_bmi": baseline_bmi,
    "followup_bmi": followup_bmi,
    "baseline_sbp": baseline_sbp,
    "followup_sbp": followup_sbp,
    "baseline_hba1c": baseline_hba1c,
    "followup_hba1c": followup_hba1c,
    "has_followup": has_followup,
    "baseline_window": "Enrollment",
    "followup_window": "Approximately 6 months"
})


# ============================================================
# SAVE
# ============================================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\n=== SYNTHETIC MEMBER COHORT ===")
print("SYNTHETIC / ILLUSTRATIVE DATA — NOT REAL PATIENT DATA")

print(f"\nEnrolled members: {len(df):,}")

print(
    f"Members with follow-up: "
    f"{df['has_followup'].sum():,}"
)

coverage = (
    df["has_followup"].mean() * 100
)

print(
    f"Overall follow-up coverage: "
    f"{coverage:.1f}%"
)

print("\nEngagement distribution:")
print(
    df["engagement_tier"]
    .value_counts()
    .sort_index()
)

print("\nSample records:")
print(df.head())

print(
    f"\nSaved synthetic cohort to:\n"
    f"{OUTPUT_PATH}"
)