import simpy
import numpy as np

def patient_arrival_process(env: simpy.Environment, rng: np.random.Generator, resources, cfg, triage_fn):
    lam = cfg.arrival_rate_per_hour / 60.0  # per minute
    while True:
        # Inter‑arrival ~ Exponential(lam)
        dt = rng.exponential(1/lam)
        yield env.timeout(dt)
        env.process(handle_patient(env, rng, resources, cfg, triage_fn))

def handle_patient(env, rng, resources, cfg, triage_fn):
    # Assign a triage level (ESI‑like) with rough priors
    p = rng.choice([1,2,3,4,5], p=[0.05, 0.15, 0.4, 0.25, 0.15])
    yield from triage_fn(env, rng, p, resources, cfg)
