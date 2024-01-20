FROM python:3.11-slim-bullseye

RUN apt update
RUN pip install --upgrade pip

COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY user_config.jsonc ./
COPY backend/src ./src
RUN apt-get install -y tzdata && \
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

CMD ["python", "./src/main.py"]
