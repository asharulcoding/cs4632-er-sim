# CS4632 — Emergency Room Simulation (ER Sim)
**Course:** CS 4632 W01 Fall Semester

**Author:** Aashna Suthar, Ash Arul

## Project Overview
This project is a discrete-event simulation of an emergency room. The goal is to study how patients move through the ER and how limited staff and resources affect wait times, congestion, and overall patient flow. Patients arrive randomly, go through triage, wait for beds if needed, may visit labs, and then leave the system. By changing staffing levels, beds, labs, and arrival rates, we can analyze how different conditions impact system performance without using real patient data.

This simulation was built across Milestones 1–5 and includes full implementation, data collection, scenario testing, sensitivity analysis, validation, and final reporting.

## Project Status
This project was completed over five milestones. Each milestone built on the previous one and added new functionality, analysis, and validation.

**Milestone 1**
- Defined the overall problem and scope of the emergency room simulation.
- Identified the main system components: patients, triage, beds, doctors, and rooms.
- Created initial UML class and activity diagrams.
- Defined key assumptions and modeling goals.
- Selected Python and SimPy as the main simulation tools.
- Completed a literature review on ER simulation, queuing systems, and triage models.
- Set up the GitHub repository with README, folder structure, and version control.

**Milestone 2**
- Implemented random patient arrivals using a Poisson process.
- Implemented basic triage logic and severity assignment using the Emergency Severity Index (ESI).
- Modeled nurses, doctors, and rooms as limited simulation resources.
- Implemented FIFO and priority-based queuing.
- Added basic service time distributions for treatment.
- Implemented CSV output for storing simulation results.
- Added automated tests using pytest.
- Verified that changing bed capacity affected wait times correctly.
- Created a GitHub Project Board to track development progress.

**Milestone 3**
- Completed end-to-end simulation workflow from arrival to discharge.
- Added lab resource modeling and lab processing delays.
- Implemented full batch-run capability for repeated experiments.
- Added command-line arguments for:
  - arrival rate
  - triage capacity
  - bed capacity
  - lab capacity
  - random seed
  - simulation length
- Generated multiple CSV files from batch runs.
- Merged all run outputs into a single Excel/CSV results file.
- Collected performance metrics for:
  - triage wait
  - bed wait
  - lab time
  - total time in system
  - number of patients processed
- Documented all runs with screenshots and console output.

**Milestone 4**
- Created sensitivity analysis for:
  - number of beds vs total time
  -number of labs vs total time
- Generated sensitivity plots using matplotlib.
- Performed scenario testing using multiple configurations.
- Ran both 12-hour and 24-hour simulation scenarios.
- Completed statistical summaries for:
  - mean
  - standard deviation
  - confidence intervals
- Performed validation using:
  - face validity
  - output reasonableness
  - statistical stability
- Identified system bottlenecks and limitations.
- Documented all findings in the Milestone 4 analysis report.

**Milestone 5**
- Integrated all previous milestone work into one final, polished project.
- Improved sensitivity analysis with calculated sensitivity coefficients.
- Expanded scenario testing with deeper quantitative comparisons.
- Strengthened validation using extreme-condition testing.
- Added full statistical summary with visualizations:
  - box plots
  - histograms
- Completed final ER system recommendations based on results.
- Finalized the GitHub repository with clean structure and documentation.
- Finalized the LaTeX report for professional submission.
- Created and recorded a full video demonstration of the simulation.
- Ensured reproducibility with complete setup and usage instructions.
- Prepared all final deliverables for Milestone 5 submission.

## Models Used
**Queueing theory:** The ER is modeled using queue-based resource systems (M/M/c style behavior).
**Triage system:** Patients receive ESI severity levels (1–5) which map to priority scheduling.
**Resource utilization:** Triage nurses, beds, doctors, and labs are treated as limited shared resources.
**Discrete-event simulation:** Events such as arrivals, triage completion, bed assignment, lab service, and discharge advance the system.

## Metrics Collected
- Triage wait time
- Bed wait time
- Lab processing time
- Total time in the system
- Patient throughput
- System congestion under different conditions
- Statistical summaries across multiple runs

## Installation Instructions
```bash
git clone https://github.com/asharulcoding/cs4632-er-sim.git
cd cs4632-er-sim
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
## Usage Instructions
To run a 12-hour simulation with a fixed seed:
```bash
python src/main.py --hours 12 --seed 42
```

To run the simulation for 24 hours with a fixed seed: 
```bash
python src/main.py --hours 24 --seed 42
```

**Expected Output:**
- A CSV file is created in the data/ folder for each run.
- Output includes triage wait, bed wait, lab time, and total system time.
- A summary is printed to the terminal after each run.

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
├─ data/           # Output CSV files from simulation runs
├─ figures/        # Plots and graphs used in the report
├─ screenshots/    # Simulation and analysis screenshots
├─ uml/            # UML diagrams
├─ tests/          # pytest files
├─ refs.bib        # bibliography
├─ requirements.txt
├─ .gitignore
└─ README.md
```
## Architecture Overview
- **main.py**: Initializes the simulation, handles parameters, and runs the event loop.
- **sim_config.py**: Stores arrival rates, service distributions, and staffing setup.
- **arrivals.py**: Generates patient arrivals using a Poisson process.
- **triage.py**: Assigns severity levels and simulates triage waiting.
- **service_stations.py**: Handles beds, doctors, and labs as shared resources.
- **scheduler.py**: Controls staffing behavior and capacity logic.
  
These files directly match the UML class and activity diagrams used in the final report.

## Running Experiments
Different scenarios are defined by changing parameters in the command line or in sim_config.py. By running multiple seeds and multiple capacity combinations, we analyze system behavior under:
- Normal load
- High patient inflow
- Low staffing
- Extended 24-hour stress conditions
The output from these runs is used for sensitivity analysis, scenario comparison, and validation in Milestones 4 and 5.

## Data Analysis & Validation
- Sensitivity coefficients were calculated using percent change in output divided by percent change in input.
- Scenario testing was performed across four major operating conditions.
- Statistical summaries include means, standard deviations, and 95% confidence intervals.
- Validation included face validity, output reasonableness, and extreme-condition testing.
All analysis results are documented in the final M5 report.

## Project Management
We are tracking progress using a Github Project Board with "To Do / In Progress / Done" columns. 
- https://github.com/users/AashnaS23/projects/4

## License
MIT
