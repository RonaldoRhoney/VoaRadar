from typing import Literal

from pydantic import BaseModel, Field


class Offer(BaseModel):
    id: str
    price: float
    departure_date: str
    return_date: str | None = None
    duration_minutes: int
    stops: int
    airline: str


class RawDestination(BaseModel):
    """Formato que um FlightProvider devolve — sem noção de orçamento do usuário.

    A classificação de orçamento (dentro/próximo) e o destaque de melhor preço
    são calculados pelo service, não pelo provider: um provider real (Amadeus,
    Duffel...) não sabe nada sobre a busca de um usuário específico, só devolve
    destinos e ofertas disponíveis.
    """

    id: str
    city: str
    uf: str
    offers: list[Offer]


class Destination(BaseModel):
    id: str
    city: str
    uf: str
    budget_status: Literal["within_budget", "near_budget"]
    highlight: Literal["best_price"] | None = None
    best_offer: Offer
    offers: list[Offer]


class ExploreRequest(BaseModel):
    origin_city: str = Field(min_length=1)
    budget: float = Field(gt=0)
    month: str = Field(min_length=1)
    flexible: bool = True
    # Coletado e devolvido em `search` (SearchSummary), mas ainda não afeta
    # preço/disponibilidade — MockFlightProvider não tem noção de ocupação.
    # Passa a valer quando um provider real for integrado.
    passengers: int = Field(default=1, ge=1)


class SearchSummary(BaseModel):
    origin_city: str
    budget: float
    month: str
    flexible: bool
    passengers: int


class Metadata(BaseModel):
    result_count: int
    cheapest_price: float | None = None


class ExploreResponse(BaseModel):
    search: SearchSummary
    destinations: list[Destination]
    near_budget: list[Destination]
    metadata: Metadata
