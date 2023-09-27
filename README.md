# Проект ReviewService
**Проект ReviewService - сервис, который собирает отзывы пользователей на произведения.**   
Сами произведения в сервисе не хранятся. 
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Список категорий может быть расширен. Произведению может быть присвоен жанр из списка предустановленных.  
Добавлять произведения, категории и жанры может только администратор.  
Пользователям доступна возможность оставлять к произведениям текстовые отзывы и ставить произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.  
Пользователи могут оставлять комментарии к отзывам.  
Добавлять отзывы, комментарии и ставить оценки могут только авторизованные пользователи.

**Разработан backend и API для сервиса.**  
## Стек технологий:
- Python 3
- Django 3.2
- DRF
- SQLite

## Как запустить проект в dev-режиме:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Elllym-em/review_service_api.git
```
```
cd review_service_api
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
* Если у вас Linux/macOS
    ```
    source env/bin/activate
    ```
* Если у вас windows
    ```
    source env/scripts/activate
    ```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить команду импорта данных в БД:
```
python3 manage.py import_data
```
Запустить проект:
```
python3 manage.py runserver
```
## Примеры запросов API (
### Полная документация к API доступна после запуска dev-режима по ссылке http://127.0.0.1:8000/redoc/

### Запрос на получение списка произведений (GET):
```
/api/v1/titles/
```
**Пример ответа:**
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```
### Запрос на добавление жанра (POST):
```
/api/v1/genres/
```
```
{
  "name": "string",
  "slug": "string"
}
```
**Пример ответа:**
```
{
  "name": "string",
  "slug": "string"
}
```
### Запрос на получение списка отзывов к произведению (GET):
```
/api/v1/titles/{title_id}/reviews/
```
**Пример ответа:**
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
### Запрос на добавление отзыва к произведению (POST):
```
/api/v1/titles/{title_id}/reviews/
```
**Пример ответа:**
```
{
  "text": "string",
  "score": 1
}
```
### Запрос на получение списка всех комментариев к отзыву (GET):
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
**Пример ответа:**
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
### Запрос на удаление комментария к отзыву (DELETE):
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

**Авторы:**
- [Платон Попов](https://github.com/BetterCallTheAmbulance)
- [Элина Мустафаева](https://github.com/Elllym-em)
- [Кирилл Бовин](https://github.com/Kirill-Bovin/)
