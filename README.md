# Schedules API

FastAPI backend for the PostgreSQL `schedules` table in `deploy/schedules.sql`.

## Database

Configure PostgreSQL with libpq environment variables:

```dotenv
PGHOST=localhost
PGDATABASE=schedules
PGUSER=schedules
PGPASSWORD=your-db-password
PGPORT=5432
```

Apply the schema:

```sh
psql -f deploy/schedules.sql
```

## Run

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The service listens on `http://localhost:8000`.

## Endpoints

- `GET /schedules` lists schedules ordered by `sort_order`.
- `GET /schedules?calendar_name=IELTS` filters by calendar.
- `POST /schedules` adds a schedule.
- `PUT /schedules/{id}` replaces a schedule item.
- `DELETE /schedules/{id}` deletes a schedule item.
- `PUT /schedules/order` updates order with a body like `{"ids": [3, 1, 2]}`. The list must contain every schedule id exactly once.
