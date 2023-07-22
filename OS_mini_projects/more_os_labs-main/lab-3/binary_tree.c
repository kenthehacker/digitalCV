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
#include "binary_tree.h"
struct node* init_node(int line_number, char * buf){
    struct node* new_node = (struct node*) malloc(sizeof(struct node));
    new_node->left = NULL;
    new_node->right = NULL;
    new_node->line_number = line_number;
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