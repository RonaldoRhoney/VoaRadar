import { describe, expect, it } from "vitest";
import { applyFilters, DEFAULT_FILTERS, sortDestinations } from "./exploreFilters";
import type { Destination } from "../../types/flight";

function makeDestination(overrides: Partial<Destination> & { id: string }): Destination {
  return {
    city: overrides.city ?? overrides.id,
    uf: "XX",
    budgetStatus: "within_budget",
    highlight: null,
    offers: [],
    ...overrides,
    bestOffer: overrides.bestOffer ?? {
      id: `${overrides.id}-offer`,
      price: 500,
      departureDate: "2026-10-01",
      returnDate: "2026-10-05",
      durationMinutes: 120,
      stops: 0,
      airline: "Azul",
    },
  };
}

describe("applyFilters", () => {
  it("filters by max price using bestOffer", () => {
    const destinations = [
      makeDestination({ id: "A", bestOffer: { id: "a", price: 400, departureDate: "", returnDate: null, durationMinutes: 100, stops: 0, airline: "X" } }),
      makeDestination({ id: "B", bestOffer: { id: "b", price: 900, departureDate: "", returnDate: null, durationMinutes: 100, stops: 0, airline: "X" } }),
    ];

    const result = applyFilters(destinations, { ...DEFAULT_FILTERS, maxPrice: 500 });

    expect(result.map((d) => d.id)).toEqual(["A"]);
  });

  it("filters nonstop only", () => {
    const destinations = [
      makeDestination({ id: "A", bestOffer: { id: "a", price: 400, departureDate: "", returnDate: null, durationMinutes: 100, stops: 1, airline: "X" } }),
      makeDestination({ id: "B", bestOffer: { id: "b", price: 400, departureDate: "", returnDate: null, durationMinutes: 100, stops: 0, airline: "X" } }),
    ];

    const result = applyFilters(destinations, { ...DEFAULT_FILTERS, nonstopOnly: true });

    expect(result.map((d) => d.id)).toEqual(["B"]);
  });
});

describe("sortDestinations", () => {
  const destinations = [
    makeDestination({ id: "A", bestOffer: { id: "a", price: 900, departureDate: "", returnDate: null, durationMinutes: 300, stops: 2, airline: "X" } }),
    makeDestination({ id: "B", bestOffer: { id: "b", price: 400, departureDate: "", returnDate: null, durationMinutes: 100, stops: 0, airline: "X" } }),
  ];

  it("sorts by price and opportunity identically", () => {
    expect(sortDestinations(destinations, "price").map((d) => d.id)).toEqual(["B", "A"]);
    expect(sortDestinations(destinations, "opportunity").map((d) => d.id)).toEqual(["B", "A"]);
  });

  it("sorts by duration", () => {
    expect(sortDestinations(destinations, "duration").map((d) => d.id)).toEqual(["B", "A"]);
  });

  it("sorts by stops", () => {
    expect(sortDestinations(destinations, "stops").map((d) => d.id)).toEqual(["B", "A"]);
  });

  it("does not mutate the original array", () => {
    const original = [...destinations];
    sortDestinations(destinations, "price");
    expect(destinations).toEqual(original);
  });
});
