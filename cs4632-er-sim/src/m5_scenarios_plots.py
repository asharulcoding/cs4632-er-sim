import pandas as pd
import matplotlib.pyplot as plt
import os

csv_path = "M5_Analysis/scenarios/m5_scenario_statistical_summary.csv"
df = pd.read_csv(csv_path)

out_dir = "screenshots/m5_scenario_charts"
os.makedirs(out_dir, exist_ok=True)

# ===========================
# TOTAL TIME COMPARISON
# ===========================

plt.figure()
plt.bar(df["Scenario"], df["Mean Total Time"])
plt.title("Mean Total Time by Scenario")
plt.xlabel("Scenario")
plt.ylabel("Mean Total Time (minutes)")
plt.xticks(rotation=45)
plt.tight_layout()
total_time_plot = os.path.join(out_dir, "scenario_total_time_comparison.png")
plt.savefig(total_time_plot)
plt.close()

# ===========================
# BED WAIT COMPARISON
# ===========================

plt.figure()
plt.bar(df["Scenario"], df["Mean Bed Wait"])
plt.title("Mean Bed Wait by Scenario")
plt.xlabel("Scenario")
plt.ylabel("Mean Bed Wait (minutes)")
plt.xticks(rotation=45)
plt.tight_layout()
bed_wait_plot = os.path.join(out_dir, "scenario_bed_wait_comparison.png")
plt.savefig(bed_wait_plot)
plt.close()

print("Scenario comparison charts saved:")
print(total_time_plot)
print(bed_wait_plot)
