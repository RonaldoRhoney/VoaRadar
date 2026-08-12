import { renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { useBudgetSearch } from "./useBudgetSearch";

const baseParams = { budget: 800, originCity: "Belém", month: "Outubro", flexible: true };

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("useBudgetSearch", () => {
  it("starts loading, then resolves with the destinations returned by the API", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => [{ city: "Recife", uf: "PE", price: 429 }],
      }),
    );

    const { result } = renderHook(() => useBudgetSearch(baseParams));

    expect(result.current.status).toBe("loading");

    await waitFor(() => expect(result.current.status).toBe("success"));
    expect(result.current.destinations).toEqual([{ city: "Recife", uf: "PE", price: 429 }]);
  });

  it("exposes a friendly error message when the API call fails", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: false, json: async () => ({}) }),
    );

    const { result } = renderHook(() => useBudgetSearch(baseParams));

    await waitFor(() => expect(result.current.status).toBe("error"));
    expect(result.current.errorMessage).toMatch(/não conseguimos/i);
  });
});
