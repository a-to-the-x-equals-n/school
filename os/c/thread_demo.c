#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>

// Function prototype for the thread function
void* additionThread(void* arg);

int main()
{
    pthread_t thread1;  // Declaration of pthread variable to hold thread ID
    int num;            // Declaration of variable to hold user input

    printf("Enter a number: ");
    scanf("%d", &num);  // Prompt user to enter a number and read it into num variable

    // Create a new thread, passing the address of the num variable as an argument
    pthread_create(&thread1, NULL, additionThread, (void*)&num);

    void *results;  // Declaration of a void pointer to store the result returned by the thread

    // Wait for the thread to finish execution and obtain its return value
    pthread_join(thread1, &results);

    // Print the result obtained from the thread
    printf("Results of adding %d and %d: %d\n", num, 5, *((int*)results)); 

    return 0;
}

// Implementation of the thread function
void* additionThread(void* arg)
{
    // Extract the integer value from the argument passed to the thread
    int num = *((int *) arg);

    // Allocate memory to store the result
    int *result = (int *)malloc(sizeof(int));

    // Perform the addition operation and store the result
    *result = num + 5;
    
    // Exit the thread, returning the result
    pthread_exit(result);
}
