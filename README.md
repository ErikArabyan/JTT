# Mini User & Project Management API

A small FastAPI REST API for creating users and assigning projects to them.

Built with FastAPI, SQLModel/Pydantic models, async SQLAlchemy sessions, and PostgreSQL.

## Run locally

Fill in `.env` first:

```bash
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

For Docker Compose, `POSTGRES_HOST` should normally be `db`.

```bash
docker-compose up
```

The API is available at `http://localhost:8000`.

Interactive API docs are available at `http://localhost:8000/docs`.