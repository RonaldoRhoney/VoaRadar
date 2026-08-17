from abc import ABC, abstractmethod

from app.schemas.flight import CalendarDay, RawDestination


class FlightProvider(ABC):
    """Fonte de dados de voo. Cada provedor real (Amadeus, Duffel, ...) implementa esta interface.

    Um provider não sabe nada sobre o orçamento do usuário — só devolve os
    destinos e ofertas que encontrar para a origem/mês pedidos. Classificar
    por orçamento é responsabilidade do service.
    """

    @abstractmethod
    def get_destinations(self, origin_city: str, month: str) -> list[RawDestination]:
        raise NotImplementedError

    @abstractmethod
    def get_price_calendar(self, destination_id: str, month: str) -> list[CalendarDay]:
        """Preço por dia do mês (formato "YYYY-MM") pra um destino — base do
        calendário de flexibilidade de datas (DEC-008)."""
        raise NotImplementedError
