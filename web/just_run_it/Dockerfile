FROM python:3.5-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev

ADD requirements.txt /just_run_it/
RUN pip install -r /just_run_it/requirements.txt
ADD . /just_run_it
WORKDIR /just_run_it
