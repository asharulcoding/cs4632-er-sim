import argparse
import numpy as np
import simpy
from models.arrivals import patient_arrival_process
from models.service_stations import EDResources
from models.triage import triage_and_route
from sim_config import SimConfig

def run(hours: int, seed: int = 42, cfg: SimConfig | None = None):
    rng = np.random.default_rng(seed)
    env = simpy.Environment()
    cfg = cfg or SimConfig.default()
    resources = EDResources(env, cfg)
    env.process(patient_arrival_process(env, rng, resources, cfg, triage_and_route))
    env.run(until=hours * 60)  # minutes
    resources.dump_results()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=int, default=12)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    run(hours=args.hours, seed=args.seed)
