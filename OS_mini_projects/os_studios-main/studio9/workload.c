/*    Simulated workload using OpenMP
 *
 * This program will create some number of seconds of work on each processor
 * on the system.
 *
 * This program requires the use of the OpenMP compiler flag, and that 
 * optimizations are turned off, to build correctly. E.g.: 
 * gcc -fopenmp workload.c -o workload
 */

#define _GNU_SOURCE
#include <stdio.h> // for printf()
#include <sched.h> // for sched_getcpu()

// 500 million iterations should take several seconds to run
#define ITERS 500000000
#define locked  1
#define unlocked  0
int iter_lock = unlocked;

void critical_section( void ){
	int index = 0;
	while(index < ITERS){ index++; }
}

void lock(volatile int * iter_lock){
	int expected = unlocked;
	int desired = locked;
	while(!__atomic_compare_exchange(iter_lock, &expected, &desired, 0, __ATOMIC_ACQ_REL, __ATOMIC_ACQUIRE)){
		expected = unlocked;
		//printf("CPU %d stuck \n", sched_getcpu());
	}
}

void unlock(volatile int * iter_lock){
	int expected = locked;
	int desired = unlocked;
	if(!__atomic_compare_exchange(iter_lock, &expected, &desired, 0, __ATOMIC_ACQ_REL, __ATOMIC_ACQUIRE)){
		printf("Failed to unlock\n");
		return;
	}
}

int main (int argc, char* argv[]){
	
	// Create a team of threads on each processor
	#pragma omp parallel
	{
		// Each thread executes this code block independently
		lock(&iter_lock);
		critical_section();
		unlock(&iter_lock);

		printf("CPU %d finished!\n", sched_getcpu());
	}

	return 0;
}
