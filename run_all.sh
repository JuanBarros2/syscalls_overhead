#/bin/bash
docker build -t projso/strace:1.0 .

if [ ! -d "./reports" ] 
then
    mkdir reports
    mkdir ./reports/hip1
    mkdir ./reports/hip4
fi

## Hipotese 1 - Memória influencia em syscall
for syscall in fork execvp clone posix_spawnp
do
    if [ ! -d "./reports/hip1/$syscall" ] 
    then
        mkdir ./reports/hip1/$syscall
    fi

    for memoryLevel in 10 100
    do
        docker run -it projso/strace:1.0 strace -c ./memoriaOverhead $syscall $memoryLevel > ./reports/hip1/$syscall/$memoryLevel.txt
    done
done


## Hipotese 4 - Memória influencia em syscall
for syscall in execv execvp posix_spawn posix_spawnp
do
    docker run -it projso/strace:1.0 strace -c ./pesquisaOverhead $syscall  > ./reports/hip4/$syscall.txt
done

