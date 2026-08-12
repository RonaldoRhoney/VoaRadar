export interface Airport {
  code: string;
  city: string;
  country: string;
}

export interface FlightOffer {
  id: string;
  origin: Airport;
  destination: Airport;
  airline: string;
  departure: string;
  arrival: string;
  durationMinutes: number;
  stops: number;
  price: number;
  currency: string;
}

export interface SearchParams {
  origin: string;
  destination: string;
  departureDate: string;
  returnDate?: string;
  passengers: number;
}
