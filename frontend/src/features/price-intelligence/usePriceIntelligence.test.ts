import { renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { usePriceIntelligence } from "./usePriceIntelligence";

const wireResponse = {
  current_price: 429,
  sample_size: 6,
  confidence: "LOW",
  has_sufficient_data: true,
  minimum: 429,
  maximum: 531,
  mean: 474,
  median: 462,
  percentage_vs_mean: -9.5,
  percentage_vs_min: 0,
  score: 100,
  classification: "EXCELLENT",
  history: [{ price: 429, observed_at: "2026-08-13T01:35:06.697770Z" }],
};

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("usePriceIntelligence", () => {
  it("starts loading, then resolves with the mapped result", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => wireResponse }));

    const { result } = renderHook(() => usePriceIntelligence("offer-rec-001", 429));

    expect(result.current.status).toBe("loading");

    await waitFor(() => expect(result.current.status).toBe("success"));
    expect(result.current.data?.score).toBe(100);
    expect(result.current.data?.history[0].observedAt).toBe("2026-08-13T01:35:06.697770Z");
  });

  it("maps a 404 to the not-found status, not an error", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 404, json: async () => ({}) }));

    const { result } = renderHook(() => usePriceIntelligence("offer-desconhecida", 500));

    await waitFor(() => expect(result.current.status).toBe("not-found"));
    expect(result.current.data).toBeNull();
  });

  it("exposes a friendly error message on a real failure", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 500, json: async () => ({}) }));

    const { result } = renderHook(() => usePriceIntelligence("offer-rec-001", 429));

    await waitFor(() => expect(result.current.status).toBe("error"));
    expect(result.current.errorMessage).toMatch(/não conseguimos/i);
  });
});
