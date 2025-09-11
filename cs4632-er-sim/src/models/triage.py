import simpy
import numpy as np

def triage_and_route(env, rng, priority, resources, cfg):
    # Triage service time: uniform
    triage_time = rng.uniform(cfg.triage_service_min, cfg.triage_service_max)
    with resources.triage_nurse.request(priority=priority) as req:
        arrival = env.now
        yield req
        yield env.timeout(triage_time)
        resources.metrics['triage_waits'].append(env.now - arrival)

    # Route to clinician (priority queue)
    yield from resources.see_clinician(env, rng, priority, cfg)
