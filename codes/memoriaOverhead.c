#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sched.h>
#include <spawn.h>

#define DEPTH_STACK 100

int doNothing() {
    return 0;
}

void expandMemory(int depth, char syscall[]) {
    pid_t pid;
    long auxMemory[depth][depth];
    if (depth == 0) {
        if (strcmp(syscall, "fork") == 0){
            /* Cria uma cópia do processo atual e continua a execução
            dos dois processos.*/
            fork();
        } else if(strcmp(syscall, "execvp") == 0) {
            char *argv[] = {""};
            /* Substitui a imagem do processo atual por um novo
            processo. Recebe o nome da imagem a ser pesquisada e um
            array de argumentos a ser passado. */
            int erro = execvp("ls", argv);
        } else if(strcmp(syscall, "clone") == 0) {
            /* Cria uma thread de execução para o processo atual.
            Recebe um ponteiro de uma função que rodará na execução
            da syscall, um ponteiro para a pilha compartilhada entre
            threads, constantes (nesse caso, CLONE_VFORK define que
            o processo pai deve esperar os filhos terminarem a execução
            para continuar a execução), e ponteiro para argumentos.*/
            clone(&doNothing, NULL, CLONE_VFORK, NULL);
        } else if(strcmp(syscall, "posix_spawnp") == 0) {
            pid_t pid;
            char *argv[] = {""};
            posix_spawnp(&pid, "ls", NULL, NULL, argv, NULL);
        }
    } else {
        expandMemory(depth - 1, syscall);
    }
}


int main(int argc, char *argv[]) {
    if (argc == 1) {
        printf("É preciso ter mais argumentos");
    } else {
        expandMemory(DEPTH_STACK, argv[1]);
    }

   return 0;
}
