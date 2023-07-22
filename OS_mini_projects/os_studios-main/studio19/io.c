#include <sys/select.h>
#include <sys/time.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char * argv[]){
	int nfds;
	fd_set readfds;
	int ret;

	FD_ZERO(&readfds);
	FD_SET(STDIN_FILENO, &readfds);
	nfds = STDIN_FILENO+1;
	while(1==1){
		ret = select(nfds, &readfds, NULL, NULL, NULL);
		if (ret == -1){
			perror("select failed:");
			return -1;
		}
		//printf("ret: %d\n",ret);
		if (FD_ISSET(STDIN_FILENO, &readfds)){
			char words[1024];
			fgets(words, 1024, stdin);
			if(strcmp(words,"quit\n") == 0){
				printf("killed program \n");
				return 0;
			}
			printf("read %s\n",words);
		}
	}
	return 0;
}



