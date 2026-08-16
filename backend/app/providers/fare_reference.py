import uuid
from abc import ABC, abstractmethod

from app.schemas.price_intelligence import AnacReference


class FareReferenceProvider(ABC):
    """Fonte de REFERÊNCIA histórica de tarifa — nunca oferta comprável.

    Diferente de FlightProvider (backend/app/providers/base.py), que
    devolve ofertas específicas e compráveis: um FareReferenceProvider só
    devolve um sinal estatístico (ex: "tarifa média histórica pra essa
    rota"), usado pra enriquecer o Price Intelligence, nunca apresentado
    como preço disponível pra compra (PROVIDER_ARCHITECTURE.md §2).
    """

    @abstractmethod
    def get_reference(self, route_id: uuid.UUID) -> AnacReference | None:
        """None quando não há referência importada pra essa rota — nunca
        inventar/estimar um valor, é melhor não mostrar nada."""
        raise NotImplementedError
