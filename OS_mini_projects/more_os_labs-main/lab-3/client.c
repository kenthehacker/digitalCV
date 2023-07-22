#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netdb.h>
#include <poll.h>
#include <fcntl.h>


#define CHAR_BUF 1024 

/*
each node represents individual line
all the nodes construct BST
*/
struct node{
    int line_number;
    char buf[CHAR_BUF];
    struct node *left;
    struct node *right;
};
struct node* init_node(int line_number, char * buf){
    struct node* new_node = (struct node*) malloc(sizeof(struct node));
    new_node->left = NULL;
    new_node->right = NULL;
    new_node->line_number = line_number;
    memset(new_node->buf,0,sizeof(new_node->buf));
    strcpy(new_node->buf, buf);
    return new_node;
}
struct node* insert(struct node* root, int new_line_number, char * buf){
    if (root == NULL){
        struct node * new_root = init_node(new_line_number, buf);
        if (new_root == NULL){
            printf("Failed to make new root");
        }
        return new_root;
    }else if (root->line_number < new_line_number){
        root->right = insert(root->right, new_line_number, buf);
    }else{
        root->left = insert(root->left, new_line_number, buf);
    }
    return root;
}
//inorder traversal guaruntees sorted order 
void inorder_traverse(struct node* root, int sock_fd){
    if (root!=NULL){
        inorder_traverse(root->left, sock_fd);
        if (write(sock_fd, root->buf, strlen(root->buf)) < 0) {
            perror("inorder traverse write failed");
            exit(1);
        }
        printf("sent: %s",root->buf);
        inorder_traverse(root->right, sock_fd);
    }
}
//establishes socket connection to server to specified port and ip addy
int connect_to_server(int port_num, char * ip_address){
    int cli_socket;
    struct sockaddr_in address;
    cli_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (cli_socket == -1){
		perror("Client socket fail\n");
		exit(1);
    }
    memset(&address, 0, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_port = htons(port_num);
    address.sin_addr.s_addr = inet_addr(ip_address);
    if (connect(cli_socket, (struct sockaddr *) &address, sizeof(address)) == -1){
        perror("CLIENT connect fail");
		exit(1);
    }
    return cli_socket;
}

void useage(){
    printf("./client <ip_address> <port_number>\n");
    exit(1);
}

/*
uses poll() for multiplexed reads once we read something 
we copy the data to a char buf and store it into a BST
*/
struct node* read_msg(int sock_fd){
    struct pollfd *pollFd;
    int nfd = 1;
    int read_all_srv_msg = 0;
    pollFd = calloc(1, sizeof(struct pollfd));
    char * buffer = NULL;
    size_t buf_size = 0;

    if (pollFd == NULL){
        perror("pollFd calloc");
        exit(1);
    }
    pollFd[0].fd = sock_fd;
    pollFd[0].events = POLLIN | POLLOUT;
    while(1){
        int ready = poll(pollFd, nfd, -1);
        if (read<0){
            perror("poll failed: ");
            exit(1);
        }
        else if (pollFd[0].revents & POLLIN){
            char temp_buf[CHAR_BUF];
            ssize_t bytes_read = read(sock_fd, temp_buf, CHAR_BUF);
            if ( bytes_read < 0) {
                perror("read failed");
                exit(1);
            }else if (bytes_read ==0){
                break;
            }
            buffer = realloc(buffer, buf_size + bytes_read);
            memcpy(buffer + buf_size, temp_buf, bytes_read);
            buf_size += bytes_read;
            read_all_srv_msg = 1;
        }
        else if (read_all_srv_msg == 1){
            //detects whether or not we finished reading everything
            //so we don't block the code
            //enables us to terminate process so socket connection can
            //be killed
            break;
        }
    }
    char *token = NULL;
    int line_number;
    token = strtok(buffer, "\n");
    struct node * root = NULL;
    
    while (token != NULL) {
        sscanf(token, "%d", &line_number);
        char * tmp = (char*)malloc(sizeof(char) * (strlen(token)+1));
        memset(tmp, 0, sizeof(tmp));
        strcpy(tmp,token);
        strcat(tmp, "\n\0");
        root = insert(root, line_number, tmp);
        token = strtok(NULL, "\n");
        free(tmp);
    }
    return root;
}

int main(int argc, char * argv[]){
    if (argc!=3){
        useage();
    }
    int port_number = atoi(argv[2]);
    char * ip = argv[1];
    int sock_fd = connect_to_server(port_number, ip);
    
    struct node * root = read_msg(sock_fd);
    if (root == NULL){
        printf("READ MSG RETURNED NULL\n");
    }
    char payload_msg[CHAR_BUF];
    memset(payload_msg,0,sizeof(payload_msg));
    inorder_traverse(root, sock_fd);
    //inorder traversal sends the messages in sorted order

    close(sock_fd);
    printf("sent message to server\n");
    return 0;
}

