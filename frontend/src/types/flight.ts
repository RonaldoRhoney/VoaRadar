export type BudgetStatus = "within_budget" | "near_budget";
export type Highlight = "best_price" | null;

export interface Offer {
  id: string;
  price: number;
  departureDate: string;
  returnDate: string | null;
  durationMinutes: number;
  stops: number;
  airline: string;
}

export interface Destination {
  id: string;
  city: string;
  uf: string;
  budgetStatus: BudgetStatus;
  highlight: Highlight;
  bestOffer: Offer;
  offers: Offer[];
}

export interface ExploreParams {
  budget: number;
  originCity: string;
  month: string;
  flexible: boolean;
  passengers: number;
}

export interface ExploreResult {
  search: ExploreParams;
  destinations: Destination[];
  nearBudget: Destination[];
  metadata: {
    resultCount: number;
    cheapestPrice: number | null;
  };
}

export interface CalendarDay {
  date: string;
  price: number;
}

export interface PriceCalendar {
  destinationId: string;
  month: string;
  days: CalendarDay[];
  cheapestDate: string | null;
}
