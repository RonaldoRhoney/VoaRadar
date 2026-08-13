export type Classification = "EXCELLENT" | "GOOD" | "NORMAL" | "EXPENSIVE" | "VERY_EXPENSIVE";
export type ConfidenceLevel = "LOW" | "MEDIUM" | "HIGH";

export interface PriceHistoryPoint {
  price: number;
  observedAt: string;
}

export interface PriceIntelligence {
  currentPrice: number;
  sampleSize: number;
  confidence: ConfidenceLevel;
  hasSufficientData: boolean;
  minimum: number | null;
  maximum: number | null;
  mean: number | null;
  median: number | null;
  percentageVsMean: number | null;
  percentageVsMin: number | null;
  score: number | null;
  classification: Classification | null;
  history: PriceHistoryPoint[];
}
