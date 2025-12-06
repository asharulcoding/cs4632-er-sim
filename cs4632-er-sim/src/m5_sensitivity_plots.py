import pandas as pd
import matplotlib.pyplot as plt
import os

# Load M5 sensitivity data
csv_path = "M5_Analysis/sensitivity/m5_sensitivity_coefficients.csv"
df = pd.read_csv(csv_path)

# Output folder
out_dir = "screenshots/m5_sensitivity_charts"
os.makedirs(out_dir, exist_ok=True)

# ===============================
# BEDS SENSITIVITY PLOT
# ===============================
beds_df = df[df["Parameter"] == "Beds"]

plt.figure()
plt.plot(beds_df["Value"], beds_df["Mean Total Time"], marker="o")
plt.xlabel("Number of Beds")
plt.ylabel("Mean Total Time (minutes)")
plt.title("M5 Sensitivity: Beds vs Mean Total Time")
plt.grid(True)
beds_plot = os.path.join(out_dir, "m5_beds_vs_total_time.png")
plt.savefig(beds_plot)
plt.close()

# ===============================
# LABS SENSITIVITY PLOT
# ===============================
labs_df = df[df["Parameter"] == "Labs"]

plt.figure()
plt.plot(labs_df["Value"], labs_df["Mean Total Time"], marker="o")
plt.xlabel("Number of Labs")
plt.ylabel("Mean Total Time (minutes)")
plt.title("M5 Sensitivity: Labs vs Mean Total Time")
plt.grid(True)
labs_plot = os.path.join(out_dir, "m5_labs_vs_total_time.png")
plt.savefig(labs_plot)
plt.close()

print("M5 Sensitivity plots saved:")
print(beds_plot)
print(labs_plot)
