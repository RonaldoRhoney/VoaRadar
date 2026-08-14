import uuid
from datetime import datetime

from pydantic import BaseModel


class NotificationOut(BaseModel):
    id: uuid.UUID
    radar_id: uuid.UUID
    type: str
    title: str
    message: str
    read_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
