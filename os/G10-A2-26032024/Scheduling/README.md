# Scheduling program 

This java program simulates how certain task scheduling algorithms work

## How to Use

1. Compile the program using a java compiler:

   ```bash
   javac Task.java
   javac Algorithm.java
   javac CPU.java
   javac FCFS.java
   javac RR.java
   javac SJF.java
   javac Priority.java
   javac PriorityRR.java
   javac Driver.java
   ```

2. Run the compiled program:

   ```bash
   java Driver <Algorithm> <Schedule>
   ```


## Example

```bash
java Driver FCFS sched.txt

FCFS Scheduling 

Will run Name: T1
Tid: 0
Priority: 4
Burst: 20

Will run Name: T2
Tid: 1
Priority: 3
Burst: 25
....
```

## Notes

- Supported scheduling algorithms: FCFS (First Come First Serve), SJF (Shortest Job First), PRI (Priority), RR (Round Robin), PRI-RR (Priority with Round Robin).
