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
#include <sys/epoll.h>
#define BACKLOG 5
#define BUF_SIZE 1024
#define MAX_EVENTS 3

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
void handle_stdin(){
    char words[BUF_SIZE];
    fgets(words, BUF_SIZE, stdin);
    if(strcmp(words,"quit\n") == 0){
        printf("killed program \n");
        exit(0);
    }
    printf("read %s\n",words);
}
void kill_client_connection(int epfd, int cli_sock){
    epoll_ctl(epfd, EPOLL_CTL_DEL, cli_sock, NULL);
    close(cli_sock);
    printf("Killed client connection\n");
}
void read_from_client(int cli_sock, int epfd){
    char words[BUF_SIZE];
    int byte_count = read(cli_sock, words, BUF_SIZE);
    if (byte_count>0){
        printf("cli said: %s\n",words);
    }
    if (strcmp(words,"quit") == 0 || strcmp(words,"quit\n")==0){
        printf("connection killed");
        kill_client_connection(epfd, cli_sock);
    }
}
int main(void){
    int epfd = epoll_create1(0);
    int cli_sock;
    int sfd = init_socket();
    struct epoll_event stdin_ev, server_ev;
    struct epoll_event evlist[MAX_EVENTS];
    memset(&stdin_ev,0,sizeof(stdin_ev)); 
    memset(&server_ev,0,sizeof(server_ev));
    server_ev.events = EPOLLIN;
    server_ev.data.fd = sfd;
    stdin_ev.events = EPOLLIN | EPOLLET;
    stdin_ev.data.fd = STDIN_FILENO;
    if (epoll_ctl(epfd, EPOLL_CTL_ADD, sfd, &server_ev)<0){
        perror("failed to add server"); 
        exit(1);
    }
    if (epoll_ctl(epfd, EPOLL_CTL_ADD, STDIN_FILENO, &stdin_ev)<0){
        perror("failed to add stdin"); 
        exit(1);
    }
    while(1==1){
        int ready = epoll_wait(epfd, evlist, MAX_EVENTS, -1);
        for(int i = 0; i<ready; i++){
            int this_fd = evlist[i].data.fd;
            if (this_fd == sfd){
                cli_sock = accept_client(sfd);
                struct epoll_event cli_event;
                cli_event.events = EPOLLIN | EPOLLRDHUP;
                cli_event.data.fd = cli_sock;
                if (epoll_ctl(epfd, EPOLL_CTL_ADD, cli_sock, &cli_event)<0){
                    perror("failed to accept"); 
                    exit(1);
                }
            }
            else if (evlist[i].events & EPOLLIN){
                if (this_fd == STDIN_FILENO){
                    handle_stdin();
                }else if (this_fd == cli_sock){
                    read_from_client(cli_sock, epfd);
                }
            }else if (evlist[i].events & (EPOLLHUP | EPOLLERR)){
                kill_client_connection(epfd,cli_sock);
            }
        }
    }
    return 0;
}