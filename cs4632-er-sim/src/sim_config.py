from dataclasses import dataclass

@dataclass
class SimConfig:
    triage_service_min: float = 4.0      # minutes
    triage_service_max: float = 8.0
    reg_service_mean: float = 5.0
    md_service_mean: float = 20.0
    nurse_service_mean: float = 12.0
    lab_turnaround_mean: float = 45.0

    arrival_rate_per_hour: float = 15.0  # Poisson arrivals

    n_triage_nurses: int = 2
    n_rns: int = 4
    n_mds: int = 2
    n_rooms: int = 8

    @staticmethod
    def default() -> "SimConfig":
        return SimConfig()
