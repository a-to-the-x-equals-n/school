# Avg, Min, and Max generator

This C program generates the avg min and max of a sequence


The program uses a thread to generate the sequence for the given input number.

## How to Use

1. Compile the program using a C compiler:

   ```bash
   gcc stats.c -o stats -pthread
   ```

2. Run the compiled program:

   ```bash
   ./stats 0 1 2 3 4 76 43
   ```

## Example

```bash
    The average value is 18.428571
    The minimum value is 0
    The maximum value is 76
```
