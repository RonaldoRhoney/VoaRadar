import type { FlightOffer } from "../types/flight";

export const mockFlights: FlightOffer[] = [
  {
    id: "1",
    origin: { code: "GRU", city: "São Paulo", country: "Brasil" },
    destination: { code: "LIS", city: "Lisboa", country: "Portugal" },
    airline: "TAP Air Portugal",
    departure: "2026-09-10T22:40:00",
    arrival: "2026-09-11T12:05:00",
    durationMinutes: 565,
    stops: 0,
    price: 3489,
    currency: "BRL",
  },
  {
    id: "2",
    origin: { code: "GRU", city: "São Paulo", country: "Brasil" },
    destination: { code: "LIS", city: "Lisboa", country: "Portugal" },
    airline: "Air France",
    departure: "2026-09-10T19:15:00",
    arrival: "2026-09-11T14:30:00",
    durationMinutes: 675,
    stops: 1,
    price: 2950,
    currency: "BRL",
  },
  {
    id: "3",
    origin: { code: "GRU", city: "São Paulo", country: "Brasil" },
    destination: { code: "EZE", city: "Buenos Aires", country: "Argentina" },
    airline: "LATAM",
    departure: "2026-09-12T08:20:00",
    arrival: "2026-09-12T10:50:00",
    durationMinutes: 150,
    stops: 0,
    price: 890,
    currency: "BRL",
  },
  {
    id: "4",
    origin: { code: "GRU", city: "São Paulo", country: "Brasil" },
    destination: { code: "MIA", city: "Miami", country: "Estados Unidos" },
    airline: "American Airlines",
    departure: "2026-09-15T23:55:00",
    arrival: "2026-09-16T07:10:00",
    durationMinutes: 555,
    stops: 0,
    price: 4120,
    currency: "BRL",
  },
];

// MOCK DATA — preços de exemplo, ainda sem integração com fonte real de dados de voo.
export interface BudgetDestination {
  city: string;
  uf: string;
  price: number;
}

export const budgetDestinationsMock: BudgetDestination[] = [
  { city: "Recife", uf: "PE", price: 429 },
  { city: "Fortaleza", uf: "CE", price: 517 },
  { city: "Brasília", uf: "DF", price: 598 },
  { city: "Salvador", uf: "BA", price: 689 },
];

export const inspireDestinations: Array<{
  city: string;
  country: string;
  code: string;
  price: number;
  tag: string;
}> = [
  { city: "Lisboa", country: "Portugal", code: "LIS", price: 2950, tag: "Europa" },
  { city: "Buenos Aires", country: "Argentina", code: "EZE", price: 890, tag: "Perto" },
  { city: "Cidade do México", country: "México", code: "MEX", price: 2340, tag: "América" },
  { city: "Miami", country: "Estados Unidos", code: "MIA", price: 4120, tag: "Praia" },
  { city: "Cusco", country: "Peru", code: "CUZ", price: 1580, tag: "Aventura" },
  { city: "Roma", country: "Itália", code: "FCO", price: 3210, tag: "Europa" },
];
