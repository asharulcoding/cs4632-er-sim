# CS4632 — Emergency Room Simulation (ER Sim)

This project is a discrete-event simulation of an emergency department. It focuses on patient triage, queues, resource use, and staff schedules. The goal is to study how changes in staffing or capacity affect wait times and overall flow.

## Models used
- **Queueing theory**: Patients are modeled in M/M/c style queues for triage, registration, rooms, and lab/imaging. Emergency cases use priority queues.  
- **Triage system**: Patients are assigned a priority level based on the Emergency Severity Index (five levels). These levels map to priority scheduling in the simulation.  
- **Resource use**: The model allows testing different numbers of nurses, physicians, rooms, and schedules to see how resources affect outcomes.  

## Metrics collected
- Wait times for each triage level  
- Utilization of nurses, physicians, and rooms  
- Patient throughput and cases where patients leave without being seen  
- Length of stay distribution  
- Service levels (probability that wait times stay under a target value by triage level)  

## How to run 
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/main.py --hours 24 --seed 42

##Project structure
cs4632-er-sim/
├─ src/
│  ├─ main.py
│  ├─ sim_config.py
│  └─ models/
│     ├─ arrivals.py
│     ├─ triage.py
│     ├─ service_stations.py
│     └─ scheduler.py
├─ data/           # output CSVs and configs
├─ docs/           # figures for the report
├─ uml/            # UML diagrams
├─ tests/          # pytest files
├─ refs.bib        # bibliography
├─ requirements.txt
├─ .gitignore
└─ README.md

## Running experiments
Scenarios are defined in src/sim_config.py. By changing the number of staff or the schedule setup, different cases can be tested. Running multiple seeds and comparing results makes it possible to study variation in outcomes.
## License
MIT
