#define shared_mem "/shared_memory_region"
#define shared_mem_size 2000000

struct shared_data {
    volatile int write_guard;
    volatile int read_guard;
    volatile int delete_guard;
    volatile int data[shared_mem_size]; //if we have size million we seg fault stack is too small
    //volatile int* data;
    
};




