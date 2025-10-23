import argparse
from sim_config import SimConfig
import numpy as np
import simpy
import pandas as pd
import sim_config as cfg
from models.scheduler import StaffScheduler
from models.labs import LabImaging


def patient(env, name, triage, beds, labs, rng, log):
    t0 = env.now

    # triage
    with triage.resource.request() as req:
        yield req
        triage_start = env.now
        yield env.timeout(rng.exponential(5))  # ~5 min
        triage_end = env.now

    # treatment (bed)
    with beds.resource.request() as req:
        yield req
        bed_start = env.now
        yield env.timeout(rng.exponential(60))  # ~60 min
        bed_end = env.now

    # labs/imaging (optional step, e.g. 50% of patients need it)
    lab_start = None
    lab_end = None
    if rng.random() < 0.5:  # 50% chance patient needs labs
        with labs.resource.request() as req:
            yield req
            lab_start = env.now
            yield from labs.process(env, rng)
            lab_end = env.now

    log.append({
        "arrival": t0,
        "triage_wait": triage_start - t0,
        "bed_wait": bed_start - triage_end,
        "lab_time": (lab_end - lab_start) if lab_end else 0,
        "total_time": (lab_end if lab_end else bed_end) - t0
    })


def arrivals(env, triage_scheduler, beds_scheduler, labs, lam, rng, log):
    i = 0
    while True:
        yield env.timeout(rng.exponential(1.0 / lam))
        i += 1
        env.process(patient(env, f"p{i}", triage_scheduler, beds_scheduler, labs, rng, log))


def simulate(seed, minutes, lam, triage_cap, bed_cap, lab_cap=1):
    rng = np.random.default_rng(seed)
    env = simpy.Environment()

    triage_scheduler = StaffScheduler(env, triage_cap, [
        (0, 720, triage_cap),
        (720, 1080, triage_cap - 1)
    ])
    beds_scheduler = StaffScheduler(env, bed_cap, [
        (0, 720, bed_cap // 2),
        (720, 1440, bed_cap)
    ])
    labs = LabImaging(env, lab_cap)

    log = []
    env.process(arrivals(env, triage_scheduler, beds_scheduler, labs, lam, rng, log))
    env.run(until=minutes)
    return log


def summarize(records):
    if not records:
        print("no patients processed")
        return
    n = len(records)
    triage_wait = np.mean([r["triage_wait"] for r in records])
    bed_wait = np.mean([r["bed_wait"] for r in records])
    lab_time = np.mean([r["lab_time"] for r in records if r["lab_time"] > 0]) if any(r["lab_time"] > 0 for r in records) else 0
    total = np.mean([r["total_time"] for r in records])
    print("=== RUN SUMMARY ===")
    print(f"Patients processed: {n}")
    print(f"Avg triage wait: {triage_wait:.2f}")
    print(f"Avg bed wait: {bed_wait:.2f}")
    print(f"Avg lab time: {lab_time:.2f}")
    print(f"Avg total time: {total:.2f}")


def save_results(records, filename="data/results_with_labs.csv"):
    """Save simulation records to CSV for later analysis."""
    df = pd.DataFrame(records)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--minutes", type=int, default=8*60)
    p.add_argument("--lam", type=float, default=0.8)
    p.add_argument("--triage", type=int, default=1)
    p.add_argument("--beds", type=int, default=5)
    p.add_argument("--labs", type=int, default=1)
    args = p.parse_args()

    # === Validation ===
    problems = []
    if args.minutes <= 0:
        problems.append("minutes must be > 0")
    if args.lam <= 0:
        problems.append("arrival rate (lam) must be > 0")
    if args.triage <= 0:
        problems.append("triage capacity must be > 0")
    if args.beds <= 0:
        problems.append("bed capacity must be > 0")
    if args.labs <= 0:
        problems.append("labs capacity must be > 0")

    if problems:
        raise ValueError("Invalid config: " + "; ".join(problems))

    # === Run Simulation ===
    rec = simulate(args.seed, args.minutes, args.lam, args.triage, args.beds, args.labs)
    summarize(rec)

    # === Save Results ===
    import os
    os.makedirs("data/m3_batch_runs", exist_ok=True)

    filename = f"data/m3_batch_runs/run_seed{args.seed}_beds{args.beds}_labs{args.labs}.csv"
