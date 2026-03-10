# api_final


## Описание
REST API для сервиса Yatube.
Позволяет:
-Публиковать посты с изображениями
-Комментировать посты
-Объединять посты в группы
-Подписываться на авторов

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:VladTheDevolper/api-final-yatube.git
```

```
cd api_final_yatube
```

Создать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Примеры запросов

Получение JWT-токена:

```
POST /api/v1/jwt/create/
Content-Type: application/json

{
    "username": "user",
    "password": "password"
}
```

Ответ:

```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbG...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbG..."
}
```

Создание поста (требуется токен):

```
POST /api/v1/posts/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "text": "Мой первый пост!",
    "group": 1
}
```

Получение списка постов:

```

GET /api/v1/posts/?limit=5&offset=0
```

Подписка на автора (требуется токен)

```
POST /api/v1/follow/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "following": "username"
}
```

## Документация

Документация доступна по адресу:

```
http://127.0.0.1:8000/redoc/
```