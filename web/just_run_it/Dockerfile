FROM python:3.5-alpine
ENV PYTHONUNBUFFERED 1
ADD . /just_run_it
WORKDIR /just_run_it

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev

RUN pip install -r requirements.txt