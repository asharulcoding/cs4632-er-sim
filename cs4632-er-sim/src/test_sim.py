import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import sim_config as cfg
from main import simulate



def test_sim_runs():
    rec = simulate(cfg.SEED, 60, cfg.ARRIVAL_LAMBDA, 1, 2)
    assert len(rec) > 0


def test_more_beds_reduces_wait():
    r1 = simulate(cfg.SEED, 8 * 60, cfg.ARRIVAL_LAMBDA, 1, 2)
    r2 = simulate(cfg.SEED, 8 * 60, cfg.ARRIVAL_LAMBDA, 1, 8)

    avg1 = sum(x["bed_wait"] for x in r1) / len(r1)
    avg2 = sum(x["bed_wait"] for x in r2) / len(r2)

    assert avg2 < avg1

