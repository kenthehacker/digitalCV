#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/stat.h>
#include "sync.h"


int main(void){
    printf("hi\n");
    char buff[500];
    FILE * file;
    FILE * file_write;
    int num;
    int doubled;

    if (mkfifo(FIFO_NAME, S_IRUSR | S_IWUSR)<0){
        printf("failed to make fifo \n"); return -1;
    }
    file = fopen(FIFO_NAME, "r");
    file_write = fopen(FIFO_NAME, "w");
    if (file == NULL || file_write == NULL){
        printf("Failed to open file \n"); return -1;
    }

    
    printf("Reading from fifo: \n");
    while(fscanf(file, "%d\n", &num) == 1){
        
        printf("got %d ",num);
        doubled = num*2;
        printf("doubled: %d\n", doubled);
        
        
    }
    fclose(file);
    unlink(FIFO_NAME);
    return 0;
}
