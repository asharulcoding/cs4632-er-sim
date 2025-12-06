import pandas as pd
import glob
import os

data_dir = "data/m3_batch_runs"
out_dir = "M5_Analysis/scenarios"
os.makedirs(out_dir, exist_ok=True)

scenario_groups = {
    "baseline": "*beds5_labs1*.csv",
    "high_inflow": "*lam1.2*.csv",
    "low_staffing": "*beds3_labs1*.csv",
    "high_capacity": "*beds8_labs3*.csv"
}

rows = []

for name, pattern in scenario_groups.items():
    files = glob.glob(os.path.join(data_dir, pattern))

    total = []
    triage = []
    bed = []

    for f in files:
        df = pd.read_csv(f)
        total.extend(df["total_time"])
        triage.extend(df["triage_wait"])
        bed.extend(df["bed_wait"])

    if total:
        rows.append({
            "Scenario": name,
            "Mean Total Time": sum(total) / len(total),
            "Mean Triage Wait": sum(triage) / len(triage),
            "Mean Bed Wait": sum(bed) / len(bed),
            "Patients": len(total)
        })

summary = pd.DataFrame(rows)
summary_path = os.path.join(out_dir, "m5_scenario_statistical_summary.csv")
summary.to_csv(summary_path, index=False)

print("Scenario summary created at:")
print(summary_path)
