from typing import Literal

from pydantic import BaseModel, Field, field_validator


ArrangeType = Literal["early", "late", "auto"]


class ScheduleBase(BaseModel):
    calendar_name: str = Field(min_length=1)
    schedule_description: str = Field(min_length=1)
    duration_minutes: int = Field(gt=0)
    weekdays: list[int] = Field(min_length=1)
    arrange_type: ArrangeType

    @field_validator("weekdays")
    @classmethod
    def get_valid_weekdays(cls, value: list[int]) -> list[int]:
        if not all(0 <= day <= 6 for day in value):
            raise ValueError("weekdays must contain values from 0 to 6")
        return value


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleOut(ScheduleBase):
    id: int
    sort_order: int


class ScheduleOrderMod(BaseModel):
    ids: list[int] = Field(min_length=1)

    @field_validator("ids")
    @classmethod
    def get_unique_ids(cls, value: list[int]) -> list[int]:
        if len(value) != len(set(value)):
            raise ValueError("ids must be unique")
        return value
