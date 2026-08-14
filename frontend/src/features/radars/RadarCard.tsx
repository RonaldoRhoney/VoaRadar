import { Link } from "react-router-dom";
import type { Airport, Radar } from "../../types/radar";
import { formatCurrencyBRL } from "../../utils/format";

function airportLabel(airports: Airport[], id: string): string {
  const airport = airports.find((a) => a.id === id);
  return airport ? airport.city : "—";
}

function conditionLabel(radar: Radar): string {
  if (radar.conditionType === "PRICE_BELOW") {
    return `Até ${formatCurrencyBRL(radar.conditionPrice ?? 0)}`;
  }
  return "Excelente oportunidade";
}

export function RadarCard({
  radar,
  airports,
  onToggleStatus,
  onDelete,
}: {
  radar: Radar;
  airports: Airport[];
  onToggleStatus: (radar: Radar) => void;
  onDelete: (radarId: string) => void;
}) {
  const isActive = radar.status === "ACTIVE";

  return (
    <div
      className={`flex flex-col gap-2 rounded-2xl p-5 ring-1 ring-white/10 transition ${
        isActive ? "bg-night-800/80" : "bg-night-800/40 opacity-70"
      }`}
    >
      <div className="flex items-start justify-between gap-2">
        <div>
          <p className="font-medium text-white">🔵 {radar.name}</p>
          <p className="mt-1 text-sm text-white/60">
            {airportLabel(airports, radar.originAirportId)} → {airportLabel(airports, radar.destinationAirportId)}
          </p>
          <p className="mt-1 text-sm text-white/60">{conditionLabel(radar)}</p>
        </div>
        <span className={`shrink-0 text-xs font-medium ${isActive ? "text-radar-400" : "text-white/40"}`}>
          {isActive ? "🟢 ATIVO" : "⚪ PAUSADO"}
        </span>
      </div>

      <div className="mt-2 flex flex-wrap items-center gap-3 text-sm">
        <Link to={`/radares/${radar.id}/editar`} className="text-sky-400 hover:underline">
          Editar
        </Link>
        <button onClick={() => onToggleStatus(radar)} className="text-white/70 hover:text-white">
          {isActive ? "Pausar" : "Ativar"}
        </button>
        <button onClick={() => onDelete(radar.id)} className="text-white/50 hover:text-red-400">
          Excluir
        </button>
      </div>
    </div>
  );
}
