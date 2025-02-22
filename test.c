#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int main(void)
{
    int unix_time = time(NULL);
    printf("Unix time: %d\n", unix_time);

    while(1)
    {
        int unix_time = time(NULL);
        printf("Unix time: %d\n", unix_time);
        sleep(1);
    }
    // 输出年月日时分秒
    return 0;
}