# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 08:59:33 2025

@author: 33787
"""

import numpy as np 

# Simplified EDF Scheduling Without Classes

# Define tasks as a list of (computation_time, period)
tasks = [
    (2, 10),  # Task 1
    (3, 10),  # Task 2
    (2, 20),  # Task 3
    (2, 20),  # Task 4
    (2, 40),  # Task 5
    (2, 40),  # Task 6
    (3, 80),  # Task 7
]

# Identify Task 5 for special treatment
special_task = 4  # τ5 is task index 4 (0-based)

# Calculate hyperperiod (LCM of periods)
periods = [task[1] for task in tasks]
hyperperiod = np.lcm.reduce(periods)

print("Hyperperiod:", hyperperiod)

# Check schedulability using utilization factor
utilization = sum(task[0] / task[1] for task in tasks)
print(f"Total Utilization: {utilization:.2f}")
if utilization > 1:
    print("The task set is NOT schedulable.")
else:
    print("The task set is schedulable.")

# Create EDF schedule

# Initialize variables
schedule = []
remaining_times = [0] * len(tasks)
deadlines = [0] * len(tasks)
waiting_times = [0] * len(tasks)

for task_id, task in enumerate(tasks):
    deadlines[task_id] = task[1]  # Initial deadline

# Simulation loop
for time in range(hyperperiod):
    # Release tasks
    for task_id, task in enumerate(tasks):
        if time % task[1] == 0:
            remaining_times[task_id] = task[0]  # Refill computation time
            deadlines[task_id] = time + task[1]  # Set new deadline

    # Find the eligible task with the earliest deadline
    eligible_tasks = [i for i, remaining in enumerate(remaining_times) if remaining > 0]
    if eligible_tasks:
        next_task = min(eligible_tasks, key=lambda i: (deadlines[i], i))
        
        # Allow τ5 to miss a deadline
        if next_task == special_task and deadlines[next_task] < time:
            remaining_times[next_task] = 0  # Skip this task (missed deadline)
            print(f"Time {time}: Task {special_task + 1} missed a deadline.")
            continue

        # Execute the selected task
        schedule.append((time, next_task + 1))
        remaining_times[next_task] -= 1
        for i in eligible_tasks:
            if i != next_task:
                waiting_times[i] += 1  # Increment waiting time for other tasks
    else:
        schedule.append((time, None))  # Idle time

# Print the schedule
print("\nSchedule:")
for time, task_id in schedule:
    if task_id is None:
        print(f"Time {time}: IDLE")
    else:
        print(f"Time {time}: Task {task_id}")

# Print total waiting times
print("\nTotal Waiting Times:")
for i, wait_time in enumerate(waiting_times):
    print(f"Task {i + 1}: {wait_time}")

