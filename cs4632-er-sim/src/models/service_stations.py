import simpy
import numpy as np
import csv

class PriorityResource(simpy.PriorityResource):
    pass

class EDResources:
    def __init__(self, env, cfg):
        self.env = env
        self.triage_nurse = PriorityResource(env, capacity=cfg.n_triage_nurses)
        self.md = PriorityResource(env, capacity=cfg.n_mds)
        self.rn = PriorityResource(env, capacity=cfg.n_rns)
        self.rooms = simpy.Resource(env, capacity=cfg.n_rooms)
        self.metrics = {
            'triage_waits': [],
            'md_waits': [],
            'los': []
        }

    def see_clinician(self, env, rng, priority, cfg):
        with self.md.request(priority=priority) as req_md, self.rooms.request() as req_room:
            t0 = env.now
            yield req_md & req_room
            wait = env.now - t0
            self.metrics['md_waits'].append(wait)
            service = rng.exponential(cfg.md_service_mean)
            yield env.timeout(service)
            self.metrics['los'].append(service + wait)

    def dump_results(self, path='data/results.csv'):
        with open(path, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['metric','value'])
            for x in self.metrics['triage_waits']:
                w.writerow(['triage_wait', x])
            for x in self.metrics['md_waits']:
                w.writerow(['md_wait', x])
            for x in self.metrics['los']:
                w.writerow(['los', x])
