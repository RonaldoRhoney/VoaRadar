import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, model_validator

ConditionType = Literal["PRICE_BELOW", "OPPORTUNITY_CLASSIFICATION"]
RadarStatus = Literal["ACTIVE", "PAUSED"]


class RadarCreate(BaseModel):
    name: str
    origin_airport_id: uuid.UUID
    destination_airport_id: uuid.UUID
    departure_date: date | None = None
    return_date: date | None = None
    condition_type: ConditionType
    condition_price: float | None = None
    condition_classification: str | None = None

    @model_validator(mode="after")
    def _condition_matches_type(self) -> "RadarCreate":
        if self.condition_type == "PRICE_BELOW" and self.condition_price is None:
            raise ValueError("condition_price é obrigatório quando condition_type = PRICE_BELOW")
        if self.condition_type == "OPPORTUNITY_CLASSIFICATION" and self.condition_classification is None:
            raise ValueError("condition_classification é obrigatório quando condition_type = OPPORTUNITY_CLASSIFICATION")
        return self

    @model_validator(mode="after")
    def _origin_differs_from_destination(self) -> "RadarCreate":
        if self.origin_airport_id == self.destination_airport_id:
            raise ValueError("Origem e destino não podem ser o mesmo aeroporto")
        return self

    @model_validator(mode="after")
    def _return_not_before_departure(self) -> "RadarCreate":
        if self.departure_date and self.return_date and self.return_date < self.departure_date:
            raise ValueError("A data de volta não pode ser anterior à data de ida")
        return self


class RadarUpdate(BaseModel):
    name: str | None = None
    origin_airport_id: uuid.UUID | None = None
    destination_airport_id: uuid.UUID | None = None
    departure_date: date | None = None
    return_date: date | None = None
    status: RadarStatus | None = None
    condition_type: ConditionType | None = None
    condition_price: float | None = None
    condition_classification: str | None = None


class RadarOut(BaseModel):
    id: uuid.UUID
    name: str
    origin_airport_id: uuid.UUID
    destination_airport_id: uuid.UUID
    departure_date: date | None
    return_date: date | None
    status: RadarStatus
    condition_type: ConditionType
    condition_price: float | None
    condition_classification: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
