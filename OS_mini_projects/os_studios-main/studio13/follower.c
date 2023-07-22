#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include "shared_mem.h"

int main(void){
    
    int file_descriptor;
    
    file_descriptor = shm_open("/shared_memory_region", O_RDWR, S_IRWXU);
    if (file_descriptor == -1){
        printf("shm_open failed to create\n");
        return -1;
    }
    
    struct shared_data * dat;
    dat = mmap(NULL, sizeof(dat),PROT_READ | PROT_WRITE, MAP_SHARED, file_descriptor, 0);
    if (dat == MAP_FAILED){
        printf("map failed in follower \n");
        return -1;
    }


    dat->write_guard = 1;
    while (dat->read_guard == 0){
        //wait
    }

    //int follower_array[shared_mem_size];

    int *follower_array = malloc(sizeof(int) * shared_mem_size);
    printf("dat value: %p\n",(void*)dat->data);
    printf("made follower array\n" );
    memcpy(follower_array, (const void *)dat->data, sizeof(int)*shared_mem_size);


    printf("PRINTING FOLLOWER ARRAY: \n");
    for(int i = 0; i < shared_mem_size; i++){
        printf("%d\n",follower_array[i]);
    }

    dat->delete_guard = 1;
    

    return 0;
}

