# CS4632 — Emergency Room Simulation (ER Sim)
**Course:** CS 4632 W01 Fall Semester

**Author(s):** Aashna Suthar, Ash Arul

## Project Overview
This project is a discrete-event simulation of an emergency room. The goal is to look at how patients move through the ER and how staff/resources are used when things get busy. We’re focusing on triage, queues, and staff schedules to see how changes in setup affect wait times and overall flow.

## Project Status - (Milestone 3)
**Done:**  
- Arrivals, triage, beds, staff scheduling, and labs/imaging are working  
- Command-line arguments for parameters (`--beds`, `--labs`, `--minutes`, `--seed`)  
- Validation added so values can’t be negative  
- Results save automatically into CSVs with clear names  
- Batch runs script added for 10+ experiments  
- Tests written with pytest (all passing)  

**Data collected:**  
- Patient arrivals  
- Triage wait  
- Bed wait  
- Lab time  
- Total time  

**Still improving later:**  
- More graphs/plots with matplotlib  
- More test cases  

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

## Installation Instructions
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
## Usage Instructions
To run the simulation:

**Default Run (8 hours)**:
```bash
python src/main.py --beds 5 --labs 1 --minutes 480 --seed 42
```
**24-hour Run (24 hours)**:
```bash
python src/main.py --beds 5 --labs 1 --minutes 1440 --seed 42
```
**Arguments**:
- (--beds) = number of beds (default 5)
- (--labs) = number of lab stations (default 1)
- (--minutes) = how long to run (default 480 = 8 hrs, can be set to 1440 for 24 hrs)
- (--seed) = random seed (default 42)

**Output**:
- Console shows run summary
- Multiple results saved under data/ as "run_seed42_beds5_labs1.csv"

**Run multiple experiments**:
```bash
python src/batch_runs.py
```
This runs 10+ experiments with different setups.
Results go to:
```bash
data/batch_runs_folder/
```

**Run tests**:
```bash
pytest -v
```

Expected:
```bash
3 passed
```

## Project Structure
```bash
cs4632-er-sim/
├─ data/                        # simulation outputs
│  └─ m3_batch_runs/            # batch run CSV files
├─ report/                      # milestone reports
├─ screenshots/                 # console + CSV screenshots for M3
├─ src/
│  ├─ __init__.py
│  ├─ batch_runs.py             # batch experiment runner
│  ├─ main.py                   # main simulation runner
│  ├─ sim_config.py             # baseline configuration
│  ├─ models/
│  │  ├─ __init__.py
│  │  ├─ labs.py                # labs/imaging process
│  │  └─ scheduler.py           # staff scheduling
│  └─ tests/
│     └─ test_sim.py            # pytest verification tests
├─ uml/                         # UML diagrams
├─ refs.bib                     # references
├─ requirements.txt             # Python dependencies
├─ pytest.ini                   # pytest config
├─ README.md

```
## Architecture Overview
- **main.py**: sets up and runs the simulation (patients, triage, beds, labs).  
- **batch_runs.py**: runs multiple experiments automatically with different seeds and parameters.  
- **sim_config.py**: stores baseline default parameters (seed, minutes, arrival rates, capacities).  
- **models/scheduler.py**: handles staff scheduling (shift changes across time).  
- **models/labs.py**: simulates labs/imaging with random turnaround times.  
- **tests/test_sim.py**: verification tests to make sure patients are logged and times are valid.  

These align with the UML diagrams (class + activity) in the `uml/` folder.  

## Running Experiments
You can change scenarios in two ways:  

1. **Command-line parameters**  
   Run a single simulation with different values, for example:  
   ```bash
   python src/main.py --beds 10 --labs 5 --minutes 1440 --seed 99
   ```
2. **Batch runs**
   ```bash
   python src/batch_runs.py
   ```

   Results are saved into:
   data/batch_runs_folder/


## Project Management
We are tracking progress using a Github Project Board with "To Do / In Progress / Done" columns. 
- Here is the link: https://github.com/users/AashnaS23/projects/4

## License
MIT

