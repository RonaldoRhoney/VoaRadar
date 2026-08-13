import { usePriceIntelligence } from "./usePriceIntelligence";
import { PriceHistoryChart } from "./PriceHistoryChart";
import { formatCurrencyBRL, formatPercentage } from "../../utils/format";
import type { Classification, ConfidenceLevel } from "../../types/priceIntelligence";

const CLASSIFICATION_LABELS: Record<Classification, string> = {
  EXCELLENT: "🟢 Excelente oportunidade",
  GOOD: "🟢 Boa oportunidade",
  NORMAL: "🟡 Preço normal",
  EXPENSIVE: "🟠 Acima da média",
  VERY_EXPENSIVE: "🔴 Preço alto",
};

const CONFIDENCE_LABELS: Record<ConfidenceLevel, string> = {
  HIGH: "🟢 Alta confiança",
  MEDIUM: "🟡 Confiança moderada",
  LOW: "⚪ Poucos dados",
};

function Loading() {
  return (
    <div role="status" aria-live="polite" className="h-[120px] animate-pulse rounded-2xl bg-night-800/60 ring-1 ring-white/10" />
  );
}

function NotFound() {
  return (
    <p className="rounded-2xl bg-night-800/80 p-5 text-sm text-white/60 ring-1 ring-white/10">
      📊 Ainda não temos dados suficientes para analisar este preço.
    </p>
  );
}

function ErrorState({ message }: { message: string }) {
  return (
    <p role="alert" className="rounded-2xl bg-night-800/80 p-5 text-sm text-white/60 ring-1 ring-white/10">
      {message}
    </p>
  );
}

export function PriceIntelligenceView({ offerId, currentPrice }: { offerId: string; currentPrice: number }) {
  const { status, data, errorMessage } = usePriceIntelligence(offerId, currentPrice);

  if (status === "loading") return <Loading />;
  if (status === "not-found") return <NotFound />;
  if (status === "error") return <ErrorState message={errorMessage ?? "Algo deu errado."} />;
  if (!data!.hasSufficientData) return <NotFound />;

  const { classification, confidence, percentageVsMean, mean, minimum, maximum, score, sampleSize, history } =
    data!;

  return (
    <div className="rounded-2xl bg-night-800/80 p-5 ring-1 ring-white/10">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h3 className="text-sm font-medium text-white/70">Análise de preço</h3>
        {classification && (
          <span className="text-sm font-medium text-white">{CLASSIFICATION_LABELS[classification]}</span>
        )}
      </div>

      {confidence === "LOW" && (
        <p className="mt-2 text-xs text-white/40">
          Ainda estamos aprendendo esta rota — {sampleSize} observação{sampleSize !== 1 ? "ões" : ""}.
        </p>
      )}

      {percentageVsMean !== null && mean !== null && (
        <p className="mt-2 text-sm text-white/60">
          O preço atual está <span className="font-medium text-radar-400">{formatPercentage(percentageVsMean)}</span>{" "}
          em relação à média observada ({formatCurrencyBRL(mean)}).
        </p>
      )}

      <dl className="mt-4 grid grid-cols-2 gap-3 text-sm sm:grid-cols-4">
        <div>
          <dt className="text-xs text-white/40">Menor já visto</dt>
          <dd className="text-white">{minimum !== null ? formatCurrencyBRL(minimum) : "—"}</dd>
        </div>
        <div>
          <dt className="text-xs text-white/40">Média</dt>
          <dd className="text-white">{mean !== null ? formatCurrencyBRL(mean) : "—"}</dd>
        </div>
        <div>
          <dt className="text-xs text-white/40">Maior já visto</dt>
          <dd className="text-white">{maximum !== null ? formatCurrencyBRL(maximum) : "—"}</dd>
        </div>
        <div>
          <dt className="text-xs text-white/40">Score</dt>
          <dd className="text-white">{score !== null ? `${score}/100` : "—"}</dd>
        </div>
      </dl>

      {history.length >= 2 && (
        <div className="mt-4">
          <PriceHistoryChart points={history} />
        </div>
      )}

      <div className="mt-4 flex flex-wrap items-center justify-between gap-2 text-xs text-white/40">
        <span>{CONFIDENCE_LABELS[confidence]}</span>
        <span>Análise baseada no histórico disponível pelo Voa Radar.</span>
      </div>
    </div>
  );
}
