#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include "shared_mem.h"
int main(){
    int fd;
    struct shared_data *my_struct;
    fd = shm_open("/shared_memory_region", O_RDWR, S_IRWXU);
    if (fd==-1){
        printf("shm failed\n"); return -1;
    }
    my_struct = mmap(NULL, sizeof(struct shared_data), PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (my_struct == MAP_FAILED){
        printf("map failed\n");
        return -1;
    }
    my_struct->write_guard = 1;
    printf("Shared data values:\n");
    while(my_struct->read_guard == 0){

    }
    int local_array[shared_mem_size];
    memcpy(local_array, my_struct->data, sizeof(my_struct->data));

    /*
    for (int i = 0; i < shared_mem_size; i++) {
        printf("%d\n", local_array[i]);
    }
    */
    printf("Data pointer value: %p\n", (void*)my_struct);
    my_struct->delete_guard = 1;
    return 0;
}