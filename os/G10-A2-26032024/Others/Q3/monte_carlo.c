#include <stdlib.h> // For rand() and srand()
#include <stdio.h> // For printf()
#include <pthread.h> // For threads
#include <time.h> // For time()

#define RADIUS 1.0 // Circle's radius
#define MAX 100000 // Total coordinates
#define PI 3.141593 // pi

int in = 0; // Coordinates within the circle

// Function prototypes
double normalize();
double getPi();
void* generate_coordinates();
void count_in(double x, double y);

int main()
{
    srand(time(NULL)); // Seed the random number generator with current time
    pthread_t thread_gen; // Thread for generating coordinates

    // Create a thread for generating coordinates
    pthread_create(&thread_gen, NULL, generate_coordinates, NULL);
    
    // Wait for the thread to finish
    pthread_join(thread_gen, NULL);

    // Output total points and points inside radius
    printf("Total Points:         %d\n", MAX);
    printf("Points inside radius: %d\n\n", in);
    
    // Output estimated and actual values of pi
    printf("Estimated pi: %f\n", getPi());
    printf("Actual pi:    %f\n", PI);

    return 0;
}

// Function to normalize coordinates
double normalize()
{
    // Generate a random number and normalize it
    return ((double)rand() / RAND_MAX * 2) - RADIUS;
}

// Function to estimate the value of pi
double getPi()
{
    // Calculate pi using the Monte Carlo method
    return (4.0 * in / MAX);
}

// Thread function to generate coordinates
void* generate_coordinates()
{
    double x, y;

    // Generate coordinates and count points within the circle
    for(int i = 0; i < MAX; i++)
    {
        x = normalize(rand);
        y = normalize(rand);

        count_in(x, y);
    }
    return NULL;
}

// Function to count points inside the circle
void count_in(double x, double y)
{
    // Check if the point (x, y) is inside the circle
    if(x * x + y * y <= RADIUS)
    {
        // Increment the count of points inside the circle
        in++;
    }
}
