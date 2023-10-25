# fastapi-book-library

## Описание
Технологии: FastAPI, SQLAlchemy, PostgreSQL

## Инструкции

Для запуска приложения необходимо выполнить следующие команды в терминале:
```sh
$ docker-compose up -d --build
$ docker-compose exec web alembic upgrade head
```

Для доступа к интерактивной документации, с помощью которой можно проверить работоспособность API нужно перейти по http://localhost:8888/docs
