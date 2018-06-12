FROM python:3.5-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev g++

ADD run.py /runner/
WORKDIR /runner
