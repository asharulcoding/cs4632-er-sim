import os
import glob
import pandas as pd

INPUT_DIR = "data/m3_batch_runs"
OUTPUT_DIR = "M5_Analysis/summary"
os.makedirs(OUTPUT_DIR, exist_ok=True)

all_files = glob.glob(os.path.join(INPUT_DIR, "*.csv"))

records = []

for file in all_files:
    df = pd.read_csv(file)

    label = os.path.basename(file).replace(".csv", "")

    summary = {
        "run": label,
        "triage_mean": df["triage_wait"].mean(),
        "triage_std": df["triage_wait"].std(),
        "bed_mean": df["bed_wait"].mean(),
        "bed_std": df["bed_wait"].std(),
        "lab_mean": df["lab_time"].mean(),
        "lab_std": df["lab_time"].std(),
        "total_mean": df["total_time"].mean(),
        "total_std": df["total_time"].std()
    }

    records.append(summary)

summary_df = pd.DataFrame(records)
summary_path = os.path.join(OUTPUT_DIR, "m5_statistical_summary.csv")
summary_df.to_csv(summary_path, index=False)

print("M5 Statistical summary saved to:", summary_path)
