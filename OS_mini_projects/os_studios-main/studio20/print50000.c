#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


#define size 500000

volatile int i;
int called [size];
volatile sig_atomic_t flag = 0;

void handler (int arg){
    called[i] = 1;
    // flag = 1;
    // printf("Caught SIGINT\n");
    char * message = "Caught SIGINT\n";
    write(STDOUT_FILENO, message, strlen(message));
}

int main (int argc, char* argv[]){
    struct sigaction s_action;
    
    s_action.sa_handler = handler;
    s_action.sa_flags = SA_RESTART;
    int ret = sigaction(SIGINT, &s_action, NULL);

    if (ret<0){
        perror("sigation");
        exit(1);
    }

    for(i = 0; i < size; i++){
        printf("i: %d\n", i);
        if (flag == 1){
            break;
        }
    }
    for(i = 0; i < size; i++){
        
        if( called[i] == 1 )
            printf("%d was possibly interrupted\n", i);
    }

    return 0;
}



/*

int sigaction(int signum, const struct sigaction *act, struct sigaction *oldact);
*/

