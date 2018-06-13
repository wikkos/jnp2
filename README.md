start application:
```$./run.sh```

stop application:
```$docker-compose down```

Application works on:
http://localhost:8000/

RabbitMQ:
http://localhost:15672/#/
login: guest
password: guest


celery is currently not working :(

start celery worker:
```
$docker exec -i -t jnp2_front_1 /bin/ash
$cd compiler
$celery -A tasks worker --loglevel=info -b message-broker
```

start celery beat:
```
$docker exec -i -t jnp2_front_1 /bin/ash
$cd compiler
$celery -A tasks beat
```
