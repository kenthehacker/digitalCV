#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/ktime.h>
#include <linux/hrtimer.h>
#include <linux/kthread.h>

#define iters 1000000

static struct task_struct *k_threads[4];
volatile int shared_data = 0;


int ret_zero(void * payload){
    int i;
	for(i = 0; i<iters; i++){
		shared_data++;
	}
    while(!kthread_should_stop()){
    	//do nothing
	}
    return 0;
}

static int thread_init(void){
	int i;
    printk(KERN_ALERT "k thread module loaded \n");
    k_threads[0] = kthread_create(ret_zero, NULL, "a");
    k_threads[1] = kthread_create(ret_zero, NULL, "b");
    k_threads[2] = kthread_create(ret_zero, NULL, "c");
    k_threads[3] = kthread_create(ret_zero, NULL, "d");

    for(i = 0; i<4; i++){
        kthread_bind(k_threads[i], i);
        wake_up_process(k_threads[i]);
    }
    return 0;
}

static void thread_exit(void){
	int i;
    printk(KERN_ALERT "k thread module offloaded \n");

    for(i = 0; i<4; i++){
        kthread_stop(k_threads[i]);
    }
    printk(KERN_ALERT "shared_data was %d \n", shared_data);

}

module_init(thread_init);
module_exit(thread_exit);
MODULE_AUTHOR("kenthehacker");
MODULE_DESCRIPTION("Thread Module");
MODULE_LICENSE("GPL"); 








