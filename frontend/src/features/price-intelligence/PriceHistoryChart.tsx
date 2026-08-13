import { formatCurrencyBRL, formatObservedDate } from "../../utils/format";
import type { PriceHistoryPoint } from "../../types/priceIntelligence";

const WIDTH = 320;
const HEIGHT = 96;
const PADDING = 12;

export function PriceHistoryChart({ points }: { points: PriceHistoryPoint[] }) {
  if (points.length < 2) return null;

  const prices = points.map((p) => p.price);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const range = max - min || 1;

  const toX = (index: number) => PADDING + (index / (points.length - 1)) * (WIDTH - PADDING * 2);
  const toY = (price: number) => HEIGHT - PADDING - ((price - min) / range) * (HEIGHT - PADDING * 2);

  const linePoints = points.map((p, i) => `${toX(i)},${toY(p.price)}`).join(" ");

  return (
    <div>
      <svg viewBox={`0 0 ${WIDTH} ${HEIGHT}`} className="w-full" role="img" aria-label="Histórico de preços">
        <polyline points={linePoints} fill="none" stroke="currentColor" strokeWidth={2} className="text-sky-500" />
        {points.map((p, i) => (
          <circle key={i} cx={toX(i)} cy={toY(p.price)} r={3} className="fill-radar-400">
            <title>
              {formatObservedDate(p.observedAt)}: {formatCurrencyBRL(p.price)}
            </title>
          </circle>
        ))}
      </svg>
      <div className="mt-1 flex justify-between text-xs text-white/40">
        <span>{formatObservedDate(points[0].observedAt)}</span>
        <span>{formatObservedDate(points[points.length - 1].observedAt)}</span>
      </div>
    </div>
  );
}
