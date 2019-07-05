FROM continuumio/anaconda3

COPY ./codes /app/codes

WORKDIR /app

VOLUME /app

RUN apt-get update &&\
    apt-get install -y build-essential &&\
    apt-get install -y --no-install-recommends linux-perf && \
    ln -s /usr/bin/perf_* /usr/bin/perf && \
    apt-get install -y strace &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

RUN gcc -o /app/codes/memoriaOverhead /app/codes/memoriaOverhead.c &&\
    gcc -o /app/codes/pesquisaOverhead /app/codes/pesquisaOverhead.c &&\
    gcc -o /app/codes/fileOverhead /app/codes/fileOverhead.c &&\
    gcc -o /app/codes/processosOverhead /app/codes/processosOverhead.c &&\
    gcc -o /app/codes/pesquisaOverhead /app/codes/pesquisaOverhead.c
