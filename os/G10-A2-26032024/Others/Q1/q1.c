#include <pthread.h>

void* exampleFunction(void* arg);

int main()
{
    pid_t pid;
    pid = fork();

    int example = 2;

    if(pid == 0)
    {
        fork();
        pthread_create(&pid, NULL, exampleFunction, (void*)&example);
    }

    fork();
    return 0;
}
