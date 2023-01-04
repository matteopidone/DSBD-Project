FROM python:3.11.1-alpine

WORKDIR /usr/src/application

COPY application/ .
RUN pip install --no-cache-dir prometheus_api_client

CMD ["python", "main.py"]


