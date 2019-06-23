FROM debian

COPY ./codes/memoriaOverhead.c /memoriaOverhead.c
COPY ./codes/pesquisaOverhead.c /pesquisaOverhead.c

RUN apt-get update &&\
    apt-get install -y build-essential &&\
    apt-get install -y --no-install-recommends linux-perf && \
    ln -s /usr/bin/perf_* /usr/bin/perf && \
    apt-get install -y strace &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* &&\
    gcc -o /memoriaOverhead /memoriaOverhead.c &&\
    gcc -o pesquisaOverhead /pesquisaOverhead.c 
