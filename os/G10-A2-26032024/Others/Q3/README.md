# Multithreaded Monte Carlo Pi Estimation

This program estimates the value of π using the Monte Carlo method in a multithreaded environment. It generates random points within a square and determines if each point lies inside or outside a unit circle centered at the origin. By calculating the ratio of points inside the circle to the total number of points generated, it estimates the value of π.

## Prerequisites

- C compiler (e.g., gcc)
- POSIX threads library (pthreads)

## Usage

Compile the code using a C compiler. For example, with gcc:

```
gcc monte_carlo.c -o monte
```

Then, execute the compiled program:

```
./monte
```

## Description

- `monte_carlo.c`: This is the main source code file containing the implementation of the Monte Carlo method to estimate π in a multithreaded environment.
- `stdlib.h`, `stdio.h`, `pthread.h`, `time.h`: Header files necessary for standard library functions, thread creation, and time-related functions.
- `RADIUS`: Defines the radius of the circle for the Monte Carlo estimation.
- `MAX`: Defines the total number of random coordinates to generate.
- `PI`: The known value of π for comparison.
- `in`: Variable to count the number of coordinates falling inside the circle.
- `normalize()`: Function to generate a normalized random number within the range [-1, 1].
- `getPi()`: Function to estimate the value of π using the Monte Carlo method.
- `generate_coordinates()`: Thread function to generate random coordinates and count points inside the circle.
- `count_in()`: Function to count points inside the circle based on given coordinates.
- `main()`: The entry point of the program, responsible for spawning a thread to generate coordinates and outputting the estimated and actual values of π.

## Sample Output

```
Total Points:         100000
Points inside radius: 78514

Estimated pi: 3.140560
Actual pi:    3.141593
```

The program outputs the total number of points generated, the number of points falling inside the circle, and the estimated and actual values of π.