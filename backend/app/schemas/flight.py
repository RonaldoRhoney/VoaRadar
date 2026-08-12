from pydantic import BaseModel, Field


class BudgetSearchRequest(BaseModel):
    budget: float = Field(gt=0)
    origin_city: str = Field(min_length=1)
    month: str = Field(min_length=1)
    flexible: bool = True


class BudgetDestination(BaseModel):
    city: str
    uf: str
    price: float
