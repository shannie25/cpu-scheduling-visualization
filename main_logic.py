import random
from collections import deque

# Get user input or generate random processes
def get_processes():
    processes = []
    n = int(input("Enter number of processes: "))
    mode = input("Manual (M) or Random (R) input? ").strip().upper()

    for i in range(n):
        pid = "P" + str(i)
        if mode == "M":
            at = int(input(f"Enter arrival time for {pid}: "))
            bt = int(input(f"Enter burst time for {pid}: "))
        else:
            at = random.randint(0, 5)
            bt = random.randint(1, 10)
            print(f"{pid} - Arrival: {at}, Burst: {bt}")
        processes.append([pid, at, bt])
    return processes

# First-Come First-Serve
def fcfs(processes):
    processes.sort(key=lambda x: x[1])
    time = 0
    gantt = []

    for p in processes:
        pid, at, bt = p
        if time < at:
            time = at
        start = time
        time += bt
        completion = time
        p.append(start)
        p.append(completion)
        gantt.extend([pid] * bt)

    return processes, gantt

# Shortest Job First (Non-Preemptive)
def sjf(processes):
    n = len(processes)
    completed = 0
    time = 0
    gantt = []
    ready_queue = []
    visited = [False] * n

    while completed < n:
        for i in range(n):
            if processes[i][1] <= time and not visited[i]:
                ready_queue.append(processes[i])
                visited[i] = True

        if ready_queue:
            ready_queue.sort(key=lambda x: x[2])
            current = ready_queue.pop(0)
            pid, at, bt = current
            start = time
            time += bt
            completion = time
            current.append(start)
            current.append(completion)
            gantt.extend([pid] * bt)
            completed += 1
        else:
            time += 1

    return processes, gantt

# Shortest Remaining Time First (Preemptive)
def srtf(processes):
    n = len(processes)
    time = 0
    complete = 0
    remaining_bt = [p[2] for p in processes]
    gantt = []
    start_times = [None] * n
    completion_times = [0] * n

    while complete < n:
        idx = -1
        min_bt = float('inf')
        for i in range(n):
            if processes[i][1] <= time and remaining_bt[i] > 0 and remaining_bt[i] < min_bt:
                min_bt = remaining_bt[i]
                idx = i

        if idx == -1:
            gantt.append("idle")
            time += 1
            continue

        if start_times[idx] is None:
            start_times[idx] = time

        gantt.append(processes[idx][0])
        remaining_bt[idx] -= 1
        time += 1

        if remaining_bt[idx] == 0:
            complete += 1
            completion_times[idx] = time

    for i in range(n):
        processes[i].append(start_times[i])
        processes[i].append(completion_times[i])

    return processes, gantt

# Round Robin Scheduling
def round_robin(processes, quantum):
    processes.sort(key=lambda x: x[1])
    n = len(processes)
    remaining_bt = [p[2] for p in processes]
    time = 0
    completed = 0
    gantt = []
    queue = deque()
    visited = [False] * n
    start_times = [None] * n
    completion_times = [0] * n
    i = 0

    while completed < n or queue:
        while i < n and processes[i][1] <= time:
            queue.append(i)
            visited[i] = True
            i += 1

        if queue:
            idx = queue.popleft()
            pid, at, bt = processes[idx]
            if start_times[idx] is None:
                start_times[idx] = time

            run_time = min(quantum, remaining_bt[idx])
            gantt.extend([pid] * run_time)
            time += run_time
            remaining_bt[idx] -= run_time

            while i < n and processes[i][1] <= time:
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True
                i += 1

            if remaining_bt[idx] > 0:
                queue.append(idx)
            else:
                completion_times[idx] = time
                completed += 1
        else:
            gantt.append("idle")
            time += 1

    for i in range(n):
        processes[i].append(start_times[i])
        processes[i].append(completion_times[i])

    return processes, gantt

# Multilevel Feedback Queue
def mlfq(processes, quantums, allotments):
    n = len(processes)
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    remaining_bt = [p[2] for p in processes]
    time = 0
    completed = 0
    gantt = []

    queues = [deque() for _ in range(len(quantums))]
    level = [0] * n
    visited = [False] * n
    allotment_used = [0] * n  # Tracks how many quanta used at current level
    start_times = [None] * n
    completion_times = [0] * n
    i = 0

    while completed < n:
        while i < n and processes[i][1] <= time:
            queues[0].append(i)
            visited[i] = True
            i += 1

        queue_found = False
        for q in range(len(quantums)):
            if queues[q]:
                idx = queues[q].popleft()
                queue_found = True
                pid, at, bt = processes[idx]

                if start_times[idx] is None:
                    start_times[idx] = time

                run_time = min(quantums[q], remaining_bt[idx])
                gantt.extend([f"{pid}(Q{q})"] * run_time)
                time += run_time
                remaining_bt[idx] -= run_time

                # Check for new arrivals during execution
                while i < n and processes[i][1] <= time:
                    if not visited[i]:
                        queues[0].append(i)
                        visited[i] = True
                    i += 1

                if remaining_bt[idx] > 0:
                    allotment_used[idx] += 1
                    if allotment_used[idx] >= allotments[q]:
                        level[idx] = min(level[idx] + 1, len(quantums) - 1)
                        allotment_used[idx] = 0
                    queues[level[idx]].append(idx)
                else:
                    completion_times[idx] = time
                    completed += 1
                break

        if not queue_found:
            gantt.append("idle")
            time += 1

    for i in range(n):
        processes[i].append(start_times[i])
        processes[i].append(completion_times[i])

    return processes, gantt

# Inside main_logic.py
def run_algorithm(processes, algorithm, quantum=2, quantums=[], allotments=[]):
    # Convert list of dicts to format like: [pid, at, bt]
    proc_list = [[p["pid"], p["arrival"], p["burst"]] for p in processes]

    if algorithm == "FCFS":
        result, gantt = fcfs(proc_list)
    elif algorithm == "SJF":
        result, gantt = sjf(proc_list)
    elif algorithm == "SRTF":
        result, gantt = srtf(proc_list)
    elif algorithm == "RR":
        result, gantt = round_robin(proc_list, quantum)
    elif algorithm == "MLFQ":
        result, gantt = mlfq(proc_list, quantums, allotments)
    else:
        result, gantt = fcfs(proc_list)  # Default fallback

    final = []
    for r in result:
        pid, at, bt, st, ct = r
        final.append({
            "pid": pid, "arrival": at, "burst": bt,
            "start": st, "end": ct
        })
    return final, gantt


# Print Gantt chart and metrics
def print_results(processes, gantt):
    print("\nGantt Chart:")
    print(" | ".join(gantt))

    print("\nPID\tAT\tBT\tCT\tTAT\tRT")
    total_tat = 0
    total_rt = 0

    for p in processes:
        pid, at, bt, st, ct = p
        tat = ct - at
        rt = st - at
        total_tat += tat
        total_rt += rt
        print(f"{pid}\t{at}\t{bt}\t{ct}\t{tat}\t{rt}")

    n = len(processes)
    print(f"\nAverage Turnaround Time: {total_tat / n:.2f}")
    print(f"Average Response Time: {total_rt / n:.2f}")

# Main program
def main():
    processes = get_processes()
    algo = input("Choose Algorithm (FCFS, SJF, SRTF, RR, MLFQ): ").strip().upper()

    if algo == "FCFS":
        processes, gantt = fcfs([p.copy() for p in processes])
    elif algo == "SJF":
        processes, gantt = sjf([p.copy() for p in processes])
    elif algo == "SRTF":
        processes, gantt = srtf([p.copy() for p in processes])
    elif algo == "RR":
        quantum = int(input("Enter time quantum: "))
        processes, gantt = round_robin([p.copy() for p in processes], quantum)
    elif algo == "MLFQ":
        quantums = []
        allotments = []
        for q in range(4):
            t = int(input(f"Enter time quantum for Queue Q{q}: "))
            a = int(input(f"Enter allotment (quanta before demotion) for Queue Q{q}: "))
            quantums.append(t)
            allotments.append(a)
        processes, gantt = mlfq([p.copy() for p in processes], quantums, allotments)
    else:
        print("Invalid choice. Defaulting to FCFS.")
        processes, gantt = fcfs([p.copy() for p in processes])

    print_results(processes, gantt)

if __name__ == "__main__":
    main()