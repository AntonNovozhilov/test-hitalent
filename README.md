### QA Servis
Небольшой сервис вопросов и ответов.
Тестовое задание для HiTalent
Стек: FastAPI, SQLAlchemy (async), PostgreSQL, Alembic, Docker Compose, тесты на pytest.

#### Эндпоинты
##### Auth

| Метод |  Путь | Описание |
| ----- |----| --------|
| POST |  /auth/login | получить JWT-токен(Авутентифицироваться) |
| GET |  /auth/me | текущий пользователь |

##### Questions

| Метод |  Путь | Описание |
| ----- |----| --------|
| GET |  /questions/ | список вопросов |
| POST |  /questions/ | создать вопрос |
| GET |  /questions/{id} | один вопрос + его ответы |
| DELETE |  /questions/{id} | удалить вопрос (каскадно удалит ответы) |


##### Answers

| Метод |  Путь | Описание |
| ----- |----| --------|
| POST |  /questions/{id}/answers/ | добавить ответ к вопросу |
| GET |  /answers/{id} | получить ответ |
| DELETE |  /answers/{id} | удалить ответ (проверка владельца) 


#### Запуск приложения

Скачайте скрипт
```
git clone git@github.com:AntonNovozhilov/test-hitalent.git
cd src
```
Скопируйте переменные окружения(при необходимости измените данные):
```
cp .env.example .env
```
Запустите всё одной командой:
```
cd ..
docker-compose up --build
```
Откройте Swagger:
```
http://localhost:8000/docs
```
