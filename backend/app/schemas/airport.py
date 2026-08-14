import uuid

from pydantic import BaseModel


class AirportOut(BaseModel):
    id: uuid.UUID
    code: str
    name: str
    city: str

    model_config = {"from_attributes": True}
