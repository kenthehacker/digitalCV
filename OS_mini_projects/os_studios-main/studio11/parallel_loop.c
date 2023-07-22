#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <sched.h>
#include <stdlib.h>

int main(int argc, char* argv[]){
    int end_loop = 500000000;
    int random_work = 0;
    int policy = SCHED_RR;

	if (argc!=4){
        printf("Incorrect usage\n");
        return -1;
    }
	int priority = atoi(argv[2]);
    int processor = atoi(argv[1]);
	int num_tasks = atoi(argv[3]);
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

	if (num_tasks>10 || num_tasks<=0){
		printf("Num tasks must be between 10 and 1");
		return -1;
	}
	for(int i = 0; i<num_tasks; i++){
		pid_t curr_pid = fork();
		if (curr_pid==-1){
			printf("failed to fork\n");
			return -1;
		}
		else if (curr_pid == 0){
			printf("child %d pid:%d created \n",i+1,getpid());
		}else{
			printf("Parent pid:%d spawned child %d'th child with pid:%d \n",getpid(), i+1, curr_pid);
		}
	}	
    
	printf("Entering workload ...\n");
    for(int i = 0; i<end_loop; i++){
        random_work = (random_work+1)*5;
    }
	printf("\n");
    
    return 0;
}




