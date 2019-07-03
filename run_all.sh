#/bin/bash
echo "Construindo imagem docker..."
docker build -t projso/docker:1.0 .

IT=30

if [ ! -d "./reports" ] 
then
    echo "Criando pasta para resultados..."
    mkdir reports
    for hip in hip1 hip3 hip4
    do
        mkdir ./reports/$hip
        mkdir ./reports/$hip/perf
        mkdir ./reports/$hip/strace
    done
fi

## Hipotese 1 - Memória influencia em syscall
echo "Gerando dados para hipotese 1 - Memoria influencia em tempo de Syscall"
for syscall in fork execvp clone posix_spawnp
do
    for tool in strace perf
    do
        if [ ! -d "./reports/hip1/$tool/$syscall" ] 
        then
            mkdir ./reports/hip1/$tool/$syscall
        fi
    done
    echo ".......Rodando analise para" $syscall 
    for memoryLevel in 10 100
    do
        for count in $(seq 1 $IT);
        do
            echo ".............. Gerando resultado $count para $memoryLevel de niveis de pilha"
            docker run -it projso/docker:1.0 strace -f -T -a 120 ./memoriaOverhead $syscall $memoryLevel > ./reports/hip1/strace/$syscall/$memoryLevel-$count.txt
            docker run -it --privileged projso/docker:1.0 perf trace ./memoriaOverhead $syscall $memoryLevel > ./reports/hip1/perf/$syscall/$memoryLevel-$count.txt
        done
    done
done

## Hipotese 3 - Número de arquivos abertos na memória
echo "Gerando dados para hipotese 3 - Memoria número de arquivos abertos"
for syscall in fork execvp clone posix_spawnp
do
    for tool in strace perf
    do
        if [ ! -d "./reports/hip3/$tool/$syscall" ] 
        then
            mkdir ./reports/hip3/$tool/$syscall
        fi
    done
    echo ".......Rodando analise para" $syscall 
    for memoryLevel in 10 100
    do
        for count in $(seq 1 $IT);
        do
            echo ".............. Gerando resultado $count para $memoryLevel de niveis de pilha"
            docker run -it projso/docker:1.0 strace -f -T -a 120 ./fileOverhead $syscall $memoryLevel > ./reports/hip3/strace/$syscall/$memoryLevel-$count.txt
            docker run -it --privileged projso/docker:1.0 perf trace ./fileOverhead $syscall $memoryLevel > ./reports/hip3/perf/$syscall/$memoryLevel-$count.txt
        done
    done
done

echo "Gerando dados para hipotese 4 - Path do binário influencia no tempo"
## Hipotese 4 - 
for syscall in execv execvp posix_spawn posix_spawnp
do
    for count in $(seq 1 $IT);
        do
        echo ".......Rodando analise $count para $syscall" 
        docker run -it projso/docker:1.0 strace -f -T -a 120 ./pesquisaOverhead $syscall  > ./reports/hip4/strace/$syscall-$count.txt
        docker run --privileged -it projso/docker:1.0 perf trace ./pesquisaOverhead $syscall  > ./reports/hip4/perf/$syscall-$count.txt
    done
done

echo "Processando resultados..."
python3.6 ./utils/index.py

echo "Finalizado"
