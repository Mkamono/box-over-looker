FROM python:3.11-slim-bullseye

RUN apt update
RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./src ./src

CMD ["python", "./src/main.py"]
