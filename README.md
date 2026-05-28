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
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python main.py
```

The service listens on `http://localhost:8000`.

## Endpoints

- `GET /schedules` lists schedules.
- `GET /schedules?calendar_name=IELTS` filters by calendar.
- `POST /schedules` adds a schedule.
- `PUT /schedules/{id}` replaces a schedule item.
- `DELETE /schedules/{id}` deletes a schedule item.

## Background Service

`deploy/schedules-api.service` runs the API with systemd from `/home/admin/server`.
Create `/home/admin/server/.env` with the PostgreSQL variables above, then install it:

```sh
sudo cp deploy/schedules-api.service /etc/systemd/system/schedules-api.service
sudo systemctl daemon-reload
sudo systemctl enable --now schedules-api
sudo systemctl status schedules-api
```
