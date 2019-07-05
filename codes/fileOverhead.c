#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sched.h>
#include <spawn.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <dirent.h>

#define PATH_NAME "files/"


int doNothing() {
    return 0;
}

void createFiles(int files, char syscall[]) {
    pid_t pid;
    FILE* array[100];
    char* argv[] = { "sleep" , "0", NULL};

    struct stat st = {0};

    if(stat(PATH_NAME, &st) == -1){
        mkdir(PATH_NAME, 0700);
    }

    for(int i = 0; i<files; i++){
        char x [100] = PATH_NAME;
        sprintf(x, "%sfile%d.txt", PATH_NAME, i);
        array[i] = fopen(x, "w");        
    }

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
    printf("Fechando arquivos\n");
    for(int i = 0; i<files; i++){
        fclose(array[i]);
    }
    remove_directory(PATH_NAME);
    
}

int remove_directory(const char *path)
{
   DIR *d = opendir(path);
   size_t path_len = strlen(path);
   int r = -1;

   if (d)
   {
      struct dirent *p;

      r = 0;

      while (!r && (p=readdir(d)))
      {
          int r2 = -1;
          char *buf;
          size_t len;

          /* Skip the names "." and ".." as we don't want to recurse on them. */
          if (!strcmp(p->d_name, ".") || !strcmp(p->d_name, ".."))
          {
             continue;
          }

          len = path_len + strlen(p->d_name) + 2; 
          buf = malloc(len);

          if (buf)
          {
             struct stat statbuf;

             snprintf(buf, len, "%s/%s", path, p->d_name);

             if (!stat(buf, &statbuf))
             {
                if (S_ISDIR(statbuf.st_mode))
                {
                   r2 = remove_directory(buf);
                }
                else
                {
                   r2 = unlink(buf);
                }
             }

             free(buf);
          }

          r = r2;
      }

      closedir(d);
   }

   if (!r)
   {
      r = rmdir(path);
   }

   return r;
}


int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Numero de argumentos incorreto");
    } else {
        createFiles(atoi(argv[2]), argv[1]);
    }

   return 0;
}