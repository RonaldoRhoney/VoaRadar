from abc import ABC, abstractmethod

from app.schemas.flight import RawDestination


class FlightProvider(ABC):
    """Fonte de dados de voo. Cada provedor real (Amadeus, Duffel, ...) implementa esta interface.

    Um provider não sabe nada sobre o orçamento do usuário — só devolve os
    destinos e ofertas que encontrar para a origem/mês pedidos. Classificar
    por orçamento é responsabilidade do service.
    """

    @abstractmethod
    def get_destinations(self, origin_city: str, month: str) -> list[RawDestination]:
        raise NotImplementedError
