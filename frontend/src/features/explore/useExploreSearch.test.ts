import { renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { useExploreSearch } from "./useExploreSearch";

const baseParams = { budget: 800, originCity: "Belém", month: "Outubro", flexible: true, passengers: 1 };

const wireResponse = {
  search: { origin_city: "Belém", budget: 800, month: "Outubro", flexible: true, passengers: 1 },
  destinations: [
    {
      id: "REC",
      city: "Recife",
      uf: "PE",
      budget_status: "within_budget",
      highlight: "best_price",
      best_offer: {
        id: "offer-1",
        price: 429,
        departure_date: "2026-10-14",
        return_date: "2026-10-18",
        duration_minutes: 260,
        stops: 1,
        airline: "Azul",
      },
      offers: [],
    },
  ],
  near_budget: [],
  metadata: { result_count: 1, cheapest_price: 429 },
};

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("useExploreSearch", () => {
  it("starts loading, then resolves with the mapped result", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => wireResponse }));

    const { result } = renderHook(() => useExploreSearch(baseParams));

    expect(result.current.status).toBe("loading");

    await waitFor(() => expect(result.current.status).toBe("success"));
    expect(result.current.result?.destinations[0].bestOffer.price).toBe(429);
    expect(result.current.result?.destinations[0].highlight).toBe("best_price");
  });

  it("exposes a friendly error message when the API call fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, json: async () => ({}) }));

    const { result } = renderHook(() => useExploreSearch(baseParams));

    await waitFor(() => expect(result.current.status).toBe("error"));
    expect(result.current.errorMessage).toMatch(/não conseguimos/i);
  });
});
