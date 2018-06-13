#!/bin/bash

docker-compose build
docker network create just_run_it_net
docker-compose up -d front_db
docker-compose up -d programs_db
docker-compose up -d front
docker-compose up -d programs

docker exec -i -t jnp2_front_1 python manage.py migrate
docker exec -i -t jnp2_programs_1 python manage.py migrate