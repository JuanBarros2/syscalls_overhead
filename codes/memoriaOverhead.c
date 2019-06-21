#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <sched.h>
#include <spawn.h>

#define DEPTH_STACK 50

void doNothing() {
    return;
}

void expandMemory(int depth, char syscall[]) {
    long auxMemory[depth][depth];
    if (depth == 0) {
        if (strcmp(syscall, "fork") == 0){
            /* Cria uma cópia do processo atual e continua a execução
            dos dois processos.*/
            fork();
        } else if(strcmp(syscall, "execv") == 0) {
            char args[] = "";
            execv(*args, *args);
        } else if(strcmp(syscall, "clone") == 0) {
            /* Cria uma thread de execução para o processo atual.
            Recebe um ponteiro de uma função que rodará na execução
            da syscall, um ponteiro para a pilha compartilhada entre
            threads, constantes (nesse caso, CLONE_VFORK define que
            o processo pai deve esperar os filhos terminarem a execução
            para continuar a execução), e ponteiro para argumentos.*/
            clone(*doNothing, NULL, CLONE_VFORK, NULL);
        } else if(strcmp(syscall, "spawn") == 0) {
            posix_spawnp();
        }
    } else {
        expandMemory(depth - 1, syscall);
    }
}


int main(int argc, char *argv[]) {
    if (argc == 1) {
        printf("É preciso ter mais argumentos");
    } else {
        printf("Syscall: %s\n", argv[1]);
        expandMemory(DEPTH_STACK, argv[1]);
    }

   return 0;
}
