# Cardiometabolic Client Reporting & Analytics
## Clinical Business Review

**Prepared by:** Deja Davis  
**Stakeholders:** VP of Clinical Operations and Client Success Leadership  
**Reporting Period:** Baseline to approximately 6-month follow-up

---

## Executive Summary

The analysis indicates favorable directional change across four cardiometabolic outcomes among members with observed follow-up. Weight, BMI, systolic blood pressure, and HbA1c all decreased from baseline to approximately six-month follow-up. These findings support continued focus on member engagement and follow-up completion while using clinical outcome trends to identify opportunities for targeted client reporting and program improvement.

The recommended next step is to strengthen follow-up coverage and recurring outcome reporting, with particular attention to engagement segments where completion or improvement is weaker. Because the member-level cohort is synthetic/illustrative and the analysis does not include a randomized or matched control group, the observed changes should be interpreted as descriptive program-performance signals rather than causal estimates of program impact.

---

## Cohort and Measurement Approach

The illustrative member cohort contains **600 enrolled members**. Of these members, **463 have observed follow-up measurements**, resulting in **77.2% follow-up coverage** and approximately **22.8% without observed follow-up**.

The primary outcome analysis therefore uses a **completer denominator of N = 463** rather than the full enrolled population. Enrollment counts describe overall program reach, while follow-up outcome metrics describe members for whom both baseline and follow-up information is available.

This distinction is important because completer-only results may differ from outcomes for the entire enrolled population. Members who remain engaged and complete follow-up may systematically differ from those without follow-up.

---

## Cardiometabolic Outcomes

Among the 463 members with observed follow-up, all four selected cardiometabolic measures improved directionally over the approximately six-month observation period.

| Outcome | Baseline | Follow-Up | Absolute Change | Relative Change | N |
|---|---:|---:|---:|---:|---:|
| Weight (kg) | 97.48 | 94.08 | -3.41 kg | -3.49% | 463 |
| BMI | 33.90 | 32.71 | -1.19 | -3.51% | 463 |
| Systolic BP (mmHg) | 136.96 | 132.22 | -4.74 mmHg | -3.46% | 463 |
| HbA1c (%) | 6.75 | 6.47 | -0.28 percentage points | -4.20% | 463 |

The largest relative improvement among the four reported outcomes was observed for **HbA1c (-4.20%)**, followed by BMI, weight, and systolic blood pressure. The direction of change is consistent across measures, providing a useful signal for ongoing cardiometabolic reporting.

However, these changes should not be interpreted as proof that program participation caused the improvements. The appropriate comparison is each observed completer's baseline measurement versus follow-up measurement.

---

## Engagement and Segmentation

Engagement provides an important lens for interpreting the outcome results. The analysis evaluates follow-up and outcome patterns across engagement segments to determine whether performance is consistent across the member population.

The segmentation indicates that engagement level is meaningfully related to the pattern of observed outcomes and/or follow-up. This supports using engagement as an operational segmentation variable rather than relying exclusively on overall averages.

From a client-reporting perspective, this segmentation can help identify groups that may benefit from additional outreach and can help distinguish strong aggregate results from areas where follow-up or outcome performance warrants additional attention.

---

## External Population-Health Context

Public CDC PLACES data was incorporated to provide external population-health and geographic context. Across the four analyzed population-health measures, **obesity had the highest average prevalence (37.63%)**, followed by **high blood pressure (33.54%)** and **physical inactivity (27.02%)**.

These external data can help identify populations or geographic areas where cardiometabolic burden may be elevated and therefore where additional program attention could be considered.

The CDC data are **not a control group** for the synthetic member cohort. Differences in population, geography, measurement methodology, timing, and risk composition limit direct comparison. External population-health measures should therefore be used to inform prioritization and contextual interpretation—not to attribute member-level outcomes to the program.

---

## Recommended Actions

### 1. Improve follow-up completion

**Metric:** Follow-up coverage  
**Current performance:** 463 of 600 members, or 77.2%

Establish recurring monitoring of missing follow-up and implement targeted outreach for members approaching the expected follow-up window. Increasing follow-up coverage would strengthen the representativeness and reliability of subsequent client outcome reporting.

### 2. Use engagement segmentation to target intervention

**Metrics:** Follow-up coverage and cardiometabolic outcome change by engagement segment

Track outcomes and completion longitudinally by engagement level. Where lower-engagement groups demonstrate weaker follow-up or outcome performance, prioritize outreach, re-engagement strategies, or other operational interventions.

### 3. Establish recurring cardiometabolic reporting

**Metrics:** Weight, BMI, systolic blood pressure, HbA1c, enrollment, engagement, follow-up coverage, and missingness

Develop a consistent reporting cadence that distinguishes enrolled members from outcome completers and tracks baseline-to-follow-up change over time. Where clinically appropriate thresholds are defined, future reporting should also include the proportion of members meeting those thresholds rather than relying solely on mean change.

---

## Interpretation and Limitations

The results are descriptive and should be interpreted with several limitations in mind:

- The member-level cohort is **synthetic/illustrative and does not contain real patient data**.
- The analysis does not include a randomized, matched, or otherwise comparable control group.
- Members with follow-up may differ systematically from members without follow-up, creating potential **self-selection and loss-to-follow-up bias**.
- Observed changes may reflect factors outside the program, including differences in baseline risk, treatment, behavior, or other unmeasured characteristics.
- Aggregate averages may obscure meaningful differences between member subgroups.
- External CDC population-health data provide context but are not directly comparable member-level outcomes.

Accordingly, the analysis identifies **associations and descriptive trends**, not causal program effects.

---

## Data Provenance

**External population-health data:** CDC PLACES API/public data used for population-level cardiometabolic and geographic context.

**Member-level data:** Synthetic/illustrative cohort generated solely for this analytical demonstration. It contains no real patient data.

**Processed outputs:** Derived through the Python ETL and analytical workflow included in the accompanying repository.

**Dashboard and figures:** Generated from the processed analytical outputs used in the accompanying Streamlit application and client presentation.

All synthetic or illustrative results should remain clearly labeled as such when presented to stakeholders.