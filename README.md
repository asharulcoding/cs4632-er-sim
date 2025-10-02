# CS4632 — Emergency Room Simulation (ER Sim)

This project is a discrete-event simulation of an emergency room. The goal is to look at how patients move through the ER and how staff/resources are used when things get busy. We’re focusing on triage, queues, and staff schedules to see how changes in setup affect wait times and overall flow.

## Project Status
Currently the basics are working:
- Patients show up randomly (Poisson arrivals).
- They get a severity level (using the 5-level Emergency Severity Index).
- Triage nurses, doctors, and rooms are all modeled as resources with limits.
- The simulation tracks wait times, length of stay, and how busy staff are.
- Results are written to a CSV file.

Still working on:
- Adding shift scheduling (staggered shifts, surge staff, etc.).  
- Modeling labs/imaging and adding their turnaround times.  
- Graphing/visuals with matplotlib.

Planned next:
- Fine-tuning parameters to match more realistic data.  
- Expanding the test cases with pytest.  
- Running experiments with different staffing levels and patient loads.

## Models Used
- **Queueing theory**: Patients are modeled in M/M/c style queues for triage, registration, rooms, and lab/imaging. Emergency cases use priority queues.  
- **Triage system**: Patients are assigned a priority level based on the Emergency Severity Index (five levels). These levels map to priority scheduling in the simulation.  
- **Resource use**: The model allows testing different numbers of nurses, physicians, rooms, and schedules to see how resources affect outcomes.  

## Metrics Collected
- Wait times for each triage level  
- Utilization of nurses, physicians, and rooms  
- Patient throughput and cases where patients leave without being seen  
- Length of stay distribution  
- Service levels (probability that wait times stay under a target value by triage level)  

## How To Run
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/main.py --hours 24 --seed 42
```

## Project Structure
```bash
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
```
## Architecture Overview
- **main.py**: sets up and runs the simulation loop.
- **sim_config.py**: holds parameters (arrival rates, service times, staff numbers).
- **arrivals.py**: handles patient arrivals.
- **triage.py**: assigns severity and simulates triage.
- **service_stations.py**: manages doctors, nurses, and rooms. Tracks metrics.
- **scheduler.py**: placeholder for staff shift scheduling (future).
  
These line up with the UML diagrams (class + activity)

## Running Experiments
Scenarios are defined in src/sim_config.py. By changing the number of staff or the schedule setup, different cases can be tested. Running multiple seeds and comparing results makes it possible to study variation in outcomes.

## Project Management
We are tracking progress using a Github Project Board with "To Do / In Progress / Done" columns. 
- https://github.com/users/AashnaS23/projects/4

## License
MIT
