import { Link } from "react-router-dom";
import type { Destination } from "../../types/flight";
import { formatCurrencyBRL, formatDateRange, formatDuration, formatStops } from "../../utils/format";

export function DestinationCard({ destination, detailHref }: { destination: Destination; detailHref: string }) {
  const { bestOffer } = destination;

  return (
    <article className="flex flex-col gap-3 rounded-2xl bg-night-800/80 p-5 ring-1 ring-white/10 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <div className="flex flex-wrap items-center gap-2">
          <p className="font-medium text-white">
            ✈️ {destination.city} <span className="text-white/40">— {destination.id}</span>
          </p>
          {destination.highlight === "best_price" && (
            <span className="rounded-full bg-radar-500/15 px-2 py-0.5 text-xs font-medium text-radar-400">
              ⭐ Melhor oportunidade
            </span>
          )}
          {destination.budgetStatus === "near_budget" && (
            <span className="rounded-full bg-sky-500/15 px-2 py-0.5 text-xs font-medium text-sky-400">
              Perto do seu orçamento
            </span>
          )}
        </div>

        <p className="mt-1 text-sm text-white/50">A partir de</p>
        <p className="text-2xl font-semibold text-radar-400">{formatCurrencyBRL(bestOffer.price)}</p>

        <p className="mt-2 text-xs text-white/40">
          📅 {formatDateRange(bestOffer.departureDate, bestOffer.returnDate)} · ⏱ {formatDuration(bestOffer.durationMinutes)} ·{" "}
          {formatStops(bestOffer.stops)} · {bestOffer.airline}
        </p>

        {destination.offers.length > 1 && (
          <p className="mt-1 text-xs text-white/30">
            + {destination.offers.length - 1} outra{destination.offers.length > 2 ? "s" : ""} data
            {destination.offers.length > 2 ? "s" : ""} disponíve
            {destination.offers.length > 2 ? "is" : "l"}
          </p>
        )}
      </div>

      <Link
        to={detailHref}
        className="shrink-0 rounded-lg bg-sky-500 px-4 py-2 text-center text-sm font-medium text-white transition hover:bg-sky-600"
      >
        Ver oportunidade
      </Link>
    </article>
  );
}
