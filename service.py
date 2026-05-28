import psycopg
from psycopg.rows import class_row

from db import COLS, get_schedule_ids, get_schedule_rows
from models import ScheduleCreate, ScheduleOut


def get_schedules(calendar_name: str | None = None) -> list[ScheduleOut]:
    with psycopg.connect() as conn:
        return get_schedule_rows(conn, calendar_name)


def add_schedule(req: ScheduleCreate) -> ScheduleOut | None:
    with psycopg.connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COALESCE(MAX(sort_order), 0) + 1 FROM schedules")
            sort_order = cursor.fetchone()[0]
        with conn.cursor(row_factory=class_row(ScheduleOut)) as cursor:
            cursor.execute(
                f"""
                INSERT INTO schedules (
                    calendar_name,
                    schedule_description,
                    duration_minutes,
                    weekdays,
                    arrange_type,
                    sort_order
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (calendar_name, schedule_description) DO NOTHING
                RETURNING {COLS}
                """,
                (
                    req.calendar_name,
                    req.schedule_description,
                    req.duration_minutes,
                    req.weekdays,
                    req.arrange_type,
                    sort_order,
                ),
            )
            return cursor.fetchone()


def mod_schedule(schedule_id: int, req: ScheduleCreate) -> ScheduleOut | None:
    with psycopg.connect() as conn:
        with conn.cursor(row_factory=class_row(ScheduleOut)) as cursor:
            cursor.execute(
                f"""
                UPDATE schedules
                SET
                    calendar_name = %s,
                    schedule_description = %s,
                    duration_minutes = %s,
                    weekdays = %s,
                    arrange_type = %s
                WHERE id = %s
                RETURNING {COLS}
                """,
                (
                    req.calendar_name,
                    req.schedule_description,
                    req.duration_minutes,
                    req.weekdays,
                    req.arrange_type,
                    schedule_id,
                ),
            )
            return cursor.fetchone()


def del_schedule(schedule_id: int) -> ScheduleOut | None:
    with psycopg.connect() as conn:
        with conn.cursor(row_factory=class_row(ScheduleOut)) as cursor:
            cursor.execute(
                f"DELETE FROM schedules WHERE id = %s RETURNING {COLS}",
                (schedule_id,),
            )
            return cursor.fetchone()


def mod_schedule_order(ids: list[int]) -> list[ScheduleOut] | None:
    with psycopg.connect() as conn:
        current_ids = get_schedule_ids(conn)
        if set(ids) != set(current_ids):
            return None
        with conn.cursor() as cursor:
            cursor.executemany(
                "UPDATE schedules SET sort_order = %s WHERE id = %s",
                [(order, schedule_id) for order, schedule_id in enumerate(ids, 1)],
            )
        return get_schedule_rows(conn)
