FROM ubuntu:22.10

WORKDIR /usr/src/application

COPY application/ .

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3.10 python3-pip
RUN pip3 install prometheus-api-client

CMD ["python3.10", "main.py"]