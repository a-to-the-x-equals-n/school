#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>

//Generates the minimum of the given sequence
void *minFunction(void *arg);

//Generates the maximum of the given sequence
void *maxFunction(void *arg);

//Generates the average of the given sequence
void *avgFunction(void *arg);


int main(int argc, char *argv[]) {

    //User didn't format command right
    if (argc < 2) {
        printf("ERROR must use command with integers. Example: %s 10 20 30 40 50\n", argv[0]);
        return -1;
    }

    //Number of elements in the sequence
    int elements = argc - 1;


    //Create the array with size of elements
    int *values = (int *)malloc(elements * sizeof(int));
    if (values == NULL) {
        printf("Memory allocation failed\n");
        return -1;
    }

    //Add the elements of the seqeuence into the array
    for(int i = 0; i < elements; i++) {
        values[i] = atoi(argv[i + 1]);
    }

    //Arguments to pass to the functions
    void *args[2];
    args[0] = (void *)values;
    args[1] = (void *)&elements;

    //Create 3 threads
    pthread_t thread[3];
    
    //Create thread for each function
    pthread_create(&thread[0], NULL, avgFunction, args);
    pthread_create(&thread[1], NULL, minFunction, args);
    pthread_create(&thread[2], NULL, maxFunction, args);

    //Variables to hold the mimimum maximum and average values
    void *min, *max, *avg;

    //Wait for threads to finish
    pthread_join(thread[0], &avg);
    pthread_join(thread[1], &min);
    pthread_join(thread[2], &max);
    

    printf("The average value is %f\n", *((double*)avg));
    printf("The minimum value is %d\n", *((int*)min));
    printf("The maximum value is %d\n", *((int*)max));

    //Free up space used from arrary and value variables
    free(values);
    free(avg);
    free(min);
    free(max);
    


    return 0;

}


void *minFunction(void *arg) {
    //Grab the array
    int *array = ((int **)arg)[0];

    //Grab the size of the array
    int size = *((int **)arg)[1];

    //create pointer for minimum value
    int *min = (int *)malloc(sizeof(int));

    //Points to minimum value
    *min = array[0];

    //Loop to find minimum value
    for(int i = 0; i < size; i++) {
        //If current value is less than the minimum change the minimum to current value
        if(array[i] < *min) *min = array[i];
    }

    //Exit with minimum
    pthread_exit(min);

}

void *maxFunction(void *arg) {
    //Grab the array
    int *array = ((int **)arg)[0];
    //Grab the size of the array
    int size = *((int **)arg)[1];

    //create pointer for maximum value
    int *max = (int *)malloc(sizeof(int));
    
    //Points to maximum value
    *max = array[0];

    //Loop to find maximum value
    for(int i = 1; i < size; i++) {
        //If current value is more than the maximum change maximum to the current value
        if(array[i] > *max) *max = array[i];
    }

    //Exit with maximum
    pthread_exit(max);
}

void *avgFunction(void *arg) {
    //Grab the array
    int *array = ((int **)arg)[0];
    //Grab the size of the array
    int size = *((int **)arg)[1];

    //Variable to hold total value
    int total = 0;

    //Pointer to hold average value
    double *avg = (double *)malloc(sizeof(double));
    
    //Loop to add the total of the whole sequence
    for(int i = 0; i < size; i++) {
        total += array[i];
    }

    //Calculate the average
    *avg = (double)total / size;

    //Exit with average
    pthread_exit(avg);
}
