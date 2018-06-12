FROM python:3.5-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add gcc

ADD ../run_template.py /runner/
ADD ../languages_map.py /runner/
ADD run.py /runner/
WORKDIR /runner