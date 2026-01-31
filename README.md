# Nighdee

**ВНИМАНИЕ:** Это форк проекта, созданный для того, чтобы не засорять основной репозиторий лишними ветками. Оригинальный проект [здесь](https://github.com/BlackfireZZZ/find_a_walk).

## Описание

Nighdee — это сервис для создания сходок по интересам и присоединения к ним. Пользователи могут создавать события, указывать их тематику, место и время, а другие пользователи могут находить эти события и присоединяться к ним.

## Технический стек

- **Backend**: Python, FastAPI, SQLAlchemy, PostgreSQL, alembic, jwt, bcrypt
- **Frontend**: HTML, CSS, JavaScript, React
- **Tools**: Docker, Docker Compose

## Запуск проекта

### В Docker
```
docker compose up --build
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