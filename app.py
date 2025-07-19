
from flask import Flask, render_template, request, jsonify
from main_logic import fcfs, sjf, srtf, round_robin, mlfq

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/schedule", methods=["POST"])
def schedule():
    data = request.get_json()
    processes = data.get("processes", [])
    algorithm = data.get("algorithm", "FCFS")
    quantum = int(data.get("quantum", 2))

    # Convert to [pid, arrival, burst]
    proc_data = [[p["pid"], int(p["arrival"]), int(p["burst"])] for p in processes]

    try:
        if algorithm == "FCFS":
            scheduled, gantt = fcfs(proc_data)
        elif algorithm == "SJF":
            scheduled, gantt = sjf(proc_data)
        elif algorithm == "SRTF":
            scheduled, gantt = srtf(proc_data)
        elif algorithm == "RR":
            scheduled, gantt = round_robin(proc_data, quantum)
        elif algorithm == "MLFQ":
            quantums = [2, 4, 8]
            allotments = [1, 2, 4]
            scheduled, gantt = mlfq(proc_data, quantums, allotments)
        else:
            return jsonify({"error": "Invalid algorithm"}), 400
    except Exception as e:
        return jsonify({"error": f"Scheduling failed: {str(e)}"}), 500

    # Return format
    results = []
    for p in scheduled:
        results.append({
            "pid": p[0],
            "arrival": p[1],
            "burst": p[2],
            "start": p[3],
            "end": p[4]
        })

    return jsonify({"processes": results, "gantt": gantt})

if __name__ == "__main__":
    app.run(debug=True)

