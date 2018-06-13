start celery worker:
```celery -A tasks worker --loglevel=info -b message-broker```

start celery beat:
```celery -A tasks beat```

start application:
```./run.sh```

stop application:
```docker-compose down```

Application works on:
http://localhost:8000/

RabbitMQ:
http://localhost:15672/#/
login: guest
password: guest
