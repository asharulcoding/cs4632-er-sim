import argparse
import numpy as np
import simpy
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
