import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = "data/m3_batch_runs"
OUT_DIR = "M5_Analysis/figures"
os.makedirs(OUT_DIR, exist_ok=True)

files = glob.glob(os.path.join(DATA_DIR, "*.csv"))

all_total_times = []
labels = []

for f in files:
    df = pd.read_csv(f)
    all_total_times.append(df["total_time"].values)
    labels.append(os.path.basename(f).replace(".csv", ""))

# ===============================
# BOXPLOT
# ===============================
plt.figure()
plt.boxplot(all_total_times, showfliers=True)
plt.xticks(rotation=90)
plt.title("M5 Total Time Distribution Across Runs")
plt.xlabel("Run")
plt.ylabel("Total Time (minutes)")
plt.tight_layout()
boxplot_path = os.path.join(OUT_DIR, "m5_total_time_boxplot.png")
plt.savefig(boxplot_path)
plt.close()

# ===============================
# HISTOGRAM (ALL RUNS COMBINED)
# ===============================
combined = [x for run in all_total_times for x in run]

plt.figure()
plt.hist(combined, bins=30)
plt.title("M5 Histogram of Patient Total Time")
plt.xlabel("Total Time (minutes)")
plt.ylabel("Frequency")
plt.tight_layout()
hist_path = os.path.join(OUT_DIR, "m5_total_time_histogram.png")
plt.savefig(hist_path)
plt.close()

print("M5 figures saved:")
print(boxplot_path)
print(hist_path)
