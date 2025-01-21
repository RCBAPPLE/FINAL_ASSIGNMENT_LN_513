# Real-Time Scheduling with FreeRTOS

This second part of the project demonstrates a real-time scheduling system implemented using FreeRTOS. The system consists of multiple tasks, each performing specific operations with strict periodicity and priorities. The tasks include logging, temperature conversion, binary search, and a RESET task for user input handling.

## Project Overview

### Tasks Description
| **Task Name**       | **Description**                                                   | **Priority**       | **Period**             |
|----------------------|------------------------------------------------------------------|--------------------|------------------------|
| **Logging Task**     | Logs a periodic "Working" message.                               | `tskIDLE_PRIORITY` | Every 400 ms           |
| **Temp Conversion**  | Converts Fahrenheit to Celsius and logs the result.             | `tskIDLE_PRIORITY + 3` | Every 330 ms       |
| **Binary Search**    | Performs a binary search on an array of 50 integers.            | `tskIDLE_PRIORITY + 1` | Every 350 ms       |
| **Big Number Math**  | Multiplies large numbers and prints the result.                 | `tskIDLE_PRIORITY + 2` | Every 330 ms       |
| **RESET Task**       | Monitors keyboard input and prints "RESET" upon detection, ensuring the state resets to zero for the next execution. | `tskIDLE_PRIORITY + 4` | Every 200 ms       |

### RESET Task Behavior
- Detects the key `'1'` from user input.
- Prints `"0"` when triggered.
- Resets its state to ensure the parameter is cleared for the next execution.

## System Design

### 1. Scheduling
The system uses the **FreeRTOS preemptive priority-based scheduler**:
- Tasks with higher priority can preempt lower-priority tasks.
- Periodic execution is managed using `vTaskDelay()` to ensure tasks execute at defined intervals without busy waiting.

We decided to display the task, as their importance seem to us. Following this idea, we put the highest priority to the reset task because it as to be executed whenever it can.
For the other tasks, there is not really an order, despite the first task, consisting on printing "Working" seem to be order as the second highest priority.
For the tasks 2, 3 and 4, we decided to let them in this order because of their similar importance in the schedule.

### 2. Worst-Case Execution Time (WCET)
Each task’s WCET has been analyzed to ensure it fits within its allocated period:

| **Task**            | **WCET (µs)**   | **Period (ms)**   | **Time Utilization** |
|----------------------|----------------|-------------------|-----------------------|
| **Logging Task**     | 50             | 400               | 12.5%                |
| **Temp Conversion**  | 70             | 330               | 21.2%                |
| **Binary Search**    | 90             | 350               | 25.7%                |
| **Big Number Math**  | 70             | 330               | 21.2%                |
| **RESET Task**       | 60             | 200               | 30.0%                |

### 3. Key Features
- **Efficient Real-Time Behavior**:
  - Each task executes within its time budget, ensuring deadlines are met.
- **Modularity**:
  - Tasks operate independently, minimizing interference.
- **Keyboard Input Handling**:
  - Task 5 uses a non-blocking method to detect keypresses (`'1'`) in real time.

## How to Run

1. **Set up FreeRTOS**:
   - Clone the FreeRTOS repository or download the required source files.
   - Copy and paste the files ipsa_sched.c and main.c into the repository :
     "../FreeRTOS/Demo/Posix_GCC"

2. **Build the Project**:
   ```bash
   make clean
   make
   ```

3. **Run the Program**:
   ```bash
   ./posix_demo
   ```

4. **Test RESET Task**:
   - Press the key `'1'` during execution to trigger the RESET task.
   - The console will display `"RESET"`.
  
## Possible Problem of running
Maybe you will face some problems to run the code, as it was for myself. I couldn't find any solution. 
I suppose the different problems I have with my computer could have drived to some errors with FreeRTOS. For myself, the code should work and run but I am blocked in an infinite loop with no exit possible.
But the terminal log out that the "Trace output saved to Trace.dump", so I guess it worked. Any solution I explored were not working, by changing the stacksize of the differents tasks in the ipsa_sched.c
or by modifying the value of configMINIMAL_STACK_SIZE into FreeRTOSConfig.h but nothing change. I hope it will work for yourself, but I don't guarantee it at 100%.
This last sentences were a warning in case of a problem with the code and the exploration of the different way I tried to resolve it.


