FROM mysql:8-debian

WORKDIR /usr/src/application
COPY application/ ./

# Commands to remove
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install vim -y
# End

# questo python è abbastanza pesante -> python3.9 e pip (20.3.4)
RUN apt-get install python3-pip -y
RUN pip install --no-cache-dir mysql-connector-python

CMD ["python3.9", "main.py"]