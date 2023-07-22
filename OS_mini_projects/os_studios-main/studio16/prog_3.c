#include <stdio.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char *argv[]){
    int fd;
    int arg_idx;

    if (argc < 2){
        printf("to run %s, must pass in arguments\n",argv[0]);
        return -1;
    }
    fd = open(argv[1], O_RDWR | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR);
    for(arg_idx = 2; arg_idx < argc; arg_idx++){
        write(fd,argv[arg_idx],strlen(argv[arg_idx]));
        write(fd,"\n",1);
    }
    close(fd);
    return 0;
}