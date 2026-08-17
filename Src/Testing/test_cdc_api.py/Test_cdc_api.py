import requests
import pandas as pd

API_URL = "https://data.cdc.gov/resource/swc5-untb.json"

params = {
    "$limit": 5
}

response = requests.get(API_URL, params=params, timeout=30)

print("Status code:", response.status_code)

response.raise_for_status()

data = response.json()
df = pd.DataFrame(data)

print("\nRows returned:", len(df))
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head())

print("\n--- COLUMN DETAILS ---")
for column in df.columns:
    print(column)

print("\n--- SAMPLE RECORD ---")
for column, value in df.iloc[0].items():
    print(f"{column}: {value}")

    # Pull a larger sample to inspect available measures
measure_params = {
    "$select": "measure,measureid,category",
    "$limit": 5000
}

measure_response = requests.get(
    API_URL,
    params=measure_params,
    timeout=30
)

measure_response.raise_for_status()

measure_data = measure_response.json()
measure_df = pd.DataFrame(measure_data)

# Remove duplicate measures
unique_measures = (
    measure_df[["measure", "measureid", "category"]]
    .drop_duplicates()
    .sort_values("measure")
)

print("\n--- AVAILABLE CDC MEASURES ---")
print(unique_measures.to_string(index=False))