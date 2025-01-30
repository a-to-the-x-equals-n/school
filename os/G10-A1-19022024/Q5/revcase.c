#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <ctype.h>

#define BUFFER_SIZE 25
#define READ_END 0
#define WRITE_END 1


int main() 
{

    // Pipe for sending original message from parent to child
    int original[2]; 

    // Pipe for sending reversed message from child to parent
    int reversed[2]; 


    // Buffer for message
    char msg[BUFFER_SIZE + 1];

    pid_t pid;

    // Creating pipes
    if (pipe(reversed) == -1 || pipe(original) == -1) 
    {
        perror("Pipe creation failed");
        return 1;
    }

    // Forking a child processs
    pid = fork();

    if (pid < 0) 
    {
        perror("Fork failed");
        return 1; 
    }

    // Parent process
    if (pid > 0) 
    { 
        close(reversed[WRITE_END]); // Close write end of reversed pipe
        close(original[READ_END]);  // Close read end of original pipe


        // Read a message from the user
        printf("Parent Process: Please enter a 25 character string to reverse its cases for each char\n");
        fgets(msg, sizeof(msg), stdin); // Read message from stdin
        msg[strcspn(msg, "\n")] = '\0'; // Remove newline character from the string


        printf("Parent process is sending a message: \"%s\"\n", msg);
        write(original[WRITE_END], msg, strlen(msg) + 1);   // Send message to child through original pipe


        // Wait for child to finish
        wait(NULL);

        // Read reversed message from child
        read(reversed[READ_END], msg, BUFFER_SIZE + 1); 
        
        sleep(1);
        printf("Parent Process received message: \"%s\"\n", msg);

        // Close remaining pipe ends
        close(original[WRITE_END]);
        close(reversed[READ_END]);
    }
    // Child Process
    else 
    { 
        close(reversed[READ_END]);   // Close read end of reversed pipe
        close(original[WRITE_END]);   // Close write end of original pipe


        // Read message from parent
        read(original[READ_END], msg, BUFFER_SIZE + 1);  // Read message from parent through original pipe

        sleep(1);
        printf("Child Process received message: \"%s\"\n", msg);


        // Reverse the case of each character in the message
        for(int i = 0; i < strlen(msg); i++) 
        {
            // swap cases
            msg[i] = isupper(msg[i]) ? tolower(msg[i]) : toupper(msg[i]);

        }
        
        // Send reversed message back to parent through reversed pipe
        write(reversed[WRITE_END], msg, strlen(msg) + 1);

        sleep(1);
        printf("Child process is sending a message: \"%s\"\n", msg);


        // Close remaining pipe ends
        close(reversed[WRITE_END]);
        close(original[READ_END]);
    }

    return 0; 
}
