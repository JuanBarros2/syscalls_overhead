#/bin/bash
echo "Construindo imagem docker..."
docker build -t projso/docker:1.0 .

if [ ! -d "./reports" ] 
then
    echo "Criando pasta para resultados..."
    mkdir reports
    for hip in hip1 hip4
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
        echo ".............." $memoryLevel "niveis de pilha"
        docker run -it projso/docker:1.0 strace -c ./memoriaOverhead $syscall $memoryLevel > ./reports/hip1/strace/$syscall/$memoryLevel.txt
        docker run -it --privileged projso/docker:1.0 perf stat ./memoriaOverhead $syscall $memoryLevel > ./reports/hip1/perf/$syscall/$memoryLevel.txt
    done
done


echo "Gerando dados para hipotese 4 - Path do binário influencia no tempo"
## Hipotese 4 - 
for syscall in execv execvp posix_spawn posix_spawnp
do
    echo ".......Rodando analise para" $syscall 
    docker run -it projso/docker:1.0 strace -c ./pesquisaOverhead $syscall  > ./reports/hip4/strace/$syscall.txt
    docker run --privileged -it projso/docker:1.0 perf stat ./pesquisaOverhead $syscall  > ./reports/hip4/perf/$syscall.txt
done

echo "Processando resultados..."
python3.6 processaGraficos.py

echo "Finalizado"
