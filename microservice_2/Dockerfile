FROM mysql:8-debian

ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_DATABASE=database
# MYSQL_USER : user
# MYSQL_PASSWORD: password
# --default-authentication-plugin=mysql_native_password

WORKDIR /usr/src/application
COPY application/ ./
COPY database_schema.json ../

# Commands to remove
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install vim -y
RUN pip install requests
# End

# questo python è abbastanza pesante -> python3.9 e pip (20.3.4)
RUN apt-get install python3-pip -y
RUN pip install --no-cache-dir mysql-connector-python

CMD ["python3.9", "init.py"]