FROM python:3.11-slim-bullseye

RUN apt update && apt install -y git

RUN pip install --upgrade pip

ENV BACKEND_PORT=8001
ENV SCRAPING_HOST=http://host.docker.internal:8000

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./src ./src
