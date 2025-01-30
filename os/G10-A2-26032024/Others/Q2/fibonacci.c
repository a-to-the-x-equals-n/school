#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>


//Function that returns the fibonacci sequence
void *fibFunction(void *arg);

//Max Sequence length
#define MAX_SEQUENCE_LENGTH 100

//Holds the fibonacci sequenece
int sequence[MAX_SEQUENCE_LENGTH];



int main() {
    pthread_t thread;
    
    int num;

    //Get the number the length of the fibonacci sequence you want to got to
    printf("Enter a positive number for length of fibonacci sequence: ");
    scanf("%d", &num);

    //Loop to make user enter a number greater than 0
    while(num <= 0) {
        printf("Enter a positive number for length of fibonacci sequence: ");
        scanf("%d", &num);
    }


    //Create thread to create fibonacci sequence
    pthread_create(&thread, NULL, fibFunction, (void *)&num);

    //Wait for thread to finish
    pthread_join(thread, NULL);


    printf("\nFibnoacci sequence: ");

    //Loop to print out sequnce
    for(int i = 0; i < num; i++) {
        printf("%d ", sequence[i]);
    }

    printf("\n");
    return 0;

}


void *fibFunction(void *arg) {

    //Pull number from previous thread
    int num = *((int *) arg);
    

    //Fibonaci sequence starts with 0 and 1
    sequence[0] = 0;
    if(num > 1) sequence[1] = 1;

    //Loop to generate rest of sequence
    for(int i = 2; i < num; i++) {
        sequence[i] = sequence[i-1] + sequence[i-2];
    }

    pthread_exit(NULL);

}