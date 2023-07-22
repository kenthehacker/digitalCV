#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

#define BUF_SIZE 500

int main(void){
    int fd[2];
    pid_t pid;
    char buf[BUF_SIZE];

    if (pipe(fd)==-1){
        printf("Piping failed \n");
        return -1;
    }
    pid = fork();
    if (pid < 0){
        printf("forking fail \n");
        return -1;
    }
    if (pid == 0){
        close(fd[0]);
        char msg[] = "hello, im the child \n";
        char msg2[] = "Anything less than immortality is a complete waste of time \n";
        char msg3[] = "Bite my shiny metal ass\n";
        write(fd[1],msg,strlen(msg));
        write(fd[1],msg2,strlen(msg2));
        write(fd[1],msg3,strlen(msg3));
        close(fd[1]);
    }else{
        close(fd[1]);
        printf("Parent recieved folowing message(s)\n");
        while(read(fd[0],buf,sizeof(buf))>0){
            printf("%s",buf);
        }
        close(fd[0]);
    }

    return 0;
}





