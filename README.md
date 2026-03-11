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
git@github.com:VladTheDevolper/API-Final-Case.git
```

```
cd API-Final-Case
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
Лайкнуть пост (требуется токен)

```
POST /api/v1/posts/1/like/
Authorization: Bearer <access_token>
```

Запуск тестов

```
pytest
```

## Документация

Документация доступна по адресу:

```
http://127.0.0.1:8000/redoc/
```

## О себе и проекте

Этот проект создан мной в рамках обучения на курсе Яндекс.Практикум. В процессе работы были реализованы:

- API для постов, комментариев, групп и подписок
- JWT-аутентификация
- Тесты для проверки дополнительного функционала (эндпоинтов для Like)
- Функционал лайков к постам (не входило изначально в рамки учебного проекта)