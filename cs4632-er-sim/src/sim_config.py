# sim_config.py
from dataclasses import dataclass

@dataclass
class SimConfig:
    seed: int = 42
    minutes: int = 8 * 60   # 8 hours
    arrival_lambda: float = 0.8
    triage_capacity: int = 1
    bed_capacity: int = 5
    labs_capacity: int = 1   # new for labs/imaging
