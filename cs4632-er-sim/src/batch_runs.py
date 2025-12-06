import os
import subprocess

# Ensure data directory exists
os.makedirs("../data", exist_ok=True)

# ============================
# BASELINE CONFIGURATION
# ============================
baseline = {
    "beds": 5,
    "labs": 1,
    "lam": 0.8,
    "minutes": 720,
    "triage": 1
}

# ============================
# NUMBER OF REPLICATIONS
# ============================
replications = 5
seed_start = 100

# ============================
# SENSITIVITY SWEEPS
# ============================

beds_sweep = [2, 3, 5, 8, 10]
labs_sweep = [1, 2, 5]
lam_sweep = [0.5, 0.8, 1.0, 1.2]

# ============================
# SCENARIO DEFINITIONS (M5)
# ============================

scenarios = [
    {"name": "baseline", "beds": 5, "labs": 1, "lam": 0.8},
    {"name": "high_inflow", "beds": 5, "labs": 1, "lam": 1.2},
    {"name": "low_staffing", "beds": 3, "labs": 1, "lam": 0.8},
    {"name": "high_capacity", "beds": 8, "labs": 3, "lam": 0.8}
]

# ============================
# EXTREME CONDITION TESTING
# ============================

extremes = [
    {"name": "extreme_overload", "beds": 1, "labs": 1, "lam": 2.0},
    {"name": "near_idle", "beds": 5, "labs": 2, "lam": 0.2}
]

# ============================
# RUN FUNCTION
# ============================

def run_experiment(label, beds, labs, lam, minutes, seed):
    csv_name = f"{label}_beds{beds}_labs{labs}_lam{lam}_seed{seed}"

    cmd = [
        "python", "src/main.py",
        "--seed", str(seed),
        "--minutes", str(minutes),
        "--lam", str(lam),
        "--triage", "1",
        "--beds", str(beds),
        "--labs", str(labs)
    ]

    print(f"\n=== Running {csv_name} ===")
    subprocess.run(cmd)


# ============================
# BASELINE REPLICATIONS
# ============================

print("\n=== Running BASELINE Replications ===")
for i in range(replications):
    seed = seed_start + i
    run_experiment(
        "baseline",
        baseline["beds"],
        baseline["labs"],
        baseline["lam"],
        baseline["minutes"],
        seed
    )

# ============================
# BEDS SENSITIVITY
# ============================

print("\n=== Running BEDS Sensitivity Sweep ===")
for beds in beds_sweep:
    for i in range(replications):
        seed = seed_start + 10 + i
        run_experiment(
            "beds_sensitivity",
            beds,
            baseline["labs"],
            baseline["lam"],
            baseline["minutes"],
            seed
        )

# ============================
# LABS SENSITIVITY
# ============================

print("\n=== Running LABS Sensitivity Sweep ===")
for labs in labs_sweep:
    for i in range(replications):
        seed = seed_start + 20 + i
        run_experiment(
            "labs_sensitivity",
            baseline["beds"],
            labs,
            baseline["lam"],
            baseline["minutes"],
            seed
        )

# ============================
# ARRIVAL RATE SENSITIVITY
# ============================

print("\n=== Running ARRIVAL RATE Sensitivity Sweep ===")
for lam in lam_sweep:
    for i in range(replications):
        seed = seed_start + 30 + i
        run_experiment(
            "lam_sensitivity",
            baseline["beds"],
            baseline["labs"],
            lam,
            baseline["minutes"],
            seed
        )

# ============================
# SCENARIO TESTING
# ============================

print("\n=== Running M5 Scenarios ===")
for scenario in scenarios:
    for i in range(replications):
        seed = seed_start + 40 + i
        run_experiment(
            scenario["name"],
            scenario["beds"],
            scenario["labs"],
            scenario["lam"],
            baseline["minutes"],
            seed
        )

# ============================
# EXTREME CONDITION TESTING
# ============================

print("\n=== Running EXTREME Condition Tests ===")
for scenario in extremes:
    for i in range(replications):
        seed = seed_start + 60 + i
        run_experiment(
            scenario["name"],
            scenario["beds"],
            scenario["labs"],
            scenario["lam"],
            baseline["minutes"],
            seed
        )

print("\n=== ALL M5 EXPERIMENTS COMPLETE ===")

