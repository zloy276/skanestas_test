import datetime
from typing import Optional

from pydantic import BaseModel


class Schema(BaseModel):
    class Config:
        orm_mode = True


class TimestampSchemaMixin(Schema):
    created_at: datetime.datetime
    updated_at: datetime.datetime


class SoftDeletableSchemaMixin(Schema):
    deleted_at: Optional[datetime.datetime]
    is_deleted: Optional[bool] = False
