
#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/resource.h>

int main(int argc, char *argv[]){
    if (argc < 3){
        return 1;
    }

    int pid = atoi(argv[1]);
    union sigval value;

    struct rlimit rlim;
    int limit = getrlimit(RLIMIT_SIGPENDING, &rlim);

    int num_signals = atoi(argv[2]);
    printf("max sigs to send: %d\n", rlim.rlim_max);
    if (num_signals > rlim.rlim_max){
        printf("num signal exceeds max\n");
        exit(1);
    }
    value.sival_int = 0;
    printf("this pid: %d\n",getpid());
    for(int i = 0; i < num_signals; i++){
        // kill(pid, SIGRTMIN);
        sigqueue(pid, SIGRTMIN, value);
    }
    // kill(pid, SIGRTMIN+1);
    value.sival_int = 1;
    sigqueue(pid, SIGRTMIN, value);
    return 0;

}


