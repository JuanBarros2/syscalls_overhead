FROM debian

COPY ./codes/memoriaOverhead.c /memoriaOverhead.c
COPY ./codes/pesquisaOverhead.c /pesquisaOverhead.c

RUN apt-get update &&\
    apt-get install -y build-essential &&\
    apt-get install -y strace &&\
    apt-get clean &&\
    gcc -o /memoriaOverhead /memoriaOverhead.c &&\
    gcc -o pesquisaOverhead /pesquisaOverhead.c 
