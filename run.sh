#!/bin/bash

docker-compose build
docker network create just_run_it_net
docker-compose up -d front_db
docker-compose up -d programs_db
docker-compose up -d front
docker-compose up -d programs