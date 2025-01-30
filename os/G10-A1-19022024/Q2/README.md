# Zombie Process Demonstration

## Overview
This C program demonstrates the creation and management of a zombie process. It forks a child process that becomes a zombie and remains in the system for a specified duration. The program then clears the zombie process to free system resources.

## Instructions
1. Compile the program using a C compiler (e.g., `gcc`):

   ```bash
   gcc -o gcc process.c -o process
   ```

2. Run the program:

   ```bash
   ./process
   ```

3. Follow the on-screen instructions to observe the creation and termination of the zombie process.

## Important Notes
- **Parent Process:** The process that creates the child process.
- **Child Process:** A new process created by the parent process.
- **Zombie Process:** A process that has completed execution but still has an entry in the process table.

## Process States
- **Running (R):** Process is running
- **Sleeping (S):** Process is sleeping
- **Zombie (Z):** Process has completed execution but has not been removed from the process table
- **Terminated (T):** Process has terminated

## Additional Information
- **`fork()`:** Creates a child process as a copy of the parent process.
- **`getpid()`:** Retrieves the process ID (PID) of the calling process.
- **`pid_t`:** Data type used to represent PIDs in C.
- **`wait(NULL)`:** Waits for any child process to change state without retrieving the exit status or termination reason.
- **`exit()`:** Terminates the program and returns a status code to the operating system.

---
**Author:** Logan Reine
