from pathlib import Path
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "Src"

PIPELINE_STEPS = [
    "cdc_pipeline.py",
    "profile_data.py",
    "synthetic_cohort.py",
    "synthetic_analysis.py",
    "client_analysis.py",
    "clinical_outcomes.py",
    "visualizations.py",
    "clinical_outcomes_visualization.py",
]


def run_script(script_name):
    script_path = SRC_DIR / script_name

    if not script_path.exists():
        raise FileNotFoundError(f"Missing pipeline script: {script_path}")

    print(f"\n=== Running {script_name} ===")

    subprocess.run(
        [sys.executable, str(script_path)],
        check=True,
        cwd=BASE_DIR,
    )


def main():
    print("\n=== DARIO CLIENT REPORTING ANALYTICS ETL ===")

    for script in PIPELINE_STEPS:
        run_script(script)

    print("\n=== ETL WORKFLOW COMPLETE ===")


if __name__ == "__main__":
    main()