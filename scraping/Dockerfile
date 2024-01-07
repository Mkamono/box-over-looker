FROM python:3.11-slim-bullseye

RUN apt update && \
    apt install -y locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG=ja_JP.UTF-8
ENV LANGUAGE=ja_JP:ja
ENV LC_ALL=ja_JP.UTF-8
ENV TZ=JST-9
ENV TERM=xterm

COPY ./requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r ./requirements.txt

COPY ./src ./src

CMD ["python", "./src/main.py"]
