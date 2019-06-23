#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sched.h>
#include <spawn.h>

void doSyscall(char syscall[]) {
    pid_t pid;

    char* argv[] = { "sleep" , "0", NULL};
    if (strcmp(syscall, "execv") == 0){
        execv("/bin/sleep", argv);
    } else if(strcmp(syscall, "execvp") == 0) {
        execvp("sleep", argv);
    } else if(strcmp(syscall, "posix_spawn") == 0) {
        posix_spawn(&pid, "/bin/sleep", NULL, NULL, argv, NULL);
    } else if(strcmp(syscall, "posix_spawnp") == 0) {
        posix_spawnp(&pid, "sleep", NULL, NULL, argv, NULL);
    }
}


int main(int argc, char *argv[]) {
    if (argc == 1) {
        printf("É preciso ter mais argumentos");
    } else {
        doSyscall(argv[1]);
    }

    return 0;
}
