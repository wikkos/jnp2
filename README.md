instalacja docker-compose:

```sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose```

budowa i uruchomienie:

```docker-compose build && docker-compose up -d db && docker-compose up front```

tylko baza danych:
```docker-compose up --build db```

[127.0.0.1:8000/accounts/login/](127.0.0.1:8000/accounts/login/)

podłączenie się do uruchomionego kontenera z konsolą
```docker exec -t -i jnp2_front_1 /bin/ash```

koniec:
```docker-compose down```