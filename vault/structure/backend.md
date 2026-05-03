# Backend

- **Стек:** Python 3.13+, FastAPI, SQLModel, SQLite, Alembic, uv.
- **Точка входа:** `backend/main.py`, приложение в `backend/app/`.
- **Модели и API:** `backend/app/models.py`, `schemas.py`, `crud.py`, `main.py` (роуты).
- **БД:** `backend/app/db.py`, миграции в `backend/alembic/versions/`.
- **Сиды:** `backend/app/seed.py`.

При новых эндпоинтах: схемы Pydantic, CRUD, согласованность с клиентом.
