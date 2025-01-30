# Message Reversal using Pipes

This C program demonstrates inter-process communication (IPC) using pipes to reverse the case of each character in a message between a parent and child process.

## How to Use

1. Compile the program using a C compiler:

   ```bash
   gcc revcase.c -o revcase
   ```

2. Run the compiled program:

   ```bash
   ./revcase
   ```

3. Follow the prompts to enter a 25-character string.

4. The program will reverse the case of each character in the string and display the reversed string.

## Example

```bash
Parent Process: Please enter a 25 character string to reverse its cases for each char
Hello, World!
Parent process is sending a message: "Hello, World!"
Child Process received message: "Hello, World!"
Child process is sending a message: "hELLO, wORLD!"
Parent Process received message: "hELLO, wORLD!"
```

## Notes

- The program uses two pipes: one for sending the original message from the parent to the child and another for sending the reversed message from the child to the parent.
- The `isupper()` and `tolower()` functions are used to convert uppercase characters to lowercase, and the `islower()` and `toupper()` functions are used to convert lowercase characters to uppercase.
- The program ensures that the entered string is no longer than 25 characters to avoid buffer overflow.