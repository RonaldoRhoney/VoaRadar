import { useNavigate } from "react-router-dom";
import { inspireDestinations } from "../data/mockFlights";

export function InspireMe() {
  const navigate = useNavigate();

  return (
    <div id="nao-sei-para-onde-ir" className="scroll-mt-24">
      <p className="mb-4 text-sm text-white/60">
        Escolha um destino e a gente mostra os melhores preços encontrados.
      </p>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {inspireDestinations.map((dest) => (
          <button
            key={dest.code}
            onClick={() => navigate(`/resultados?destino=${dest.code}`)}
            className="group flex flex-col items-start gap-1 rounded-2xl bg-night-800/80 p-5 text-left ring-1 ring-white/10 transition hover:ring-radar-400/60"
          >
            <span className="rounded-full bg-sky-500/15 px-2.5 py-1 text-xs font-medium text-sky-400">
              {dest.tag}
            </span>
            <span className="mt-2 text-lg font-semibold text-white">
              {dest.city}, {dest.country}
            </span>
            <span className="text-sm text-white/50">{dest.code}</span>
            <span className="mt-3 text-2xl font-semibold text-radar-400">
              a partir de R$ {dest.price.toLocaleString("pt-BR")}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
