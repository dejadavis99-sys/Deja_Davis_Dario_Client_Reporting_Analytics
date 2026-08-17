# Cardiometabolic Client Reporting & Analytics

## Project Overview

This project is an end-to-end analytics and client-reporting product developed for a hypothetical digital-health client review.

The solution uses Python to extract and transform public cardiometabolic data from the CDC PLACES API, validates the resulting analytical dataset, produces business-facing analytical outputs, and prepares those outputs for presentation in a Streamlit application and clinical business review.

The public-data analysis focuses on four cardiometabolic indicators:

- Obesity
- High blood pressure
- Diagnosed diabetes
- No leisure-time physical activity

The goal is not simply to display population-health statistics. The analysis is designed to help a digital-health client understand cardiometabolic burden, identify higher-risk geographic populations, and consider where targeted engagement or intervention strategies may have the greatest value.

---

## Data Source

### CDC PLACES

Public benchmark data are retrieved programmatically from the CDC PLACES API.

The project uses publicly available population-level estimates and does not contain confidential, proprietary, or personally identifiable health information.

The analytical layer retains both crude and age-adjusted prevalence estimates during processing. Age-adjusted prevalence is used as the primary measure for geographic comparisons because it improves comparability across populations with different age distributions.

### Important Data Interpretation

CDC PLACES data are population-level estimates rather than member-level digital-health outcomes.

Therefore:

- Geographic differences should not be interpreted as individual-level effects.
- Associations should not be interpreted as causal relationships.
- The CDC data alone cannot demonstrate that a digital-health intervention caused clinical improvement.
- Public benchmark data and any simulated member-level outcomes used elsewhere in the project are clearly distinguished.

---

## Analytical Questions

The public benchmark analysis addresses three primary questions:

1. Which cardiometabolic risk indicators have the highest prevalence across the analyzed geographies?
2. Which states and local areas show the highest cardiometabolic burden?
3. Is population-level physical inactivity associated with obesity prevalence across states?

These questions support a client discussion about population prioritization and where stronger cardiometabolic engagement strategies may be warranted.

---

## Cardiometabolic Measures

### Obesity
CDC PLACES adult obesity prevalence estimate.

### High Blood Pressure
CDC PLACES prevalence estimate for high blood pressure among adults.

### Diagnosed Diabetes
CDC PLACES prevalence estimate for diagnosed diabetes among adults.

### Physical Inactivity
CDC PLACES prevalence estimate for adults reporting no leisure-time physical activity.

Age-adjusted prevalence is used for the primary cross-geography comparisons.

Clinical definitions, thresholds, and source citations used in the final business review and Streamlit application are documented alongside the corresponding measures.

---

## ETL and Analytical Architecture

The project follows a simple, reproducible workflow:

CDC PLACES API
→ Raw API data
→ Transformation and cleaning
→ Data validation
→ Processed analytical dataset
→ Client analysis
→ Visualizations
→ Streamlit application
→ Clinical business review

### Extraction

The Python ETL layer connects to the public CDC API and retrieves the required cardiometabolic records.

Raw API output is retained locally to support reproducibility.

### Transformation

The transformation layer:

- Selects the four cardiometabolic measures used in the project.
- Retains relevant geography and measure fields.
- Converts analytical fields to appropriate numeric types.
- Preserves both crude and age-adjusted prevalence estimates.
- Produces a processed dataset for downstream reporting.

### Analytical Layer

The analytical layer:

- Selects age-adjusted prevalence for primary geographic comparisons.
- Calculates prevalence summaries by health measure.
- Aggregates results at the state level.
- Identifies higher-burden states and local areas.
- Evaluates the state-level relationship between physical inactivity and obesity.
- Exports reusable client-reporting tables.

---

## Data Quality and Validation

Data quality checks are treated as part of the analytical workflow rather than an afterthought.

The project checks:

- Required columns
- Missing values
- Duplicate records
- Measure coverage
- Geography coverage
- Prevalence methodology
- Numeric conversion
- Expected analytical outputs
- Presence of generated visualization files

The processed dataset contains 23,664 records across four cardiometabolic measures.

The analysis identified 11,832 age-adjusted prevalence records for primary geographic reporting.

A final automated QA script verifies required fields, health-measure availability, age-adjusted records, and expected visualization outputs.

The latest validated run completed with all automated QA checks passing.

---

## Public Benchmark Findings

The population-level benchmark analysis produced the following average age-adjusted prevalence estimates across the analyzed geographic observations:

| Measure | Average Prevalence |
| --- | ---: |
| Obesity | 37.6% |
| High blood pressure | 33.5% |
| No leisure-time physical activity | 27.0% |
| Diagnosed diabetes | 11.2% |

The geographic analysis also identified substantial variation across states and local areas.

Mississippi appeared among the highest-burden states across multiple cardiometabolic measures in the current analysis.

At the state level, physical inactivity and obesity showed a strong positive association (approximately r = 0.83).

This relationship is descriptive and should not be interpreted as evidence that physical inactivity alone causes obesity.

---

## Visualizations

Three primary public-benchmark visualizations were intentionally selected:

1. **Average Age-Adjusted Prevalence by Health Measure**
   - Compares the four cardiometabolic indicators.

2. **Top States by Average Age-Adjusted Obesity Prevalence**
   - Highlights geographic areas with elevated obesity burden.

3. **Physical Inactivity vs. Obesity**
   - Examines the state-level relationship between inactivity and obesity prevalence.

The goal was to use a small number of decision-relevant visuals rather than create charts that did not materially improve the client story.

---

## Streamlit Application

The Streamlit application serves as the interactive reporting layer for the project.

The final application is designed to allow a business stakeholder to:

- Review headline cardiometabolic metrics.
- Understand cohort and denominator definitions.
- Explore relevant segmentation.
- Compare results with public CDC benchmarks.
- Review follow-up coverage and data-quality limitations.
- Understand key findings and recommended actions without reading the underlying Python code.

The Streamlit application is intentionally business-facing rather than a technical data-exploration tool.

---

## Project Structure

```text
Dario-Client-Reporting-Analytics/
│
├── README.md
├── requirements.txt
├── etl.py
├── app.py
├── business_review.md
├── business_review_deck.pptx
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── visualizations/
│
├── src/
│   ├── cdc_pipeline.py
│   ├── profile_data.py
│   ├── analysis_check.py
│   ├── client_analysis.py
│   ├── visualizations.py
│   └── qa_check.py
│
└── ai_transcript/
## Running the Project

1. Create and activate a Python virtual environment.

2. Install project dependencies:
   pip install -r requirements.txt

3. Run the ETL and analytical workflow as needed using the scripts in `src/`.

4. Run the automated QA checks:
   python src/qa_check.py

5. Launch the Streamlit reporting application:
   streamlit run app.py

The application will open locally in a web browser.

Note: The member-level cohort used in this project is synthetic/illustrative and contains no real patient data.