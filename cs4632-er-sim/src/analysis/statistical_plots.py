import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/m4_summary/per_run_summary.csv")

# ------------------------------
# 1. BOXPlot of per-run avg total time
# ------------------------------
plt.figure(figsize=(6, 4))
plt.boxplot(df["avg_total_time"])
plt.ylabel("Average Total Time (min)")
plt.title("Distribution of Per-Run Average Total Time")
plt.tight_layout()
plt.savefig("screenshots/boxplot_per_run_total_time.png")
plt.close()

# ------------------------------
# 2. Histogram of per-run avg total time
# ------------------------------
plt.figure(figsize=(6, 4))
plt.hist(df["avg_total_time"], bins=6)
plt.xlabel("Average Total Time (min)")
plt.ylabel("Frequency")
plt.title("Histogram of Per-Run Average Total Time")
plt.tight_layout()
plt.savefig("screenshots/hist_per_run_total_time.png")
plt.close()

print("Saved boxplot and histogram.")
