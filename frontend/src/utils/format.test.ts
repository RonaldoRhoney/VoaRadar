import { describe, expect, it } from "vitest";
import { formatCurrencyBRL, formatDateRange, formatDuration, formatStops } from "./format";

describe("formatCurrencyBRL", () => {
  it("formats integers with the pt-BR thousands separator", () => {
    expect(formatCurrencyBRL(800)).toBe("R$ 800");
    expect(formatCurrencyBRL(1500)).toBe("R$ 1.500");
  });
});

describe("formatDuration", () => {
  it("formats minutes as Xh or XhYmin", () => {
    expect(formatDuration(260)).toBe("4h20min");
    expect(formatDuration(180)).toBe("3h");
  });
});

describe("formatDateRange", () => {
  it("formats a departure-return range as day/month", () => {
    expect(formatDateRange("2026-10-14", "2026-10-18")).toBe("14/10–18/10");
  });

  it("formats a one-way date without a range", () => {
    expect(formatDateRange("2026-10-14", null)).toBe("14/10");
  });
});

describe("formatStops", () => {
  it("describes 0, 1 and multiple stops", () => {
    expect(formatStops(0)).toBe("voo direto");
    expect(formatStops(1)).toBe("1 escala");
    expect(formatStops(2)).toBe("2 escalas");
  });
});
