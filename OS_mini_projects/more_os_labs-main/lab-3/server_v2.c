#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netdb.h>
#include <sys/epoll.h>
#define CHAR_BUF 1024 
#define FILE_INDEX 1
#define PORT_INDEX 2
#define MAX_EVENTS 10
#define BACKLOG 5

struct node{
    int line_number;
    char buf[CHAR_BUF];
    struct node *left;
    struct node *right;
};
struct node* init_node(int line_number, char * buf){
    printf("before making new_node\n");
    struct node* new_node = (struct node*) malloc(sizeof(struct node));
    printf("after making new_node\n");
    new_node->left = NULL;
    new_node->right = NULL;
    new_node->line_number = line_number;
    strncpy(new_node->buf, buf, CHAR_BUF - 1);
    new_node->buf[CHAR_BUF - 1] = '\0';
    return new_node;
}

void inorder_traverse(struct node* root){
    if (root!=NULL){
        inorder_traverse(root->left);
        printf("%s",root->buf);
        inorder_traverse(root->right);
    }
}

void usage(int port_number,int argc){
    if (argc!=3 || port_number == 0){
        printf("USAGE: ./server <filename> <portnumber>\n");
        exit(1);
    }
}
FILE* open_file(char * file_name, char * mode){
    FILE * file = fopen(file_name, mode);
    if (file == NULL){
        perror("file unable to open"); exit(1);
    }
    return file;
}

int init_socket(int port_num){
    struct sockaddr_in serv_addr;
    int sfd;
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

void unload_socket(int epollfd, int socket){
    epoll_ctl(epollfd, EPOLL_CTL_DEL, socket, NULL);
    close(socket);
}
int accept_client(int server_socket, int epollfd, struct epoll_event *events, int cli_idx){
    struct sockaddr_in client_address;
    socklen_t len = sizeof(client_address);
    int client_socket = accept(server_socket, (struct sockaddr *) &client_address, &len);
    if (client_socket > 0){
        printf("Client established %s\n",inet_ntoa(client_address.sin_addr));
    }else{
        perror("failed to accept client"); exit(1);
    }
    struct epoll_event client_event;
    memset(&client_event, 0, sizeof(client_event));
    client_event.events = EPOLLIN | EPOLLRDHUP;
    client_event.data.fd = client_socket;
    if (epoll_ctl(epollfd, EPOLL_CTL_ADD, client_socket, &client_event)<0){
        perror("failed to accept a client"); 
        exit(1);
    }
    
    return client_socket;
}
struct node* insert(struct node * root, int new_line_number, char * buf){
    if (root == NULL){
        printf("NULL\n");
        printf("Before creating new root\n");
        struct node* new_root = init_node(new_line_number, buf);
        printf("After creating new root, line_number: %d, buf: %s\n", new_root->line_number, new_root->buf);
        if (new_root == NULL){
            perror("Failed to make new root");
            exit(1);
        }
        return new_root;
    }else if (root->line_number < new_line_number){
        root->right = insert(root->right, new_line_number, buf);
    }else{
        root->left = insert(root->left, new_line_number, buf);
    }
    return root;
}
void read_from_client(int client_socket, int epollfd, struct node** root){
    char buf[CHAR_BUF];
    memset(buf, 0, sizeof(buf));
    ssize_t byte_read = read(client_socket, buf, CHAR_BUF);
    if (byte_read == 0) {
        printf("cli killed connection\n");
        unload_socket(epollfd, client_socket);
        return;
    } else if (byte_read < 0) {
        perror("read_from_client failed");
        return;
    }
    char *token = NULL;
    int line_number;
    token = strtok(buf, "\n");
    
    struct node * temp_root = NULL;

    while(token!=NULL){
        printf("A\n");
        sscanf(token, "%d", &line_number);
        printf("B\n");
        char * tmp = (char*)malloc(sizeof(char) * (strlen(token)+1));
        printf("C\n");
        memset(tmp, 0, strlen(token) + 1);
        strcpy(tmp,token);
        strcat(tmp, "\n");
        printf("Before INSERTING: %s\n", token);
        *root = insert(*root, line_number, tmp);
        free(tmp);
        printf("After INSERTING: %s\n", token);
        if (root == NULL){
            printf("root is still null\n");
        }
        token = strtok(NULL, "\n");
        
    }
    printf("exited token loop\n");
}

int main(int argc, char *argv[]){
    usage(1,argc);
    char * file_name = argv[FILE_INDEX];
    int port_number = atoi(argv[PORT_INDEX]);
    usage(port_number, argc);
    
    FILE* file = open_file(file_name, "r");

    char ** spec_array = malloc(1*sizeof(char*));
    if (spec_array == NULL){
        perror("malloc spec_array"); exit(1);
    }
    int line_counter = 0;
    char * output_file_name;
    char line[CHAR_BUF]; //char_buf might cause a problem
    while (fgets(line, sizeof(line), file)) {
        if (line_counter == 0){
            output_file_name = malloc(strlen(line) + 1);
            strcpy(output_file_name, line);
            printf("output file: %s",output_file_name);
        }else{
            int spec_index = line_counter-1;
            char ** new_spec_array = realloc(spec_array, line_counter*sizeof(char*));
            if (new_spec_array == NULL){
                perror("realloc"); exit(1);
            }
            spec_array = new_spec_array;
            size_t new_line_len = strcspn(line, "\r\n");
            char *new_line = malloc(new_line_len + 1);
            if (new_line == NULL){
                perror("new line"); exit(1);
            }
            strncpy(new_line, line, new_line_len);
            spec_array[spec_index] = new_line;
        }
        line_counter++;
    }
    

    FILE *spec_files[line_counter-1];
    char *spec_contents[line_counter-1]; //data structure holding contents 
    for(int i = 0; i<line_counter-1; i++){
        spec_files[i] = fopen(spec_array[i],"r");
        fseek(spec_files[i], 0, SEEK_END);
        long file_size = ftell(spec_files[i]);
        rewind(spec_files[i]);
        spec_contents[i] = (char*) malloc(sizeof(char) * file_size);
        fread(spec_contents[i], sizeof(char), file_size, spec_files[i]);
        fclose(spec_files[i]);
    }
    
    int server_socket_fd = init_socket(port_number);
    struct epoll_event events[MAX_EVENTS+1]; //may cause problem

    int epollfd = epoll_create1(0);
    struct epoll_event server_event;
    memset(&server_event, 0, sizeof(server_event));
    server_event.data.fd = server_socket_fd;
    server_event.events = EPOLLIN;
    if (epoll_ctl(epollfd, EPOLL_CTL_ADD, server_socket_fd, &server_event)<0){
        perror("failed to add server to epoll"); 
        exit(1);
    }
    
    struct node * root = NULL;
    int connected_client_counter = 0;
    int num_ready;
    int cli_idx = 0;
    int num_fragments = line_counter-1;
    while(1==1){
        num_ready = epoll_wait(epollfd, events, MAX_EVENTS+1, -1);
        if (num_ready<0) {
            perror("epoll_wait fail "); exit(1);
        }
        for(int i = 0; i<num_ready; i++){
            if (events[i].data.fd == server_socket_fd && cli_idx < num_fragments){
                int new_client_fd = accept_client(server_socket_fd, epollfd, events, cli_idx);
                //send payload to client:
                ssize_t bytes_sent = write(new_client_fd, spec_contents[cli_idx], strlen(spec_contents[cli_idx]));
                if (bytes_sent < strlen(spec_contents[cli_idx])){
                    printf("Short write on spec file %d\n",cli_idx);
                }
                printf("wrote to cli\n");
                connected_client_counter++;
                cli_idx++;
            }else if ((events[i].events & EPOLLIN)){
                read_from_client(events[i].data.fd, epollfd, &root);
            }else if (events[i].events & (EPOLLHUP | EPOLLERR)){
                unload_socket(epollfd, events[i].data.fd);
            }
        }
        if (cli_idx >= num_fragments){
            printf("sent all fragmented messages to all needed number of clients\n");
            for (int i = 0; i < num_fragments; i++) {
                free(spec_contents[i]);
            }
            free(spec_contents);
            inorder_traverse(root);
            break;
        }
    }
    for(int i = 0; i < line_counter - 1; i++) {
        free(spec_array[i]);
    }free(spec_array);
    free(output_file_name);
    fclose(file);
    exit(0);
}






