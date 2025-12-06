import pandas as pd
import glob
import os
import numpy as np
import re

DATA_DIR = "data/m3_batch_runs"
OUT_DIR = "M5_Analysis/sensitivity"
os.makedirs(OUT_DIR, exist_ok=True)

files = glob.glob(os.path.join(DATA_DIR, "*.csv"))

records = []

pattern = re.compile(r"run_seed\d+_beds(\d+)_labs(\d+)")

for f in files:
    name = os.path.basename(f)
    match = pattern.search(name)
    if not match:
        continue

    beds = int(match.group(1))
    labs = int(match.group(2))

    df = pd.read_csv(f)
    mean_total = df["total_time"].mean()

    records.append({
        "beds": beds,
        "labs": labs,
        "mean_total_time": mean_total
    })

df_all = pd.DataFrame(records)

# ================================
# BASELINE (5 beds, 1 lab)
# ================================
baseline = df_all[(df_all["beds"] == 5) & (df_all["labs"] == 1)]["mean_total_time"].mean()

results = []

# ================================
# BED SENSITIVITY
# ================================
for b in sorted(df_all["beds"].unique()):
    val = df_all[df_all["beds"] == b]["mean_total_time"].mean()
    pct_input = (b - 5) / 5
    pct_output = (val - baseline) / baseline

    if pct_input != 0:
        sens = pct_output / pct_input
    else:
        sens = 0

    results.append({
        "Parameter": "Beds",
        "Value": b,
        "Mean Total Time": val,
        "%Δ Input": pct_input * 100,
        "%Δ Output": pct_output * 100,
        "Sensitivity Coefficient": sens
    })

# ================================
# LAB SENSITIVITY
# ================================
for l in sorted(df_all["labs"].unique()):
    val = df_all[df_all["labs"] == l]["mean_total_time"].mean()
    pct_input = (l - 1) / 1
    pct_output = (val - baseline) / baseline

    if pct_input != 0:
        sens = pct_output / pct_input
    else:
        sens = 0

    results.append({
        "Parameter": "Labs",
        "Value": l,
        "Mean Total Time": val,
        "%Δ Input": pct_input * 100,
        "%Δ Output": pct_output * 100,
        "Sensitivity Coefficient": sens
    })

final = pd.DataFrame(results)
output_path = os.path.join(OUT_DIR, "m5_sensitivity_coefficients.csv")
final.to_csv(output_path, index=False)

print("Sensitivity coefficients saved to:")
print(output_path)
