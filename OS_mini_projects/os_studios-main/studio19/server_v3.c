#define _GNU_SOURCE
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
#include <poll.h>
#define BACKLOG 5
#define BUF_SIZE 1024

int init_socket(){
    struct sockaddr_in serv_addr;
    int sfd;
    int port_num = 30303;
    sfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sfd == -1){
        perror("server socket failed");
        exit(1);
    }
    memset(&serv_addr, 0, sizeof(struct sockaddr_in));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(port_num);
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    while(bind(sfd, (struct sockaddr *) &serv_addr, sizeof(struct sockaddr_in)) == -1){
        printf("bind fail, addy in use\n");
        printf("trying to bind again...\n");
    }
    if (listen(sfd, BACKLOG) == -1){
        perror("listen fail");
        exit(1);
    }
    return sfd;
}

int accept_client(int server_socket){
    struct sockaddr_in client_address;
    socklen_t len = sizeof(client_address);
    int client_socket = accept(server_socket, (struct sockaddr *) &client_address, &len);
    if (client_socket > 0){
        printf("Client established %s\n",inet_ntoa(client_address.sin_addr));
    }else{
        perror("failed to accept client"); exit(1);
    }
    return client_socket;
}

int main(int argc, char *argv[]){
    int sfd = init_socket();
    struct pollfd *pollFd;
    int nfd = 2;
    pollFd = calloc(3, sizeof(struct pollfd));
    if (pollFd == NULL){
        perror("pollFd calloc");
        exit(1);
    }
    pollFd[0].fd = sfd;
    pollFd[0].events = POLLIN;
    pollFd[1].fd = STDIN_FILENO;
    pollFd[1].events = POLLIN;
    while(1==1){
        int ready = poll(pollFd, nfd, -1);
        if (ready<0){
            perror("poll failed");
            exit(1);
        }
        if (pollFd[0].revents & POLLIN){
            printf("SERVER socket: %d %3d\n", 0, pollFd[0].fd);
            int client_socket = accept_client(sfd);
            pollFd[2].fd = client_socket;
            pollFd[2].events = POLLIN | POLLRDHUP;
            nfd = 3;
        }
        if (pollFd[1].revents & POLLIN){
            printf("STDIN fd: %d %3d\n", 1, pollFd[1].fd);
            char words[BUF_SIZE];
			fgets(words, BUF_SIZE, stdin);
			if(strcmp(words,"quit\n") == 0){
				printf("killed program \n");
                close(pollFd[0].fd);
                close(pollFd[1].fd);
                if (nfd>0){
                    close(pollFd[2].fd);
                }
				return 0;
			}
			printf("read %s\n",words);
        }
        if (nfd > 2){
            if (pollFd[2].revents & POLLIN){
                char client_message[BUF_SIZE];
                int byte_count = read(pollFd[2].fd, client_message, BUF_SIZE);
                if (byte_count == 0){
                    nfd = 2;
                    close(pollFd[2].fd);                    
                }
                else if (byte_count>0){
                    char *token = strtok(client_message, "\n");
                    printf("%s\n", token);
                    // while(token!=NULL){
                    //     printf("cli msg: %s\n",client_message);
                    //     // if (strcmp(client_message,"quit\n") == 0){
                    //     //     return 0;
                    //     // }
                    //     // token = strtok(NULL, "\n");
                    // }
                    if ((strcmp(token, "quit\n") == 0) || (strcmp(token, "quit") == 0)){
                        printf("killed program \n");
                        close(pollFd[0].fd);
                        close(pollFd[1].fd);
                        if (nfd>0){
                            close(pollFd[2].fd);
                        }
                        return 0;
                    }
                }
                else{
                    perror("read failed");
                    exit(1);
                }
            }
            if (pollFd[2].revents & POLLRDHUP){
                nfd = 2;
                close(pollFd[2].fd);
                printf("client connection killed\n");
            }
        }
        
        
    }
    return 0;
}


//https://www.geeksforgeeks.org/strtok-strtok_r-functions-c-examples/