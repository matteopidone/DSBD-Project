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

CMD ["python", "main.py"]