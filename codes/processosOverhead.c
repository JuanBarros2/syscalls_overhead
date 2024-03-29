#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sched.h>
#include <spawn.h>
#include <unistd.h>

int doNothing() {
    return 0;
}

void expandProcessos(int depth, char syscall[]) {
    pid_t pid;

    pid_t child_pid;
    for (int i = 0; i < depth; i++) {
        child_pid = fork();
        if (child_pid == 0) {
            sleep(2);
            return;
        }
    }

    char* argv[] = { "sleep" , "0", NULL};
    if (strcmp(syscall, "fork") == 0){
        /* Cria uma cópia do processo atual e continua a execução
        dos dois processos.*/
        fork();
    } else if(strcmp(syscall, "execvp") == 0) {
        /* Substitui a imagem do processo atual por um novo
        processo. Recebe o nome da imagem a ser pesquisada e um
        array de argumentos a ser passado. */
        int erro = execvp(argv[0], argv);
    } else if(strcmp(syscall, "clone") == 0) {
        void *pchild_stack2 = malloc(1024 * 1024);
        if ( pchild_stack2 == NULL ) {
            printf("ERROR: Unable to allocate memory.\n");
            exit(EXIT_FAILURE);
        }
        /* Cria uma thread de execução para o processo atual.
        Recebe um ponteiro de uma função que rodará na execução
        da syscall, um ponteiro para a pilha compartilhada entre
        threads, constantes (nesse caso, CLONE_VFORK define que
        o processo pai deve esperar os filhos terminarem a execução
        para continuar a execução), e ponteiro para argumentos.*/
        clone(&doNothing, pchild_stack2 + (1024 * 1024), CLONE_VFORK, NULL);
    } else if(strcmp(syscall, "posix_spawnp") == 0) {
        pid_t pid; 
        posix_spawnp(&pid, argv[0], NULL, NULL, argv, NULL);
        exit(0);
    }
}


int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Numero de argumentos incorreto");
    } else {
        expandProcessos(atoi(argv[2]), argv[1]);
    }

   return 0;
}
