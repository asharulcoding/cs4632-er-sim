import pandas as pd
import glob
import os

scenarios = {
    "baseline": "data/m3_batch_runs/run_seed14*_beds5_labs1.csv",
    "low_staffing": "data/m3_batch_runs/run_seed14*_beds3_labs1.csv",
    "high_capacity": "data/m3_batch_runs/run_seed14*_beds8_labs3.csv",
    "high_inflow": "M5_Analysis/scenarios/high_inflow/run_seed18*_beds5_labs1.csv"
}

output_dir = "M5_Analysis/scenarios"
os.makedirs(output_dir, exist_ok=True)

rows = []

for name, pattern in scenarios.items():
    files = sorted(glob.glob(pattern))

    all_data = []
    for f in files:
        df = pd.read_csv(f)
        all_data.append(df)

    combined = pd.concat(all_data)

    rows.append({
        "Scenario": name,
        "Mean Total Time": combined["total_time"].mean(),
        "Mean Triage Wait": combined["triage_wait"].mean(),
        "Mean Bed Wait": combined["bed_wait"].mean(),
        "Patients": len(combined)
    })

summary_df = pd.DataFrame(rows)
summary_path = os.path.join(output_dir, "m5_scenario_statistical_summary.csv")
summary_df.to_csv(summary_path, index=False)

print("Scenario summary created at:")
print(summary_path)

0

