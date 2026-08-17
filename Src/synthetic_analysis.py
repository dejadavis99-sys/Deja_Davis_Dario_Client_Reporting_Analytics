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
    / "synthetic_cohort_summary.csv"
)

# ============================================================
# LOAD SYNTHETIC MEMBER DATA
# ============================================================

df = pd.read_csv(DATA_PATH)

print("\n=== SYNTHETIC COHORT CLIENT ANALYSIS ===")
print("Synthetic / illustrative data — not real patient data")

print(f"\nTotal enrolled members: {len(df):,}")

# ============================================================
# FOLLOW-UP COVERAGE
# ============================================================

followup_count = df["has_followup"].sum()
followup_rate = df["has_followup"].mean() * 100

print(f"Members with follow-up: {followup_count:,}")
print(f"Follow-up coverage: {followup_rate:.1f}%")

# ============================================================
# ENGAGEMENT TIER SUMMARY
# ============================================================

engagement_summary = (
    df.groupby("engagement_tier")
    .agg(
        enrolled_members=("member_id", "count"),
        members_with_followup=("has_followup", "sum")
    )
    .reset_index()
)

engagement_summary["followup_rate_pct"] = (
    engagement_summary["members_with_followup"]
    / engagement_summary["enrolled_members"]
    * 100
)

print("\n=== ENGAGEMENT TIER SUMMARY ===")
print(engagement_summary.to_string(index=False))

# ============================================================
# SAVE CLIENT-READY SUMMARY
# ============================================================

engagement_summary.to_csv(OUTPUT_PATH, index=False)

print("\n=== ANALYSIS COMPLETE ===")
print(f"Saved summary to:\n{OUTPUT_PATH}")