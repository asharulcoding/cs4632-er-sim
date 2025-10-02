import argparse
import numpy as np
import simpy
import sim_config as cfg


def patient(env, name, triage, beds, rng, log):
    t0 = env.now

    # triage
    with triage.request() as req:
        yield req
        triage_start = env.now
        yield env.timeout(rng.exponential(5))   # ~5 min
        triage_end = env.now

    # treatment
    with beds.request() as req:
        yield req
        bed_start = env.now
        yield env.timeout(rng.exponential(60))  # ~60 min
        bed_end = env.now

    log.append({
        "arrival": t0,
        "triage_wait": triage_start - t0,
        "bed_wait": bed_start - triage_end,
        "total_time": bed_end - t0
    })


def arrivals(env, triage, beds, lam, rng, log):
    i = 0
    while True:
        yield env.timeout(rng.exponential(1.0 / lam))
        i += 1
        env.process(patient(env, f"p{i}", triage, beds, rng, log))


def simulate(seed, minutes, lam, triage_cap, bed_cap):
    rng = np.random.default_rng(seed)
    env = simpy.Environment()
    triage = simpy.Resource(env, capacity=triage_cap)
    beds = simpy.Resource(env, capacity=bed_cap)
    log = []
    env.process(arrivals(env, triage, beds, lam, rng, log))
    env.run(until=minutes)
    return log


def summarize(records):
    if not records:
        print("no patients processed")
        return
    n = len(records)
    triage_wait = np.mean([r["triage_wait"] for r in records])
    bed_wait = np.mean([r["bed_wait"] for r in records])
    total = np.mean([r["total_time"] for r in records])
    print("=== RUN SUMMARY ===")
    print(f"Patients processed: {n}")
    print(f"Avg triage wait: {triage_wait:.2f}")
    print(f"Avg bed wait: {bed_wait:.2f}")
    print(f"Avg total time: {total:.2f}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=cfg.SEED)
    p.add_argument("--minutes", type=int, default=cfg.SIM_MINUTES)
    p.add_argument("--lam", type=float, default=cfg.ARRIVAL_LAMBDA)
    p.add_argument("--triage", type=int, default=cfg.TRIAGE_CAPACITY)
    p.add_argument("--beds", type=int, default=cfg.BED_CAPACITY)
    a = p.parse_args()

    rec = simulate(a.seed, a.minutes, a.lam, a.triage, a.beds)
    summarize(rec)
