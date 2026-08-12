from pydantic import BaseModel


class BudgetSearchRequest(BaseModel):
    budget: float
    origin_city: str
    month: str
    flexible: bool = True


class BudgetDestination(BaseModel):
    city: str
    uf: str
    price: float
