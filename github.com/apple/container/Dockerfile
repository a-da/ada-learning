FROM ubuntu:24.04

COPY main.sh main.sh
RUN mkdir -p 24.04/arch=x86_64
COPY 24.04/arch=x86_64/packages.txt 24.04/arch=x86_64/packages.txt  
RUN bash -x main.sh init

CMD ["bash", "main.sh", 'start']
