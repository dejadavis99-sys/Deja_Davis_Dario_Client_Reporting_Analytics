from pathlib import Path

import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Client Reporting & Analytics",
    page_icon="📊",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"
PROCESSED_DIR = DATA_DIR / "processed"
VIS_DIR = DATA_DIR / "visualizations"


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("Client Reporting & Analytics Business Review")

st.caption(
    "Population-health context and synthetic member engagement analysis"
)

st.info(
    "Member-level data in this dashboard are synthetic/illustrative and "
    "do not represent real DarioHealth patient data."
)


# ---------------------------------------------------------
# EXECUTIVE SUMMARY
# ---------------------------------------------------------
st.header("Executive Summary")

st.write(
    """
    This analysis combines public CDC population-health data with a
    separate synthetic member cohort to identify cardiometabolic burden,
    geographic variation, member follow-up patterns, and opportunities
    for targeted client reporting.
    """
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Enrolled Members", "600")
col2.metric("Members With Follow-Up", "463")
col3.metric("Follow-Up Coverage", "77.2%")
col4.metric("Without Follow-Up", "137")


# ---------------------------------------------------------
# POPULATION HEALTH
# ---------------------------------------------------------
st.header("Population Health Landscape")

st.write(
    """
    Across the four analyzed CDC measures, obesity showed the highest
    average prevalence, followed by high blood pressure, physical
    inactivity, and diabetes.
    """
)

p1, p2, p3, p4 = st.columns(4)

p1.metric("Obesity", "37.63%")
p2.metric("High Blood Pressure", "33.54%")
p3.metric("Physical Inactivity", "27.02%")
p4.metric("Diabetes", "11.17%")

population_fig = VIS_DIR / "average_prevalence.png"

if population_fig.exists():
    st.image(
        str(population_fig),
        caption="Average age-adjusted prevalence by health measure",
        use_container_width=True,
    )


# ---------------------------------------------------------
# GEOGRAPHIC OPPORTUNITY
# ---------------------------------------------------------
st.header("Geographic Opportunity")

st.write(
    """
    Geographic variation provides external population-health context
    that may help identify populations warranting greater program
    attention. These estimates should not be interpreted as outcomes
    for the synthetic member cohort.
    """
)

geo_fig = VIS_DIR / "figure_2_top_states.png"

if geo_fig.exists():
    st.image(
        str(geo_fig),
        caption="Geographic variation in population-health burden",
        use_container_width=True,
    )


# ---------------------------------------------------------
# OBESITY VS INACTIVITY
# ---------------------------------------------------------
st.header("Obesity vs. Physical Inactivity")

st.metric("Population-Level Correlation", "r ≈ 0.83")

st.write(
    """
    Higher physical inactivity was strongly associated with higher
    obesity prevalence across the analyzed population data. This is a
    descriptive ecological association and does not establish causality
    or individual-level risk.
    """
)

association_fig = VIS_DIR / "figure_3_obesity_inactivity.png"

if association_fig.exists():
    st.image(
        str(association_fig),
        caption="Relationship between physical inactivity and obesity prevalence",
        use_container_width=True,
    )


# ---------------------------------------------------------
# MEMBER ENGAGEMENT
# ---------------------------------------------------------
st.header("Member Engagement & Follow-Up")

e1, e2, e3 = st.columns(3)

e1.metric("Low Engagement Follow-Up", "60.8%")
e2.metric("Medium Engagement Follow-Up", "78.3%")
e3.metric("High Engagement Follow-Up", "94.2%")

st.write(
    """
    Follow-up coverage increased across engagement segments in the
    synthetic cohort. Lower-engagement members therefore represent the
    clearest illustrative opportunity for proactive outreach and
    continued monitoring.
    """
)

followup_fig = VIS_DIR / "figure_4_followup.png"

if followup_fig.exists():
    st.image(
        str(followup_fig),
        caption="Follow-up rate by engagement tier",
        use_container_width=True,
    )


# ---------------------------------------------------------
# ILLUSTRATIVE CLINICAL OUTCOMES
# ---------------------------------------------------------
st.header("Illustrative Clinical Outcomes")

st.write(
    """
    Among the 463 synthetic members with observed follow-up, descriptive
    baseline-to-follow-up changes were observed across weight, BMI,
    systolic blood pressure, and HbA1c.
    """
)

clinical_fig = VIS_DIR / "figure_5_clinical_outcomes.png"

if clinical_fig.exists():
    st.image(
        str(clinical_fig),
        caption="Illustrative baseline vs. approximately 6-month follow-up",
        use_container_width=True,
    )

clinical_summary = PROCESSED_DIR / "synthetic_clinical_outcomes_summary.csv"

if clinical_summary.exists():
    outcomes = pd.read_csv(clinical_summary)

    with st.expander("View clinical outcome summary data"):
        st.dataframe(outcomes, use_container_width=True)


# ---------------------------------------------------------
# CLIENT OPPORTUNITY
# ---------------------------------------------------------
st.header("Client Opportunities")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Follow-Up Gap")
    st.metric("Members Without Follow-Up", "137")
    st.metric("Missing Follow-Up", "22.8%")

with c2:
    st.subheader("Reporting Implication")
    st.write(
        """
        Client reporting should retain both the enrolled
        intent-to-treat denominator and the follow-up/completer
        population. Reporting only members with observed follow-up
        could overstate performance if missingness differs
        systematically.
        """
    )


# ---------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------
st.header("Recommendations")

r1, r2, r3 = st.columns(3)

with r1:
    st.subheader("1. Target")
    st.write(
        """
        Prioritize lower-engagement members for proactive outreach,
        since this segment demonstrated the lowest illustrative
        follow-up coverage.
        """
    )

with r2:
    st.subheader("2. Monitor")
    st.write(
        """
        Establish recurring reporting for enrollment, engagement,
        follow-up coverage, missingness, and outcomes by segment.
        """
    )

with r3:
    st.subheader("3. Inform")
    st.write(
        """
        Use external population-health and geographic context alongside
        client-specific data to inform program priorities—not as a
        substitute for member-level outcomes.
        """
    )


# ---------------------------------------------------------
# METHODOLOGY & LIMITATIONS
# ---------------------------------------------------------
st.header("Methodology & Limitations")

with st.expander("Methodology"):
    st.write(
        """
        • CDC public API data  
        • Python ETL and validation  
        • Processed analytical datasets  
        • Synthetic member cohort  
        • Automated QA checks  
        • Streamlit reporting
        """
    )

with st.expander("Limitations"):
    st.write(
        """
        • Member cohort is synthetic/illustrative  
        • No real patient data are included  
        • Analysis is descriptive  
        • Follow-up is incomplete  
        • Population-level data cannot establish individual-level effects  
        • Association does not imply causation
        """
    )


# ---------------------------------------------------------
# NEXT STEPS
# ---------------------------------------------------------
st.header("Next Steps")

st.write(
    """
    Apply the reporting framework to validated client data, define
    clinical thresholds and outcomes, track baseline-to-follow-up
    change, compare intent-to-treat and completer results, and monitor
    segment-level performance longitudinally.
    """
)

st.caption(
    "Synthetic/illustrative analysis for client reporting demonstration purposes."
)