import type { ExploreParams, ExploreResult, Offer, Destination } from "../types/flight";
import type { PriceHistoryPoint, PriceIntelligence } from "../types/priceIntelligence";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {}

// O backend fala snake_case (contrato em docs/v0.2/ARCHITECTURE.md); o
// frontend trabalha em camelCase. Este arquivo é a única fronteira entre
// os dois formatos — nada fora daqui deve conhecer o snake_case da API.

interface OfferWire {
  id: string;
  price: number;
  departure_date: string;
  return_date: string | null;
  duration_minutes: number;
  stops: number;
  airline: string;
}

interface DestinationWire {
  id: string;
  city: string;
  uf: string;
  budget_status: "within_budget" | "near_budget";
  highlight: "best_price" | null;
  best_offer: OfferWire;
  offers: OfferWire[];
}

interface ExploreResponseWire {
  search: {
    origin_city: string;
    budget: number;
    month: string;
    flexible: boolean;
    passengers: number;
  };
  destinations: DestinationWire[];
  near_budget: DestinationWire[];
  metadata: {
    result_count: number;
    cheapest_price: number | null;
  };
}

function mapOffer(offer: OfferWire): Offer {
  return {
    id: offer.id,
    price: offer.price,
    departureDate: offer.departure_date,
    returnDate: offer.return_date,
    durationMinutes: offer.duration_minutes,
    stops: offer.stops,
    airline: offer.airline,
  };
}

function mapDestination(destination: DestinationWire): Destination {
  return {
    id: destination.id,
    city: destination.city,
    uf: destination.uf,
    budgetStatus: destination.budget_status,
    highlight: destination.highlight,
    bestOffer: mapOffer(destination.best_offer),
    offers: destination.offers.map(mapOffer),
  };
}

export async function exploreDestinations(params: ExploreParams): Promise<ExploreResult> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/flights/explore`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        budget: params.budget,
        origin_city: params.originCity,
        month: params.month,
        flexible: params.flexible,
        passengers: params.passengers,
      }),
    });
  } catch {
    throw new ApiError("Não conseguimos falar com o servidor agora. Verifique sua conexão e tente novamente.");
  }

  if (!response.ok) {
    throw new ApiError("Não conseguimos encontrar destinos neste momento. Tente novamente em instantes.");
  }

  const body: ExploreResponseWire = await response.json();

  return {
    search: {
      originCity: body.search.origin_city,
      budget: body.search.budget,
      month: body.search.month,
      flexible: body.search.flexible,
      passengers: body.search.passengers,
    },
    destinations: body.destinations.map(mapDestination),
    nearBudget: body.near_budget.map(mapDestination),
    metadata: {
      resultCount: body.metadata.result_count,
      cheapestPrice: body.metadata.cheapest_price,
    },
  };
}

interface PriceHistoryPointWire {
  price: number;
  observed_at: string;
}

interface PriceIntelligenceWire {
  current_price: number;
  sample_size: number;
  confidence: "LOW" | "MEDIUM" | "HIGH";
  has_sufficient_data: boolean;
  minimum: number | null;
  maximum: number | null;
  mean: number | null;
  median: number | null;
  percentage_vs_mean: number | null;
  percentage_vs_min: number | null;
  score: number | null;
  classification: "EXCELLENT" | "GOOD" | "NORMAL" | "EXPENSIVE" | "VERY_EXPENSIVE" | null;
  history: PriceHistoryPointWire[];
}

function mapPriceIntelligence(body: PriceIntelligenceWire): PriceIntelligence {
  const mapPoint = (point: PriceHistoryPointWire): PriceHistoryPoint => ({
    price: point.price,
    observedAt: point.observed_at,
  });

  return {
    currentPrice: body.current_price,
    sampleSize: body.sample_size,
    confidence: body.confidence,
    hasSufficientData: body.has_sufficient_data,
    minimum: body.minimum,
    maximum: body.maximum,
    mean: body.mean,
    median: body.median,
    percentageVsMean: body.percentage_vs_mean,
    percentageVsMin: body.percentage_vs_min,
    score: body.score,
    classification: body.classification,
    history: body.history.map(mapPoint),
  };
}

/** `null` = a oferta ainda não tem histórico coletado (404 da API) — não é
 * erro, é um estado válido que a UI trata separado ("ainda sem dados"). */
export async function fetchPriceIntelligence(
  offerId: string,
  currentPrice: number,
): Promise<PriceIntelligence | null> {
  let response: Response;
  try {
    response = await fetch(
      `${API_BASE_URL}/flights/price-intelligence/${encodeURIComponent(offerId)}?price=${currentPrice}`,
    );
  } catch {
    throw new ApiError("Não conseguimos falar com o servidor agora. Verifique sua conexão e tente novamente.");
  }

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new ApiError("Não conseguimos analisar esse preço agora. Tente novamente em instantes.");
  }

  return mapPriceIntelligence(await response.json());
}
