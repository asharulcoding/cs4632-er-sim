import os
import subprocess

# Make sure data/ exists
os.makedirs("../data", exist_ok=True)

# Define runs (tweak values as you like)
runs = [
    {"seed": 42, "beds": 2, "labs": 1, "minutes": 480, "lam": 0.8},   # baseline small
    {"seed": 43, "beds": 5, "labs": 1, "minutes": 480, "lam": 0.8},   # baseline medium
    {"seed": 44, "beds": 10, "labs": 1, "minutes": 480, "lam": 0.8},  # more beds
    {"seed": 45, "beds": 5, "labs": 2, "minutes": 480, "lam": 0.8},   # more labs
    {"seed": 46, "beds": 5, "labs": 5, "minutes": 480, "lam": 0.8},   # many labs
    {"seed": 47, "beds": 5, "labs": 1, "minutes": 480, "lam": 1.0},   # higher arrival rate
    {"seed": 48, "beds": 5, "labs": 1, "minutes": 480, "lam": 0.5},   # lower arrival rate
    {"seed": 49, "beds": 3, "labs": 1, "minutes": 480, "lam": 0.8},   # fewer beds
    {"seed": 50, "beds": 8, "labs": 2, "minutes": 480, "lam": 0.8},   # balanced
    {"seed": 51, "beds": 5, "labs": 1, "minutes": 600, "lam": 0.8},   # longer time horizon
]

for i, run in enumerate(runs, start=1):
    cmd = [
        "python", "main.py",
        "--seed", str(run["seed"]),
        "--minutes", str(run["minutes"]),
        "--lam", str(run["lam"]),
        "--triage", "1",  # keep triage fixed for now
        "--beds", str(run["beds"]),
        "--labs", str(run["labs"])
    ]
    print(f"\n=== Running experiment {i}: {cmd} ===")
    subprocess.run(cmd)
