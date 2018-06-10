FROM python:3.5-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev

ADD requirements.txt /programs/
RUN pip install -r /programs/requirements.txt
ADD . /programs
WORKDIR /programs
