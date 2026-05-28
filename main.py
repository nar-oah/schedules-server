from fastapi import FastAPI, HTTPException, status

from models import ScheduleCreate, ScheduleOut
from service import (
    add_schedule,
    del_schedule,
    get_schedules,
    mod_schedule,
)


app = FastAPI(title="Schedules API")


@app.get("/schedules", response_model=list[ScheduleOut])
def get_all_schedules(calendar_name: str | None = None) -> list[ScheduleOut]:
    return get_schedules(calendar_name)


@app.post(
    "/schedules",
    response_model=ScheduleOut,
    status_code=status.HTTP_201_CREATED,
)
def add_one_schedule(req: ScheduleCreate) -> ScheduleOut:
    schedule = add_schedule(req)
    if schedule is None:
        raise HTTPException(status_code=409, detail="schedule already exists")
    return schedule


@app.put("/schedules/{schedule_id}", response_model=ScheduleOut)
def mod_one_schedule(schedule_id: int, req: ScheduleCreate) -> ScheduleOut:
    schedule = mod_schedule(schedule_id, req)
    if schedule is None:
        raise HTTPException(status_code=404, detail="schedule not found")
    return schedule


@app.delete("/schedules/{schedule_id}", response_model=ScheduleOut)
def del_one_schedule(schedule_id: int) -> ScheduleOut:
    schedule = del_schedule(schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="schedule not found")
    return schedule


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
