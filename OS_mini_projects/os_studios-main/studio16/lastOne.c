#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[]){
    FILE *file;
    int arg_idx;
    unsigned int last_largest_length = 0;
    unsigned int new_length = 0;
    char *ptr;
    char *line;
    size_t size = 0;

    if (argc < 2){
        printf("to run %s, must pass in arguments\n",argv[0]);
        return -1;
    }
    file = fopen(argv[1],"r");
    if (file==NULL){
        printf("file DNE\n");
        return -1;
    }

    while(fscanf(file, "%u ", &new_length) == 1){
        if (new_length > last_largest_length){
            if (last_largest_length != 0){
                free(ptr);
            }
            last_largest_length = new_length;
            ptr = (char *)malloc(last_largest_length + 1);
        }
        ssize_t read = getline(&line, &size, file);
        if (read != -1) {
            for (int i = 0; i < new_length; i++) {
                ptr[i] = line[i];
            }
            ptr[new_length] = '\n';
            printf("%s", ptr);
        }
    }

    free(ptr);
    free(line);    
    fclose(file);
    return 0;
}
