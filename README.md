# API для сервиса YaMDB
### Описание
Благодаря этому проекту можно оценивать фильмы, оставлять коментарии, отзывы.
### Технологии
Python 3.7
Django 2.2.16
Docker

### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
- Запустите docker-compose командой
```
docker-compose up
``` 

- У вас развернётся проект, запущенный через Gunicorn с базой данных Postgres
- При развёртывании проекта, будут установлены зависимости а также запущен локальный сервер по адресу 127.0.0.1
- Далее в терминале, внутри установленного контейнера выполните миграции
``` 
docker-compose exec web python manage.py migrate
```
- Создайте супер-пользователя
``` 
docker-compose exec web python manage.py createsuperuser
```
- Соберите статику
```
docker-compose exec web python manage.py collectstatic
```
### Наслаждайтесь
### Авторы
Denis Razgonyaev