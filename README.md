# Nighdee

**ВНИМАНИЕ:** Это форк проекта, созданный для того, чтобы не засорять основной репозиторий лишними ветками. Оригинальный проект [здесь](https://github.com/BlackfireZZZ/find_a_walk).

## Описание

Nighdee — это сервис для создания сходок по интересам и присоединения к ним. Пользователи могут создавать события, указывать их тематику, место и время, а другие пользователи могут находить эти события и присоединяться к ним.

## Функционал
### Backend
- Поддержка миграций базы данных
- Покрытие unit- и integration-тестами
- Авторизация через JWT-токены (refresh + access)
### Frontend
- Интеграция OpenStreetMap API
- Адаптивная вёрстка под мобильные устройства
### DevOps
- Запуск проекта в Docker в двух режимах (dev + prod)
- Проксирование запросов на nginx
### Other
- Регулярный рефакторинг проекта: DRY, YAGNI, KISS

## Технический стек

- **Backend**: Python, FastAPI, SQLAlchemy, PostgreSQL, alembic, jwt, bcrypt, pytest
- **Frontend**: HTML, CSS, JavaScript, React
- **DevOps**: Docker, Docker Compose, Nginx

## Запуск проекта

### В Docker
**Development environment**
```
docker compose up --build
```
**Production environment**
```
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### Локально
```
cd backend
python -m app.main
```

```
cd frontend
npm start
```

### Запуск тестов (со статистикой)
```
cd backend/tests
pytest --duration=0
```