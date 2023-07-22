/*    Simulated workload using OpenMP
 *
 * This program will create some number of seconds of work on each processor
 * on the system.
 *
 * This program requires the use of the OpenMP compiler flag, and that 
 * optimizations are turned off, to build correctly. E.g.: 
 * gcc -fopenmp sleep_lock.c -o sleep_lock
 */

#define _GNU_SOURCE
#include <stdio.h> // for printf()
#include <sched.h> // for sched_getcpu()
#include <unistd.h>
#include <sys/syscall.h>
#include <linux/futex.h>
#include <sys/time.h>
#include <stdint.h>
#include <limits.h>

// 500 million iterations should take several seconds to run
#define ITERS 500000000
#define locked  0
#define unlocked  1
int iter_lock = unlocked;

void critical_section( void ){
	int index = 0;
	while(index < ITERS){ index++; }
}

void lock(){
	int ret_val;
	ret_val = __atomic_sub_fetch(&iter_lock, 1, __ATOMIC_ACQ_REL);
	while (ret_val<locked){
		syscall( SYS_futex, &iter_lock, FUTEX_WAIT, ret_val, NULL);
		ret_val = __atomic_sub_fetch(&iter_lock, 1, __ATOMIC_ACQ_REL);
	}
	return;
}

void unlock(){
	int ret_val;
	ret_val = __atomic_add_fetch(&iter_lock, 1, __ATOMIC_ACQ_REL );
	if (ret_val!=unlocked){
		__atomic_store_n(&iter_lock, 1, __ATOMIC_RELEASE );
		syscall( SYS_futex, &iter_lock, FUTEX_WAKE, INT_MAX );
	}
}


int main (int argc, char* argv[]){
	
	// Create a team of threads on each processor
	#pragma omp parallel
	{
		// Each thread executes this code block independently
		lock();
		critical_section();
		unlock();

		printf("CPU %d finished!\n", sched_getcpu());
	}

	return 0;
}
