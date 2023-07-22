#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <sched.h>
#include <stdlib.h>

int main(int argc, char* argv[]){
    int i;
    int end_loop = 500000000;
    int random_work = 0;
    int policy = SCHED_RR;

	if (argc!=3){
        printf("Incorrect usage\n");
        return -1;
    }
	int priority = atoi(argv[2]);
    int processor = atoi(argv[1]);
    pid_t pid = getpid();

    printf("processor: %d\n",processor);
    cpu_set_t allowed_cpus;
    CPU_ZERO(&allowed_cpus);
    CPU_SET(processor, &allowed_cpus);
	
	struct sched_param param = {.sched_priority = priority};

	int max_priority = sched_get_priority_max(policy);
	int min_priority = sched_get_priority_min(policy);
	if (priority>max_priority || priority<min_priority){
		printf("Provided priority number out of bound for SCHED_RR \n");
		printf("min: %d, max: %d \n",min_priority,max_priority);
		return -1;
	}
	int ret = sched_setscheduler(pid,policy, &param);
	if (0 != ret){
		printf("sched_setscheduler failed pid: %d\n",pid);
		printf("ret: %d \n",ret);
		printf("param priority: %d \n",param.sched_priority);
		return -1;
	}


    
    if (sched_setaffinity(pid, sizeof(allowed_cpus), &allowed_cpus)==-1){
        printf("Something went wrong at sched_setaffinity \n");
        return -1;
    }
    
	printf("Entering workload ...\n\n");
    for(i = 0; i<end_loop; i++){
        random_work = (random_work+1)*5;
    }
    
    return 0;
}




