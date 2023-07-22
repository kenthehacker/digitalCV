
#include <stdio.h>
#include <signal.h>
#include <unistd.h>

volatile sig_atomic_t done = 0;
volatile int count = 0;

void sig_handler( int signum, siginfo_t * si, void * uncontext ){

    // if (signum == SIGRTMIN) {
    //     count++;
    // }

    // if (signum == SIGRTMIN+1) {
    //     done = 1;
    // }
    if (si->si_value.sival_int == 0){
        count++;
    }else{
        done=1;
    }
}

int main (int argc, char* argv[]){

    struct sigaction ss;

    //ss.sa_handler = sig_handler;
    ss.sa_sigaction = sig_handler;
    ss.sa_flags = SA_RESTART | SA_SIGINFO;

    sigaction( SIGRTMIN, &ss, NULL );
    // sigaction( SIGRTMIN+1, &ss, NULL );

    printf("pid: %d\n", getpid());

    while (!done) {}

    printf("SIGRTMIN received %d times\n", count);

    return 0;
}
