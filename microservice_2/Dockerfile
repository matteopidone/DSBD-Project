FROM python:3.11.1-slim-bullseye

WORKDIR /usr/src/application
COPY application/ ./
COPY database_schema.json ../
COPY py_libraries.txt ../

# Commands to remove
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install vim -y
# End

RUN pip install --no-cache-dir -r ../py_libraries.txt

CMD ["python", "main.py"]