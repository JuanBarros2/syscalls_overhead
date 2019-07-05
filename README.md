# syscalls_overhead

Avaliação de overhead em system calls executadas em linux através de ferramenta
perf e strace.

## Overview

Experimento realizado em distribuição debian através da execução de containers
docker para avaliar overheads em chamadas ao sistema operacional através das 
bibliotecas padrão de linguagem C. Para realizar os experimentos, partimos de 
quatro perguntas:

- *A quantidade de memória alocada por um processo influencia em tempo de execução da Syscall?*
- *A quantidade de processos em execução influencia no tempo de execução da syscall?*
- *A quantidade de arquivos abertos em memória influencia o tempo das system calls?*
- *O tempo de execução das syscalls são prejudicados pelo tempo de pesquisa de arquivo executável?*


## Requisitos

Para executar o experimento completo é necessário ter em sua máquina:

- Docker
- Pandas instalado no python3.6

## Como executar? 

O arquivo [run_all.sh](run_all.sh) encontrado na raiz desse projeto é responsável por gerar todos
os dados necessários para esse experimento, além de executar o script [utils/index.py](utils/index.py)
que é responsável por tratar as entradas e executar o tratamento dos dados, bem 
como gerar um CSV com o resultado de cada hipótese e o o gráfico associado.

Para executar o experimento completo, execute:

```sh run_all.sh```

## Experimento

O experimento cria a pasta chamada ```reports```  que contém quatro subpastas, uma para cada pergunta.
Em cada pasta é possível verificar os arquivos gerados no experimento. Eles geram arquivos de texto 
para a execução dos programas criados em [codes](codes) os quais servem para simular as diversas situações
a serem avaliadas no experimento. Além disso, para cada hipótese é gerado duas pastas que representam
os resultados obtidos rodando dois perfiladores diferentes, o perf e o strace. Em cada subpasta, temos
o nome da chamada que foi executada para obter aquela resposta. O script roda diversas vezes, gerando
várias execuções para cada cenário. A quantidade de vezes que é rodado cada experimento é configurável 
pela variável ```IT``` no script [run_all.sh](run_all.sh). 
