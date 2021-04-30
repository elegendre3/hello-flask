FROM python:3.6-slim

WORKDIR /app

USER root

RUN mkdir /root/.pip

WORKDIR /app
COPY . .

ENTRYPOINT ["run"]
