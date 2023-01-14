FROM python:3.11.1-slim-bullseye

WORKDIR /usr/src/application
COPY application/ ./

# Commands to remove
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install vim
# End

CMD ["python", "main.py"]
