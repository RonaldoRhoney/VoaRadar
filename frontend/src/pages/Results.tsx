import { Link, useSearchParams } from "react-router-dom";
import { mockFlights, budgetDestinationsMock } from "../data/mockFlights";

function formatDuration(minutes: number) {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return `${h}h${m ? ` ${m}min` : ""}`;
}

function formatTime(iso: string) {
  return new Date(iso).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
}

function BudgetResults({ orcamento, origem, mes }: { orcamento: number; origem: string; mes: string }) {
  const destinos = budgetDestinationsMock
    .filter((d) => d.price <= orcamento)
    .sort((a, b) => a.price - b.price);

  return (
    <section className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <Link to="/" className="text-sm text-sky-400 hover:underline">
        ← Nova busca
      </Link>

      <h1 className="mt-3 text-2xl font-semibold text-white sm:text-3xl">
        🌎 Encontramos destinos que cabem no seu orçamento
      </h1>
      <p className="mt-1 text-sm text-white/50">
        Saindo de {origem || "sua cidade"}
        {mes ? ` em ${mes}` : ""} · até R$ {orcamento.toLocaleString("pt-BR")} ·{" "}
        <span className="text-white/40">dados de exemplo (mock)</span>
      </p>

      <div className="mt-8 flex flex-col gap-3">
        {destinos.length === 0 && (
          <p className="rounded-2xl bg-night-800/80 p-6 text-center text-white/60 ring-1 ring-white/10">
            Nenhum destino de exemplo dentro desse orçamento ainda.
          </p>
        )}

        {destinos.map((d) => (
          <article
            key={d.city}
            className="flex items-center justify-between rounded-2xl bg-night-800/80 p-5 ring-1 ring-white/10"
          >
            <div>
              <p className="font-medium text-white">
                {d.city} <span className="text-white/40">— {d.uf}</span>
              </p>
              <p className="text-lg font-semibold text-radar-400">
                R$ {d.price.toLocaleString("pt-BR")}
              </p>
            </div>
            <Link
              to={`/resultados?destino=${encodeURIComponent(d.city)}&preco=${d.price}&origem=${encodeURIComponent(origem)}`}
              className="rounded-lg bg-sky-500 px-4 py-2 text-sm font-medium text-white transition hover:bg-sky-600"
            >
              Ver oportunidade
            </Link>
          </article>
        ))}
      </div>
    </section>
  );
}

function OpportunityDetail({ destino, preco, origem }: { destino: string; preco: number; origem: string }) {
  return (
    <section className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <Link to="/" className="text-sm text-sky-400 hover:underline">
        ← Nova busca
      </Link>

      <h1 className="mt-3 text-2xl font-semibold text-white sm:text-3xl">
        {origem || "Origem"} → {destino}
      </h1>
      <p className="mt-1 text-sm text-white/50">
        <span className="text-white/40">dados de exemplo (mock)</span>
      </p>

      <article className="mt-8 rounded-2xl bg-night-800/80 p-6 ring-1 ring-white/10">
        <p className="text-3xl font-semibold text-radar-400">
          R$ {preco.toLocaleString("pt-BR")}
        </p>
        <p className="mt-1 text-sm text-white/50">por pessoa, ida</p>
      </article>
    </section>
  );
}

export function Results() {
  const [params] = useSearchParams();
  const orcamento = params.get("orcamento");
  const origemCidade = params.get("origem");
  const mes = params.get("mes");
  const destino = params.get("destino");
  const preco = params.get("preco");

  if (destino && preco) {
    return <OpportunityDetail destino={destino} preco={Number(preco)} origem={origemCidade ?? ""} />;
  }

  if (orcamento) {
    return <BudgetResults orcamento={Number(orcamento)} origem={origemCidade ?? ""} mes={mes ?? ""} />;
  }

  const origem = params.get("origem");
  const ida = params.get("ida");
  const flights = destino ? mockFlights.filter((f) => f.destination.code === destino) : mockFlights;

  return (
    <section className="mx-auto max-w-4xl px-4 py-10 sm:px-6">
      <Link to="/" className="text-sm text-sky-400 hover:underline">
        ← Nova busca
      </Link>

      <h1 className="mt-3 text-2xl font-semibold text-white sm:text-3xl">
        {origem && destino ? `${origem} → ${destino}` : "Resultados"}
      </h1>
      <p className="mt-1 text-sm text-white/50">
        {ida ? `Ida em ${new Date(ida).toLocaleDateString("pt-BR")} · ` : ""}
        Dados de exemplo — a busca real ainda será integrada ao backend.
      </p>

      <div className="mt-8 flex flex-col gap-4">
        {flights.length === 0 && (
          <p className="rounded-2xl bg-night-800/80 p-6 text-center text-white/60 ring-1 ring-white/10">
            Nenhum voo de exemplo para esse destino ainda.
          </p>
        )}

        {flights.map((flight) => (
          <article
            key={flight.id}
            className="flex flex-col gap-4 rounded-2xl bg-night-800/80 p-5 ring-1 ring-white/10 sm:flex-row sm:items-center sm:justify-between"
          >
            <div>
              <p className="font-medium text-white">{flight.airline}</p>
              <p className="mt-1 text-sm text-white/60">
                {flight.origin.code} {formatTime(flight.departure)} → {flight.destination.code}{" "}
                {formatTime(flight.arrival)}
              </p>
              <p className="mt-1 text-xs text-white/40">
                {formatDuration(flight.durationMinutes)} ·{" "}
                {flight.stops === 0 ? "voo direto" : `${flight.stops} parada(s)`}
              </p>
            </div>
            <div className="text-left sm:text-right">
              <p className="text-2xl font-semibold text-radar-400">
                R$ {flight.price.toLocaleString("pt-BR")}
              </p>
              <p className="text-xs text-white/40">por pessoa, ida</p>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
