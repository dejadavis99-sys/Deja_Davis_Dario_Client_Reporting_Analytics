import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "Data"
    / "processed"
    / "synthetic_clinical_outcomes_summary.csv"
)

VIS_DIR = BASE_DIR / "Data" / "visualizations"
VIS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = (
    VIS_DIR
    / "figure_5_clinical_outcomes.png"
)

# ============================================================
# LOAD SUMMARY
# ============================================================

df = pd.read_csv(DATA_PATH)

print("\n=== CREATING FIGURE 5 ===")

# ============================================================
# CREATE NORMALIZED BASELINE → FOLLOW-UP CHART
#
# Baseline is indexed to 100 so outcomes with different units
# can be compared in one figure without mixing raw scales.
# ============================================================

outcomes = df["outcome"].tolist()

baseline_index = np.repeat(100.0, len(df))

followup_index = (
    df["followup_mean"]
    / df["baseline_mean"]
    * 100
)

x = np.arange(len(outcomes))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))

bars1 = ax.bar(
    x - width / 2,
    baseline_index,
    width,
    label="Baseline"
)

bars2 = ax.bar(
    x + width / 2,
    followup_index,
    width,
    label="~6-Month Follow-Up"
)

# ============================================================
# LABELS
# ============================================================

ax.set_title(
    "Illustrative Clinical Outcomes: Baseline vs. Follow-Up"
)

ax.set_ylabel(
    "Indexed Mean (Baseline = 100)"
)

ax.set_xticks(x)
ax.set_xticklabels(outcomes)

ax.legend()

# Add relative-change labels above follow-up bars
for bar, change in zip(
    bars2,
    df["relative_change_pct"]
):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.4,
        f"{change:.1f}%",
        ha="center",
        va="bottom",
        fontsize=10
    )

# Give labels enough room
ax.set_ylim(0, 106)

# ============================================================
# DISCLOSURE
# ============================================================

fig.text(
    0.5,
    0.01,
    "Synthetic / illustrative member cohort; "
    "n = 463 members with observed follow-up. "
    "Changes are descriptive and do not establish causality.",
    ha="center",
    fontsize=9
)

plt.tight_layout(rect=[0, 0.05, 1, 1])

# ============================================================
# SAVE
# ============================================================

plt.savefig(
    OUTPUT_PATH,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"Figure 5 saved to:\n{OUTPUT_PATH}")
print("=== FIGURE 5 COMPLETE ===")