import { describe, expect, it } from "vitest";
import { formatCurrencyBRL } from "./format";

describe("formatCurrencyBRL", () => {
  it("formats integers with the pt-BR thousands separator", () => {
    expect(formatCurrencyBRL(800)).toBe("R$ 800");
    expect(formatCurrencyBRL(1500)).toBe("R$ 1.500");
  });
});
