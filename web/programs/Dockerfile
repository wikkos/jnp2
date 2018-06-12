FROM python:3.5-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev && \
    apk add docker

ADD ../runners/languages_map.py /programs/
ADD requirements.txt /programs/
RUN pip install -r /programs/requirements.txt
ADD . /programs
WORKDIR /programs
