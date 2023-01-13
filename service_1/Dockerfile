FROM python:3.10.1-alpine

WORKDIR /usr/src/application

COPY application/ .

RUN apk add py3-pip
RUN pip3.10 install prometheus-api-client

CMD ["python", "main.py"]