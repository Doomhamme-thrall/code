#include <stdio.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>

int time_unix = 10000;

int main()
{
    while (1)
    {
        int currentTime = time(NULL);
        printf("He! %d\n", currentTime);
    }
    return 0;
}