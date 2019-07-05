# syscalls_overhead

Avaliação de overhead em system calls executadas em linux através de ferramenta
perf e strace.

## Requisitos

Para executar o experimento completo é necessário ter em sua máquina:

- Docker
- Pandas instalado no python3.6

## Como executar? 

O arquivo run_all.sh encontrado na raiz desse projeto é responsável por gerar todos
os dados necessários para esse experimento, além de executar o script ```utils/index.py```
que é responsável por tratar as entradas e executar o tratamento dos dados, bem 
como gerar um CSV com o resultado de cada hipótese e o o gráfico associado.

Para executar o experimento completo, execute:

```sh run_all.sh```
