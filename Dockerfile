FROM debian

COPY ./codes/memoriaOverhead.c /memoriaOverhead.c

RUN apt-get update &&\
    apt-get install -y build-essential &&\
    apt-get install -y strace &&\
    apt-get clean &&\
    gcc -o /memoriaOverhead /memoriaOverhead.c
