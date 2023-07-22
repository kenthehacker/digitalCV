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
    fd = shm_open("/shared_memory_region", O_CREAT | O_RDWR, S_IRWXU);
    if (fd==-1){
        printf("shm_open failed \n");
        return -1;
    }
    int ret = ftruncate(fd, sizeof(struct shared_data));
    if (ret == -1){
        printf("failed to ftruncate\n");
        return -1;
    }
    my_struct = mmap(NULL, sizeof(struct shared_data), PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (my_struct == MAP_FAILED){
        printf("map failed\n");
        return -1;
    }
    my_struct->read_guard =0;
    my_struct->write_guard = 0;
    my_struct->delete_guard = 0;
    while(my_struct->write_guard == 0){

    }
    for (int i = 0; i < shared_mem_size; i++) {
        my_struct->data[i] = rand();
        //printf("val: %d\n",my_struct->data[i]);
    }
    my_struct->read_guard = 1;
    printf("my_struct pointer value: %p\n", (void*)my_struct);
    while(my_struct->delete_guard == 0){

    }

    munmap(my_struct,0);
    close(fd);
    return 0;
}