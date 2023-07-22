#define CHAR_BUF 1024 
struct node{
    int line_number;
    char buf[CHAR_BUF];
    struct node *left;
    struct node *right;
};
struct node* init_node(int line_number, char * buf);
struct node* insert(struct node* root, int new_line_number, char * buf);
void inorder_traverse(struct node* root, int sock_fd);