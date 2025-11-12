import os
import re
import glob
import math
import pandas as pd
import matplotlib.pyplot as plt

# ---------- paths (adjust if yours differ) ----------
DATA_FOLDER = "data/batch_runs_folder"
OUT_FOLDER = "data/m4_summary"
IMG_FOLDER = "screenshots"

os.makedirs(OUT_FOLDER, exist_ok=True)
os.makedirs(IMG_FOLDER, exist_ok=True)

# ---------- helper: parse beds/labs/seed from filename ----------
_fname_re = re.compile(r"seed(?P<seed>\d+)_beds(?P<beds>\d+)_labs(?P<labs>\d+)\.csv$")

def parse_params_from_filename(path):
    name = os.path.basename(path)
    m = _fname_re.search(name)
    if not m:
        return None, None, None
    return int(m.group("seed")), int(m.group("beds")), int(m.group("labs"))

# ---------- collect per-run stats (one CSV == one run, many patients) ----------
rows = []
csv_files = sorted(glob.glob(os.path.join(DATA_FOLDER, "run_*.csv")))
if not csv_files:
    raise SystemExit(f"No CSVs found in {DATA_FOLDER}. Make sure your batch runs are saved there.")

for fp in csv_files:
    seed, beds, labs = parse_params_from_filename(fp)
    if beds is None:
        # skip files that don't follow naming convention
        continue
    df = pd.read_csv(fp)

    # basic columns expected from your sim
    # arrival, triage_wait, bed_wait, lab_time, total_time
    n = len(df)
    avg_total = df["total_time"].mean()
    std_total = df["total_time"].std(ddof=1) if n > 1 else 0.0

    rows.append({
        "file": os.path.basename(fp),
        "seed": seed,
        "beds": beds,
        "labs": labs,
        "n_patients": n,
        "avg_triage_wait": df["triage_wait"].mean(),
        "avg_bed_wait": df["bed_wait"].mean(),
        "avg_lab_time": df["lab_time"].mean(),
        "avg_total_time": avg_total,
        "std_total_time": std_total
    })

per_run = pd.DataFrame(rows).sort_values(["beds", "labs", "seed"]).reset_index(drop=True)
per_run.to_csv(os.path.join(OUT_FOLDER, "per_run_summary.csv"), index=False)
print(f"[saved] {OUT_FOLDER}/per_run_summary.csv")
print(per_run.head(10))

# ---------- aggregate across runs: group by beds and labs ----------
def with_ci(df, value_col):
    g = df.groupby(value_col[0], as_index=False)[value_col[1]].agg(["mean", "std", "count"])
    g = g.reset_index()
    # 95% CI on the mean of per-run means
    g["ci95"] = 1.96 * (g["std"] / g["count"].clip(lower=1).apply(lambda c: math.sqrt(c)))
    return g

beds_agg = with_ci(per_run.rename(columns={"avg_total_time":"value"}), ("beds", "value"))
labs_agg = with_ci(per_run.rename(columns={"avg_total_time":"value"}), ("labs", "value"))

beds_agg.to_csv(os.path.join(OUT_FOLDER, "beds_vs_total_time.csv"), index=False)
labs_agg.to_csv(os.path.join(OUT_FOLDER, "labs_vs_total_time.csv"), index=False)
print(f"[saved] {OUT_FOLDER}/beds_vs_total_time.csv")
print(f"[saved] {OUT_FOLDER}/labs_vs_total_time.csv")

# ---------- plot 1: beds vs avg total time (error bars = 95% CI of per-run means) ----------
plt.figure(figsize=(8,5))
plt.errorbar(beds_agg["beds"], beds_agg["mean"], yerr=beds_agg["ci95"], fmt="o-", capsize=5)
plt.title("Effect of Bed Capacity on Average Total Time")
plt.xlabel("Number of Beds")
plt.ylabel("Average Total Time (minutes)")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(IMG_FOLDER, "beds_vs_total_time.png"), dpi=200)
print(f"[saved] {IMG_FOLDER}/beds_vs_total_time.png")

# ---------- plot 2: labs vs avg total time ----------
plt.figure(figsize=(8,5))
plt.errorbar(labs_agg["labs"], labs_agg["mean"], yerr=labs_agg["ci95"], fmt="o-", capsize=5)
plt.title("Effect of Lab Capacity on Average Total Time")
plt.xlabel("Number of Labs")
plt.ylabel("Average Total Time (minutes)")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(IMG_FOLDER, "labs_vs_total_time.png"), dpi=200)
print(f"[saved] {IMG_FOLDER}/labs_vs_total_time.png")

# ---------- optional: distribution from one run (pick the first) ----------
sample_file = per_run.iloc[0]["file"]
sample_df = pd.read_csv(os.path.join(DATA_FOLDER, sample_file))

plt.figure(figsize=(8,5))
plt.hist(sample_df["total_time"], bins=20)
plt.title(f"Distribution of Total Time (example run: {sample_file})")
plt.xlabel("Total Time (minutes)")
plt.ylabel("Count of Patients")
plt.tight_layout()
plt.savefig(os.path.join(IMG_FOLDER, "total_time_histogram_example.png"), dpi=200)
print(f"[saved] {IMG_FOLDER}/total_time_histogram_example.png")

# ---------- print a small stats block you can paste into the report ----------
overall_mean = per_run["avg_total_time"].mean()
overall_std = per_run["avg_total_time"].std(ddof=1) if len(per_run) > 1 else 0.0
overall_n = len(per_run)
overall_ci95 = 1.96 * (overall_std / math.sqrt(overall_n)) if overall_n > 1 else 0.0

print("\n=== M4 quick stats (across runs) ===")
print(f"Runs: {overall_n}")
print(f"Avg total time (mean of per-run means): {overall_mean:.2f} min")
print(f"Std dev (per-run means): {overall_std:.2f} min")
print(f"95% CI: [{overall_mean - overall_ci95:.2f}, {overall_mean + overall_ci95:.2f}] min")
