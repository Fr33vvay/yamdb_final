# YaMDb. Произведения и отзывы.

API-приложение (на основе Django Rest Framework) формирует базу произведений, разделённых на различные категории, 
такие как: "Книги", "Фильмы", "Музыка" и другие. С помощью API-инструментов в базу могут
вноситься данные, при этом с возможностью делать отзывы и комментарии к отзывам. 

## Начало

Эти инструкции позволят вам запустить копию проекта на вашем локальном компьютере в целях разработки и тестирования.

### Предварительные условия

Для установки программного обеспечения понадобятся

* [docker 19.03+](https://www.docker.com/get-started)
* [docker-compose 1.25.0+](https://docs.docker.com/compose/)
* [git](https://github.com/)


### Установка

Для установки необходимо: 
* склонировать репозиторий и создать файл .env с настройками в корневой папке проекта
* создать докер-контейнер, запустить приложение
* открыть консоль для ввода последующих команд 
* накатить миграции
* собрать статические файлы
* при необходимости, загрузить данные из файла fixtures.json (суперпользователь: admin, пароль: 543222)
* при необходимости, создать суперпользователя

```
git clone https://github.com/Fr33vvay/api_yamdb
cd api_yamdb/
docker-compose up
docker exec -it api_yamdb_web_1 bash
python manage.py migrate
python manage.py collectstatic
python manage.py loaddata fixtures.json
python manage.py createsuperuser
```

Для проверки работы откройте в своем браузере: [localhost/api/v1/](http://localhost/api/v1)

## Пример настроек окружения

Пример файла .env можно найти здесь [.env.template](.env.template).
## Создано при помощи
* [Python 3.8](https://www.python.org/downloads/)
* [Django 3.0](https://docs.djangoproject.com/en/3.1/)
* [Django-REST-Framework 3.11](https://www.django-rest-framework.org/)
* [Docker-compose](https://docs.docker.com/compose/)


## Авторы проекта

* [Татьяна Смирнова](https://github.com/Tatyana-Smirnova "github")
* [Илья Коренцвит](https://github.com/Fr33vvay "github")
* [Влад Бармичев](https://github.com/Shindler7 "github")

*2020 год, когорта 4*
