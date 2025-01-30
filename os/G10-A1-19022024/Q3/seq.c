#include <stdio.h>
#include <unistd.h> 
#include <sys/wait.h> 

int main() 
{
    // Depending on user input, `long long` is used in case `num` grows beyond 32 bits
    long long num = 0;

    
    printf("Please enter a positive integer: ");

    // Loop to ensure the user inputs a positive integer
    while(scanf("%lld", &num) != 1 || num <= 0)
    {
        printf("Invalid input. Please enter a positive integer: ");
        while (getchar() != '\n'); // clear buffer
    };
    

    // Fork a child process
    pid_t pid = fork();

    
    // Check if fork failed
    if (pid < 0) 
    {
        printf("Fork failed");
        return 1;
    }
    // Child process
    else if (pid == 0) 
    {

        printf("Child process: ");

        // Perform sequence calculation until num is 1
        while(num > 1) 
        {
            printf("%lld, ", num);

            // If num is even, divide it by 2; otherwise, multiply by 3 and add 1
            num = (num % 2 == 0) ? num / 2 : 3 * num + 1;
        }

        // Print the final number in the sequence, which should be 1
        printf("%lld\n", num);
        
    }
    
    // Parent process
    else 
    {
        // Wait for child process to finish
        wait(NULL);
        printf("Parent Process: Child process ended\n");
    }

    return 0;
}