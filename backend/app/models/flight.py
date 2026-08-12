from pydantic import BaseModel


class Airport(BaseModel):
    code: str
    city: str
    country: str


class FlightOffer(BaseModel):
    id: str
    origin: Airport
    destination: Airport
    airline: str
    departure: str
    arrival: str
    duration_minutes: int
    stops: int
    price: float
    currency: str = "BRL"


class BudgetSearchRequest(BaseModel):
    budget: float
    origin_city: str
    month: str
    flexible: bool = True


class BudgetDestination(BaseModel):
    city: str
    uf: str
    price: float
