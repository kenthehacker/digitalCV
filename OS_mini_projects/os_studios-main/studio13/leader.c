#include <stdio.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include "shared_mem.h"
#include <stdlib.h>

int main(void){
    int file_descriptor;
    file_descriptor = shm_open("/shared_memory_region", O_CREAT | O_RDWR, S_IRWXU);
    if (file_descriptor == -1){
        printf("shm_open failed to create\n");
        return -1;
    }
    struct shared_data * dat;

    if (ftruncate(file_descriptor,sizeof(struct shared_data)) == -1){
        printf("failed to ftruncate\n");
        return -1;
    }

    dat = mmap(NULL, sizeof(dat),PROT_READ | PROT_WRITE, MAP_SHARED, file_descriptor, 0);
    if (dat == MAP_FAILED){
        printf("map failed in leader \n");
        return -1;
    }

    dat->write_guard = 0;
    dat->read_guard = 0;
    dat->delete_guard = 0;
    
    while(dat->write_guard == 0){
        //wait
    }
    
    //dat->data = malloc(sizeof(int) * shared_mem_size);
    srand(42);
    printf("WRITING LEADER VALUES \n");
    for(int i = 0; i < shared_mem_size; i++){
        int val = rand()%100;
        dat->data[i] = val;
        printf("%d\n",dat->data[i]);
    }
    printf("dat value: %p\n",(void*)dat->data);
    printf("FINISHED WRITING \n");
    dat->read_guard = 1;


    while(dat->delete_guard == 0){
        //do nothing
    }



    munmap(dat,0);
    close(file_descriptor);
    return 0;
}
