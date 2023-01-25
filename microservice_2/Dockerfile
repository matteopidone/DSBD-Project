FROM python:3.11.1-slim-bullseye

WORKDIR /usr/src/application
COPY application/ ./
COPY database_schema.json ../

# Commands to remove
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install vim -y
# End

RUN pip install --no-cache-dir mysql-connector-python
RUN pip install --no-cache-dir kafka-python
RUN pip install --no-cache-dir grpcio
RUN pip install --no-cache-dir grpcio-tools
#verificare che gli ultimi due servono

CMD ["python", "main.py"]