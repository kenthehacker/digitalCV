#include <sys/socket.h>
#include <sys/select.h>
#include <sys/time.h>
#include <stddef.h>
#include <sys/un.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netdb.h>
#define BACKLOG 5
#define BUF_SIZE 1024

int main(int argc, char *argv[]){
    struct sockaddr_in addr, cli_addr;
    unsigned int end_of_message = 418;
    int sfd, cfd;
    int port_num = 30303;
    sfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sfd == -1){
        perror("server socket failed");
        exit(1);
    }
    memset(&addr, 0, sizeof(struct sockaddr_in));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port_num);
    addr.sin_addr.s_addr = INADDR_ANY;
    while(bind(sfd, (struct sockaddr *) &addr, sizeof(struct sockaddr_in)) == -1){
        printf("bind fail, addy in use\n");
        printf("trying to bind again...");
    }
    if (listen(sfd, BACKLOG) == -1){
        perror("listen fail");
        exit(1);
    }
    int nfd = sfd;
    fd_set readfds, writefds;
    FD_ZERO(&readfds);
    FD_ZERO(&writefds);
    FD_SET(sfd, &readfds);
    for(;;){
        // printf("before\n");
        fd_set temp_read_fds = readfds;
        select(nfd+1, &temp_read_fds, &writefds, NULL, NULL);
        // printf("after\n");
        
        for(int i_fd = 0; i_fd<nfd+1; i_fd++){
            // printf("point a\n");
            if (FD_ISSET(i_fd, &temp_read_fds)){
                // printf("point b\n");
                if (i_fd == sfd){
                    // printf("point c\n");
                    socklen_t addrlen = sizeof(cli_addr);
                    cfd = accept(sfd, (struct sockaddr *)&cli_addr, &addrlen);
                    FD_SET(cfd, &readfds);
                    if (cfd>nfd){
                        nfd = cfd;
                    }
                }else{
                    uint32_t cli_msg;
                    // printf("point d\n");
                    int byte_count = read(i_fd, &cli_msg, sizeof(uint32_t));
                    // printf("point e\n");
                    if (byte_count == 0){
                        char client_ip[INET_ADDRSTRLEN];
                        inet_ntop(AF_INET, &(cli_addr.sin_addr), client_ip, INET_ADDRSTRLEN);
                        printf("connection to %s client killed\n",client_ip);
                        close(i_fd);
                        FD_CLR(i_fd, &readfds);
                    }else{
                        unsigned int unsigned_cli_message = ntohl(cli_msg);
                        if (unsigned_cli_message != end_of_message){
                            printf("msg from client: %u\n",unsigned_cli_message);
                        }
                        if(unsigned_cli_message == end_of_message){
                            // printf("here\n");
                            char server_to_cli_msg[BUF_SIZE];
                            char hostname[BUF_SIZE];
                            gethostname(hostname,BUF_SIZE);
                            sprintf(server_to_cli_msg, "%s: end of msg", hostname);
                            write(nfd, server_to_cli_msg, sizeof(server_to_cli_msg));
                        }
                        // printf("point f\n");
                    }
                }
            }
        }
    }
    
}