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

int main(int argc, char * argv[]){
    FILE * fifo_file;
    FILE * standard_source;
    int byte_counter = 0;
    int int_size;
    char *line = NULL;
    size_t len = 0;
    ssize_t nread;


    fifo_file = fopen(FIFO_NAME, "w");
    standard_source = fopen(argv[1],"r");
    if (argc<2 || standard_source == NULL || fifo_file == NULL){
        printf("failed to open either fifo or standard file");
        return -1;
    }
    
    int_size = sizeof(int);
    printf("int_size: %d\n",int_size);
    while((nread = getline(&line, &len, standard_source)) != -1) {
        printf("Retrieved line of length %zd:\n", nread);
        int num = atoi(line);
        fprintf(fifo_file, "%d\n", num);
    }

    fclose(standard_source);
    fclose(fifo_file);
    free(line);
    return 0;
}
