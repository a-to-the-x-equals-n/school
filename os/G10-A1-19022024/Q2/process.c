#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>


int main()
{
    pid_t child;
    child = fork();
    int child_pid = getpid();

    char kill_command[30];

    // If 'positive int' : child PID returned; child successfully created
    if (child > 0)
    {
        // Parent sleeping
        for(int x = 15; x >= 0; x--)
        {
            system("clear");
            printf("\n\t\tParent is asleep for %d seconds\n", x);
            sleep(1);
        }
        system("clear");


        printf("\n\t\t...Executing: `ps -l`\n\n");
        sleep(2);
        system("ps -l");    // Execute terminal command "ps -l"
        fflush(stdout);     // Flush buffer

        // Wait for Enter key
        printf("\n\t\t\t--PRESS ENTER--\n");
        while (getchar() != '\n'); 
        fflush(stdout); 
        system("clear");

    }
    // Child Process
    else if (child == 0)
    {
        printf("Child process %d is exiting.\n", getpid());

        exit(0);
    }
    // Parent Process
    else
    {
        // Error forking
        perror("Error Forking");

        exit(0);
    }

    // Parent waits for any state change in `child`
    printf("\n\t\t...Executing: `wait(NULL)`\n\n");
    sleep(2);
    wait(NULL);
    system("clear");

    printf("\n\t\t-Zombie child has cleared-\n\n");
    system("ps -l"); 

    printf("\n\t\t\t--PRESS ENTER--\n");
    while (getchar() != '\n'); 
    fflush(stdout); 

    for(int x = 3; x > 0; x--)
    {
        system("clear");
        printf("\n\n\tSystem termination of PID %d in %x seconds\n\n", child_pid, x);
        sleep(1);
        // printf("\n\tThe system will now terminate PID: %d\n\n", child_pid);
    }
    
    // Format the command string with the variable value
    sprintf(kill_command, "kill -9 %d\n", child_pid);

    system("clear");
    // Pass the formatted command string to system()
    system(kill_command);

    return 0;
}