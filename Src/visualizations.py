import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "Data"
    / "processed"
    / "cdc_places_processed.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "Data"
    / "visualizations"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("\n=== LOADING DATA FOR VISUALIZATION ===")

df = pd.read_csv(DATA_PATH)

print(f"Rows loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns)}")


# ============================================================
# FILTER TO AGE-ADJUSTED PREVALENCE
# ============================================================

analysis_df = df[
    df["data_value_type"] == "Age-adjusted prevalence"
].copy()

print(f"Age-adjusted records: {len(analysis_df):,}")


# ============================================================
# CALCULATE AVERAGE PREVALENCE BY MEASURE
# ============================================================

measure_summary = (
    analysis_df
    .groupby(["measureid", "measure"], as_index=False)
    .agg(
        average_prevalence=("data_value", "mean")
    )
)

measure_summary["average_prevalence"] = (
    measure_summary["average_prevalence"].round(2)
)

measure_summary = measure_summary.sort_values(
    "average_prevalence",
    ascending=False
)

print("\n=== AVERAGE PREVALENCE BY MEASURE ===")
print(measure_summary.to_string(index=False))


# ============================================================
# CREATE BAR CHART
# ============================================================

plt.figure(figsize=(10, 6))

bars = plt.bar(
    measure_summary["measureid"],
    measure_summary["average_prevalence"]
)

plt.title(
    "Average Age-Adjusted Prevalence by Health Measure",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Health Measure")
plt.ylabel("Average Prevalence (%)")

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.3
)


# Add value labels above bars
for bar in bars:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.3,
        f"{height:.1f}%",
        ha="center",
        va="bottom"
    )


plt.tight_layout()


# ============================================================
# SAVE CHART
# ============================================================

chart_path = (
    OUTPUT_DIR
    / "average_prevalence_by_measure.png"
)

plt.savefig(
    chart_path,
    dpi=300,
    bbox_inches="tight"
)

print("\n=== VISUALIZATION COMPLETE ===")
print(f"Chart saved to: {chart_path}")

plt.show()


# ============================================================
# FIGURE 2: TOP 10 STATES BY OBESITY PREVALENCE
# ============================================================

obesity_df = df[
    (df["measureid"] == "OBESITY") &
    (df["data_value_type"] == "Age-adjusted prevalence")
].copy()

state_obesity = (
    obesity_df
    .groupby("statedesc", as_index=False)["data_value"]
    .mean()
    .sort_values("data_value", ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))

plt.bar(
    state_obesity["statedesc"],
    state_obesity["data_value"]
)

plt.title("Top 10 States by Average Age-Adjusted Obesity Prevalence")
plt.xlabel("State")
plt.ylabel("Average Prevalence (%)")
plt.xticks(rotation=45, ha="right")

for i, value in enumerate(state_obesity["data_value"]):
    plt.text(
        i,
        value + 0.2,
        f"{value:.1f}%",
        ha="center"
    )

plt.tight_layout()

figure2_path = OUTPUT_DIR / "figure_2_top_states_obesity.png"
plt.savefig(figure2_path, dpi=300, bbox_inches="tight")

print(f"Saved Figure 2 to: {figure2_path}")

plt.show()


# ============================================================
# FIGURE 3: OBESITY VS PHYSICAL INACTIVITY BY STATE
# ============================================================

print("\n=== CREATING FIGURE 3 ===")

# Keep age-adjusted prevalence records only
figure3_df = df[
    df["data_value_type"] == "Age-adjusted prevalence"
].copy()

# Calculate average prevalence for each state and health measure
state_measure_avg = (
    figure3_df
    .groupby(
        ["stateabbr", "statedesc", "measureid"],
        as_index=False
    )["data_value"]
    .mean()
)

# Reshape so OBESITY and LPA become separate columns
state_pivot = (
    state_measure_avg
    .pivot(
        index=["stateabbr", "statedesc"],
        columns="measureid",
        values="data_value"
    )
    .reset_index()
)

# Keep states that have both obesity and physical inactivity values
scatter_df = (
    state_pivot[
        ["stateabbr", "statedesc", "OBESITY", "LPA"]
    ]
    .dropna()
    .copy()
)

print(f"States plotted: {len(scatter_df)}")


# ------------------------------------------------------------
# CREATE SCATTER PLOT
# ------------------------------------------------------------

plt.figure(figsize=(10, 7))

plt.scatter(
    scatter_df["LPA"],
    scatter_df["OBESITY"],
    s=70,
    alpha=0.7
)

plt.title(
    "Relationship Between Physical Inactivity and Obesity Prevalence"
)

plt.xlabel(
    "Average Age-Adjusted Physical Inactivity Prevalence (%)"
)

plt.ylabel(
    "Average Age-Adjusted Obesity Prevalence (%)"
)

plt.grid(
    alpha=0.3
)


# ------------------------------------------------------------
# LABEL TOP 5 OBESITY STATES
# ------------------------------------------------------------

top_obesity_states = (
    scatter_df
    .nlargest(5, "OBESITY")
)

for _, row in top_obesity_states.iterrows():

    plt.annotate(
        row["stateabbr"],
        (
            row["LPA"],
            row["OBESITY"]
        ),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=9
    )


# ------------------------------------------------------------
# ADD TREND LINE
# ------------------------------------------------------------

import numpy as np

x = scatter_df["LPA"]
y = scatter_df["OBESITY"]

slope, intercept = np.polyfit(
    x,
    y,
    1
)

trend_y = slope * x + intercept

plt.plot(
    x,
    trend_y,
    linewidth=2
)


# ------------------------------------------------------------
# CORRELATION
# ------------------------------------------------------------

correlation = x.corr(y)

plt.text(
    0.05,
    0.95,
    f"Correlation: {correlation:.2f}",
    transform=plt.gca().transAxes,
    fontsize=11,
    verticalalignment="top"
)

plt.tight_layout()


# ------------------------------------------------------------
# SAVE FIGURE 3
# ------------------------------------------------------------

figure3_path = (
    OUTPUT_DIR
    / "figure_3_obesity_vs_inactivity.png"
)

plt.savefig(
    figure3_path,
    dpi=300,
    bbox_inches="tight"
)

print(
    f"Saved Figure 3 to: {figure3_path}"
)

# ============================================================
# FIGURE 3: OBESITY VS PHYSICAL INACTIVITY BY STATE
# ============================================================

print("\n=== CREATING FIGURE 3 ===")

# Keep age-adjusted prevalence records only
figure3_df = df[
    df["data_value_type"] == "Age-adjusted prevalence"
].copy()

# Calculate average prevalence for each state and health measure
state_measure_avg = (
    figure3_df
    .groupby(
        ["stateabbr", "statedesc", "measureid"],
        as_index=False
    )["data_value"]
    .mean()
)

# Reshape so OBESITY and LPA become separate columns
state_pivot = (
    state_measure_avg
    .pivot(
        index=["stateabbr", "statedesc"],
        columns="measureid",
        values="data_value"
    )
    .reset_index()
)

# Keep states that have both obesity and physical inactivity values
scatter_df = (
    state_pivot[
        ["stateabbr", "statedesc", "OBESITY", "LPA"]
    ]
    .dropna()
    .copy()
)

print(f"States plotted: {len(scatter_df)}")


# ------------------------------------------------------------
# CREATE SCATTER PLOT
# ------------------------------------------------------------

plt.figure(figsize=(10, 7))

plt.scatter(
    scatter_df["LPA"],
    scatter_df["OBESITY"],
    s=70,
    alpha=0.7
)

plt.title(
    "Relationship Between Physical Inactivity and Obesity Prevalence"
)

plt.xlabel(
    "Average Age-Adjusted Physical Inactivity Prevalence (%)"
)

plt.ylabel(
    "Average Age-Adjusted Obesity Prevalence (%)"
)

plt.grid(
    alpha=0.3
)


# ------------------------------------------------------------
# LABEL TOP 5 OBESITY STATES
# ------------------------------------------------------------

top_obesity_states = (
    scatter_df
    .nlargest(5, "OBESITY")
)

for _, row in top_obesity_states.iterrows():

    plt.annotate(
        row["stateabbr"],
        (
            row["LPA"],
            row["OBESITY"]
        ),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=9
    )


# ------------------------------------------------------------
# ADD TREND LINE
# ------------------------------------------------------------

import numpy as np

x = scatter_df["LPA"]
y = scatter_df["OBESITY"]

slope, intercept = np.polyfit(
    x,
    y,
    1
)

trend_y = slope * x + intercept

plt.plot(
    x,
    trend_y,
    linewidth=2
)


# ------------------------------------------------------------
# CORRELATION
# ------------------------------------------------------------

correlation = x.corr(y)

plt.text(
    0.05,
    0.95,
    f"Correlation: {correlation:.2f}",
    transform=plt.gca().transAxes,
    fontsize=11,
    verticalalignment="top"
)

plt.tight_layout()


# ------------------------------------------------------------
# SAVE FIGURE 3
# ------------------------------------------------------------

figure3_path = (
    OUTPUT_DIR
    / "figure_3_obesity_vs_inactivity.png"
)

plt.savefig(
    figure3_path,
    dpi=300,
    bbox_inches="tight"
)

print(
    f"Saved Figure 3 to: {figure3_path}"
)

# ============================================================
# FIGURE 3: OBESITY VS PHYSICAL INACTIVITY BY STATE
# ============================================================

print("\n=== CREATING FIGURE 3 ===")

# Keep age-adjusted prevalence records only
figure3_df = df[
    df["data_value_type"] == "Age-adjusted prevalence"
].copy()

# Calculate average prevalence for each state and health measure
state_measure_avg = (
    figure3_df
    .groupby(
        ["stateabbr", "statedesc", "measureid"],
        as_index=False
    )["data_value"]
    .mean()
)

# Reshape so OBESITY and LPA become separate columns
state_pivot = (
    state_measure_avg
    .pivot(
        index=["stateabbr", "statedesc"],
        columns="measureid",
        values="data_value"
    )
    .reset_index()
)

# Keep states that have both obesity and physical inactivity values
scatter_df = (
    state_pivot[
        ["stateabbr", "statedesc", "OBESITY", "LPA"]
    ]
    .dropna()
    .copy()
)

print(f"States plotted: {len(scatter_df)}")


# ------------------------------------------------------------
# CREATE SCATTER PLOT
# ------------------------------------------------------------

plt.figure(figsize=(10, 7))

plt.scatter(
    scatter_df["LPA"],
    scatter_df["OBESITY"],
    s=70,
    alpha=0.7
)

plt.title(
    "Relationship Between Physical Inactivity and Obesity Prevalence"
)

plt.xlabel(
    "Average Age-Adjusted Physical Inactivity Prevalence (%)"
)

plt.ylabel(
    "Average Age-Adjusted Obesity Prevalence (%)"
)

plt.grid(
    alpha=0.3
)


# ------------------------------------------------------------
# LABEL TOP 5 OBESITY STATES
# ------------------------------------------------------------

top_obesity_states = (
    scatter_df
    .nlargest(5, "OBESITY")
)

for _, row in top_obesity_states.iterrows():

    plt.annotate(
        row["stateabbr"],
        (
            row["LPA"],
            row["OBESITY"]
        ),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=9
    )


# ------------------------------------------------------------
# ADD TREND LINE
# ------------------------------------------------------------

import numpy as np

x = scatter_df["LPA"]
y = scatter_df["OBESITY"]

slope, intercept = np.polyfit(
    x,
    y,
    1
)

trend_y = slope * x + intercept

plt.plot(
    x,
    trend_y,
    linewidth=2
)


# ------------------------------------------------------------
# CORRELATION
# ------------------------------------------------------------

correlation = x.corr(y)

plt.text(
    0.05,
    0.95,
    f"Correlation: {correlation:.2f}",
    transform=plt.gca().transAxes,
    fontsize=11,
    verticalalignment="top"
)

plt.tight_layout()


# ------------------------------------------------------------
# SAVE FIGURE 3
# ------------------------------------------------------------

figure3_path = (
    OUTPUT_DIR
    / "figure_3_obesity_vs_inactivity.png"
)

plt.savefig(
    figure3_path,
    dpi=300,
    bbox_inches="tight"
)

print(
    f"Saved Figure 3 to: {figure3_path}"
)


# ============================================================
# FIGURE 3: OBESITY VS PHYSICAL INACTIVITY BY STATE
# ============================================================

print("\n=== CREATING FIGURE 3 ===")

# Keep age-adjusted prevalence records only
figure3_df = df[
    df["data_value_type"] == "Age-adjusted prevalence"
].copy()

# Calculate average prevalence for each state and health measure
state_measure_avg = (
    figure3_df
    .groupby(
        ["stateabbr", "statedesc", "measureid"],
        as_index=False
    )["data_value"]
    .mean()
)

# Reshape so OBESITY and LPA become separate columns
state_pivot = (
    state_measure_avg
    .pivot(
        index=["stateabbr", "statedesc"],
        columns="measureid",
        values="data_value"
    )
    .reset_index()
)

# Keep states that have both obesity and physical inactivity values
scatter_df = (
    state_pivot[
        ["stateabbr", "statedesc", "OBESITY", "LPA"]
    ]
    .dropna()
    .copy()
)

print(f"States plotted: {len(scatter_df)}")


# ------------------------------------------------------------
# CREATE SCATTER PLOT
# ------------------------------------------------------------

plt.figure(figsize=(10, 7))

plt.scatter(
    scatter_df["LPA"],
    scatter_df["OBESITY"],
    s=70,
    alpha=0.7
)

plt.title(
    "Relationship Between Physical Inactivity and Obesity Prevalence"
)

plt.xlabel(
    "Average Age-Adjusted Physical Inactivity Prevalence (%)"
)

plt.ylabel(
    "Average Age-Adjusted Obesity Prevalence (%)"
)

plt.grid(
    alpha=0.3
)


# ------------------------------------------------------------
# LABEL TOP 5 OBESITY STATES
# ------------------------------------------------------------

top_obesity_states = (
    scatter_df
    .nlargest(5, "OBESITY")
)

for _, row in top_obesity_states.iterrows():

    plt.annotate(
        row["stateabbr"],
        (
            row["LPA"],
            row["OBESITY"]
        ),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=9
    )


# ------------------------------------------------------------
# ADD TREND LINE
# ------------------------------------------------------------

import numpy as np

x = scatter_df["LPA"]
y = scatter_df["OBESITY"]

slope, intercept = np.polyfit(
    x,
    y,
    1
)

trend_y = slope * x + intercept

plt.plot(
    x,
    trend_y,
    linewidth=2
)


# ------------------------------------------------------------
# CORRELATION
# ------------------------------------------------------------

correlation = x.corr(y)

plt.text(
    0.05,
    0.95,
    f"Correlation: {correlation:.2f}",
    transform=plt.gca().transAxes,
    fontsize=11,
    verticalalignment="top"
)

plt.tight_layout()


# ------------------------------------------------------------
# SAVE FIGURE 3
# ------------------------------------------------------------

figure3_path = (
    OUTPUT_DIR
    / "figure_3_obesity_vs_inactivity.png"
)

plt.savefig(
    figure3_path,
    dpi=300,
    bbox_inches="tight"
)

print(
    f"Saved Figure 3 to: {figure3_path}"
)

plt.show()


# ============================================================
# FIGURE 4: FOLLOW-UP RATE BY ENGAGEMENT TIER
# Synthetic / illustrative member cohort
# ============================================================

synthetic_summary_path = (
    BASE_DIR
    / "Data"
    / "processed"
    / "synthetic_cohort_summary.csv"
)

synthetic_summary = pd.read_csv(synthetic_summary_path)

# Put tiers in logical order
tier_order = ["Low", "Medium", "High"]

synthetic_summary["engagement_tier"] = pd.Categorical(
    synthetic_summary["engagement_tier"],
    categories=tier_order,
    ordered=True
)

synthetic_summary = synthetic_summary.sort_values("engagement_tier")

plt.figure(figsize=(9, 6))

bars = plt.bar(
    synthetic_summary["engagement_tier"],
    synthetic_summary["followup_rate_pct"]
)

plt.title(
    "Follow-Up Rate by Engagement Tier\n"
    "Synthetic / Illustrative Member Cohort"
)

plt.xlabel("Engagement Tier")
plt.ylabel("Follow-Up Rate (%)")
plt.ylim(0, 100)

# Add percentage labels
for bar, value in zip(
    bars,
    synthetic_summary["followup_rate_pct"]
):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 2,
        f"{value:.1f}%",
        ha="center"
    )

plt.tight_layout()

figure4_path = (
    OUTPUT_DIR
    / "figure_4_followup_by_engagement.png"
)

plt.savefig(
    figure4_path,
    dpi=300,
    bbox_inches="tight"
)

print(f"Saved Figure 4 to: {figure4_path}")

plt.show()