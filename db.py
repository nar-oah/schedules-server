from psycopg import Connection
from psycopg.rows import class_row

from models import ScheduleOut


COLS = """
    id,
    calendar_name,
    schedule_description,
    duration_minutes,
    weekdays,
    arrange_type,
    sort_order
"""


def get_schedule_rows(
    conn: Connection, calendar_name: str | None = None
) -> list[ScheduleOut]:
    where_sql = "WHERE calendar_name = %s" if calendar_name is not None else ""
    params = (calendar_name,) if calendar_name is not None else ()
    query = f"""
        SELECT {COLS}
        FROM schedules
        {where_sql}
        ORDER BY sort_order, id
    """
    with conn.cursor(row_factory=class_row(ScheduleOut)) as cursor:
        cursor.execute(query, params)
        return list(cursor.fetchall())


def get_schedule_ids(conn: Connection) -> list[int]:
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM schedules ORDER BY sort_order, id")
        return [row[0] for row in cursor.fetchall()]
