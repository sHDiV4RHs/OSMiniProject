#include "types.h"
#include "user.h"

int main(void) 
{
    int parentPID = getpid();
    int childPID = fork();

    if(childPID == 0) 
    {
        printf(1, "I am child \n");
        printf(1, "savedParentPID: %d \n parentPIDfromgetppid(): %d \n", 
            parentPID, getppid());
    }
    else
    {
        printf(1, "I am Parent \n");
        wait();
    }
    exit();
}
