FROM --platform=linux/arm64 python:3.11-slim-bullseye

RUN apt update && \
    apt install -y locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG=ja_JP.UTF-8
ENV LANGUAGE=ja_JP:ja
ENV LC_ALL=ja_JP.UTF-8
ENV TZ=JST-9
ENV TERM=xterm

RUN apt update
RUN apt install -y chromium=119.0.6045.123-1~deb11u1 --fix-missing
RUN apt install -y chromium-driver=119.0.6045.123-1~deb11u1 --fix-missing

COPY ./requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r ./requirements.txt

COPY ./src ./src

CMD ["python", "./src/main.py"]
