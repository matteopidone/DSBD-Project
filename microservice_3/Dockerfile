FROM python:3.11.1-slim-bullseye

WORKDIR /usr/src/application
COPY application/ ./

# Commands to remove
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install vim -y
RUN pip install --no-cache-dir grpcio 
RUN pip install --no-cache-dir grpcio-tools
# End

RUN pip install --no-cache-dir Flask mysql-connector-python

CMD ["flask", "--app", "main", "run", "--host=0.0.0.0", "--port=9000"]