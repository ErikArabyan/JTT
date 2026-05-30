# Mini User & Project Management API

A small FastAPI REST API for creating users and assigning projects to them.

Built with FastAPI, SQLModel/Pydantic models, async SQLAlchemy sessions, and PostgreSQL.

## Run locally

Start the app:

```bash
docker compose up
```

Docker Compose includes default PostgreSQL settings, so a freshly cloned repo starts without creating a `.env` file.

To override the defaults, create `.env`:

```bash
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=JTT
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
```

The API is available at `http://localhost:8000`.

Interactive API docs are available at `http://localhost:8000/docs`.
