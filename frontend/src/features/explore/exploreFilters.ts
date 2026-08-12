import type { Destination } from "../../types/flight";

export type SortOption = "price" | "opportunity" | "duration" | "stops";

export interface Filters {
  maxPrice: number | null;
  nonstopOnly: boolean;
  maxDurationMinutes: number | null;
}

export const DEFAULT_FILTERS: Filters = {
  maxPrice: null,
  nonstopOnly: false,
  maxDurationMinutes: null,
};

// Filtros e ordenação olham só para bestOffer de cada destino — v0.2 ainda
// não permite filtrar ofertas individuais dentro de um mesmo destino.
export function applyFilters(destinations: Destination[], filters: Filters): Destination[] {
  return destinations.filter((d) => {
    if (filters.maxPrice !== null && d.bestOffer.price > filters.maxPrice) return false;
    if (filters.nonstopOnly && d.bestOffer.stops > 0) return false;
    if (filters.maxDurationMinutes !== null && d.bestOffer.durationMinutes > filters.maxDurationMinutes) {
      return false;
    }
    return true;
  });
}

// "opportunity" usa o mesmo critério de "price": v0.2 não calcula um índice
// de oportunidade real (ver docs/v0.2/DECISIONS.md) — o preço mais baixo É
// a melhor oportunidade disponível hoje, de forma transparente.
export function sortDestinations(destinations: Destination[], sortBy: SortOption): Destination[] {
  const sorted = [...destinations];
  switch (sortBy) {
    case "price":
    case "opportunity":
      return sorted.sort((a, b) => a.bestOffer.price - b.bestOffer.price);
    case "duration":
      return sorted.sort((a, b) => a.bestOffer.durationMinutes - b.bestOffer.durationMinutes);
    case "stops":
      return sorted.sort((a, b) => a.bestOffer.stops - b.bestOffer.stops);
  }
}
