import pandas as pd
import glob
import os
import numpy as np
import re

DATA_DIR = "data/m3_batch_runs"
OUT_DIR = "M5_Analysis/scenarios"
os.makedirs(OUT_DIR, exist_ok=True)

files = glob.glob(os.path.join(DATA_DIR, "*.csv"))

scenario_map = {
    "baseline": [],
    "high_inflow": [],
    "low_staffing": [],
    "high_capacity": [],
    "extreme_overload": [],
    "near_idle": []
}

def classify(file):
    name = file.lower()
    for key in scenario_map:
        if key in name:
            return key
    return None

for f in files:
    scenario = classify(f)
    if not scenario:
        continue

    df = pd.read_csv(f)
    scenario_map[scenario].append({
        "patients": len(df),
        "avg_triage": df["triage_wait"].mean(),
        "avg_bed": df["bed_wait"].mean(),
        "avg_lab": df["lab_time"].mean(),
        "avg_total": df["total_time"].mean()
    })

summary_rows = []

for scenario, runs in scenario_map.items():
    if not runs:
        continue

    data = pd.DataFrame(runs)

    summary_rows.append({
        "Scenario": scenario,
        "Mean Patients": data["patients"].mean(),
        "Std Patients": data["patients"].std(),
        "Mean Triage Wait": data["avg_triage"].mean(),
        "Mean Bed Wait": data["avg_bed"].mean(),
        "Mean Lab Time": data["avg_lab"].mean(),
        "Mean Total Time": data["avg_total"].mean()
    })

summary_df = pd.DataFrame(summary_rows)
output_path = os.path.join(OUT_DIR, "m5_scenario_statistical_summary.csv")
summary_df.to_csv(output_path, index=False)

print("Scenario statistical summary saved to:")
print(output_path)
