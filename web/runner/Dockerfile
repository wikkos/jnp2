FROM python:3.5-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add gcc

ADD runner/run.py /runner/
WORKDIR /runner