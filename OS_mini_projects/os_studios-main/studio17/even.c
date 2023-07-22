#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/stat.h>
#include "sync.h"
#include <limits.h>

int main(void){
    int i;
    FILE * fifo_file;
    int byte_counter = 0;
    int int_size;
    
    fifo_file = fopen(FIFO_NAME, "w");
    i = 2;
    int_size = sizeof(i);
    while(byte_counter < (PIPE_BUF/int_size)/2){
        byte_counter += 1;
        fprintf(fifo_file, "%d\n", i);
        printf("even: %d\n",i);
        i += 2;
    }

    fclose(fifo_file);
    return 0;
}