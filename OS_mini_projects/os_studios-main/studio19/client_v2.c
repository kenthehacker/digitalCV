#include <sys/socket.h>
#include <sys/un.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <netdb.h>
#define BUF_SIZE 1024

int main(int argc, char *argv[]){
    int cli_socket;
    int port_num = 30303;
    struct sockaddr_in address;
    cli_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (cli_socket == -1){
		perror("Client socket fail\n");
		exit(1);
    }
    memset(&address, 0, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_port = htons(port_num);
    address.sin_addr.s_addr = inet_addr("128.252.167.161");
    if (connect(cli_socket, (struct sockaddr *) &address, sizeof(address)) == -1){
        perror("CLIENT connect fail");
		exit(1);
    }
    for (int i = 1; i<=10; i++){
        uint32_t payload = htonl(i);
        int byte_write = write(cli_socket, &payload, sizeof(payload));
        if (byte_write<0){
            perror("CLIENT write Fail");
            exit(1);
        }else if (byte_write < sizeof(payload)){
            printf("Short write detected... killing cli\n");
            break;        
        }
    }
    uint32_t payload = htonl(418);
    int byte_write = write(cli_socket, &payload, sizeof(payload));


    printf("End sending values\n");
    char buffer[1024];
    if (read(cli_socket, buffer, 1024) < 0) {
        perror("read failed");
        exit(0);
    }
    printf("Server response: %s\n", buffer);

    return 0;
}

