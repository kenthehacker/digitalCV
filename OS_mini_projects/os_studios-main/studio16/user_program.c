#include <stdio.h>

int main(int argc, char *argv[]){
    FILE *file;
    int arg_idx;
    if (argc < 2){
        printf("to run %s, must pass in arguments\n",argv[0]);
        return -1;
    }
    file = fopen(argv[1],"w");
    for(arg_idx = 2; arg_idx<argc; arg_idx++){
        fprintf(file, "%s\n", argv[arg_idx]);
    }
    fclose(file);
    return 0;
}