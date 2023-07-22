#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <sched.h>
#include <stdlib.h>

int main(int argc, char* argv[]){
    if (argc!=2){
        printf("Incorrect usage\n");
        return -1;
    }
    int processor = atoi(argv[1]);
    printf("processor: %d\n",processor);
    cpu_set_t allowed_cpus;
    CPU_ZERO(&allowed_cpus);
    CPU_SET(processor, &allowed_cpus);
    pid_t pid = getpid();
    
    if (sched_setaffinity(pid, sizeof(allowed_cpus), &allowed_cpus)==-1){
        printf("Something went wrong at sched_setaffinity \n");
        return -1;
    }
    
    while(1==1){
        //do nothin
    }
    return 0;
}




