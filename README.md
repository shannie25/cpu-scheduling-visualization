# CPU Scheduling Simulator

### Operating Systems – Project 01

## Overview

This project is a **CPU Scheduling Simulator** built using **Python (Flask)** for the backend and **HTML/CSS/JavaScript** for the frontend. It visually demonstrates the behavior of multiple CPU scheduling algorithms. The project helps users understand and compare algorithm performance in terms of turnaround and response times.

---

## Features

- Visual and interactive web-based simulator.
- Supports **five major scheduling algorithms**:
  - FCFS (First Come, First Serve)
  - SJF (Shortest Job First - Non-preemptive)
  - SRTF (Shortest Remaining Time First - Preemptive)
  - RR (Round Robin)
  - MLFQ (Multilevel Feedback Queue)
- Supports:
  - Manual or Random input mode
  - Gantt chart generation
  - Simulation speed configuration
  - Calculation of Completion Time, Turnaround Time, and Response Time
- Beautiful **dark-themed UI** with neon hover effects.

---

## Technologies Used

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3 (custom + Roboto fonts), JavaScript (vanilla)
- **Design:** Responsive layout with flexbox/grid

---

## Project Structure

```bash
cpu-scheduling-simulator/
│
├── static/
│   └── csv.css              # All stylesheets
│
├── templates/
│   └── index.html           # Main user interface
│
├── main_logic.py            # Scheduling algorithms logic
├── app.py                   # Flask application server
├── README.md                # Project documentation
└── requirements.txt         # Flask dependency (if needed)



```  

## How to Run Locally

### 1. Install Flask

```bash
pip install flask
```

## 2. Run the app

```bash
python app.py
```
## 3. Open the browser
Visit: http://localhost:5000

## Acknowledgements
This simulator was developed as a project requirement for the Operating Systems course to visualize and analyze CPU scheduling strategies interactively.


<img width="829" height="223" alt="image" src="https://github.com/user-attachments/assets/0ce9383a-a4b2-4e7a-91c3-d4cb3401a16c" />
<img width="815" height="200" alt="image" src="https://github.com/user-attachments/assets/3775070f-1f0f-41be-8abb-e5c3e77d5dd2" />
<img width="1007" height="180" alt="image" src="https://github.com/user-attachments/assets/a7d89560-76a4-46fe-ac82-e4a92e59b399" />



