# CS4632 — Emergency Room Simulation (ER Sim)

A discrete‑event simulation (DES) of a hospital Emergency Department (ED) focused on **patient triage, queueing, resource allocation**, and **staff scheduling** using Python and SimPy.

## Key models
- **Queueing theory**: M/M/c‑style queues for triage, registration, rooms, lab/imaging; priority queues for emergent cases
- **Priority scheduling / triage**: ESI‑inspired 5‑level triage mapped to simulation priorities
- **Resource optimization**: What‑if experiments on number of nurses, physicians, rooms, and shift patterns

## Metrics (logged to CSV)
- Wait times by triage level
- Resource utilization (nurses, physicians, rooms)
- Throughput / LWBS (left‑without‑being‑seen) surrogate
- Length of stay (LOS) distribution
- Service level: P(wait < target) by triage level

## Getting started
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/main.py --hours 24 --seed 42
```

## Project layout
```
cs4632-er-sim/
├─ src/
│  ├─ main.py
│  ├─ sim_config.py
│  └─ models/
│     ├─ arrivals.py
│     ├─ triage.py
│     ├─ service_stations.py
│     └─ scheduler.py
├─ data/                 # CSV outputs, sample configs
├─ docs/                 # Figures for paper
├─ uml/                  # PlantUML diagrams (.puml)
├─ tests/                # Unit tests (pytest)
├─ refs.bib              # Literature sources (≥5)
├─ requirements.txt
├─ .gitignore
└─ README.md
```

## Reproducing experiments
Use `src/sim_config.py` to define scenarios (e.g., different numbers of nurses, staggered shifts, or priority rules). Run multiple seeds and compare CSV outputs.

## License
MIT
