FROM python:3.11.1-slim-bullseye

WORKDIR /usr/src/application
COPY application/ ./
COPY py_libraries.txt ../

# Commands to remove
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install vim -y
# End

RUN pip install --no-cache-dir -r ../py_libraries.txt

CMD ["flask", "--app", "main", "run", "--host=0.0.0.0", "--port=9000"]