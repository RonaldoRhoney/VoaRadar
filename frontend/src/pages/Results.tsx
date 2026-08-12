import { Link, useSearchParams } from "react-router-dom";
import { useBudgetSearch } from "../features/budget-search/useBudgetSearch";
import { formatCurrencyBRL } from "../utils/format";

function LoadingState() {
  return (
    <div className="flex flex-col gap-3" role="status" aria-live="polite">
      {[0, 1, 2].map((i) => (
        <div key={i} className="h-[84px] animate-pulse rounded-2xl bg-night-800/60 ring-1 ring-white/10" />
      ))}
      <span className="sr-only">Buscando destinos dentro do seu orçamento…</span>
    </div>
  );
}

function ErrorState({ message }: { message: string }) {
  return (
    <p role="alert" className="rounded-2xl bg-night-800/80 p-6 text-center text-white/70 ring-1 ring-white/10">
      {message}
    </p>
  );
}

function EmptyState({ budget }: { budget: number }) {
  return (
    <p className="rounded-2xl bg-night-800/80 p-6 text-center text-white/60 ring-1 ring-white/10">
      Não encontramos destinos de exemplo dentro de {formatCurrencyBRL(budget)}. Tente aumentar o orçamento.
    </p>
  );
}

function BudgetResults({
  budget,
  originCity,
  month,
  flexible,
}: {
  budget: number;
  originCity: string;
  month: string;
  flexible: boolean;
}) {
  const { status, destinations, errorMessage } = useBudgetSearch({
    budget,
    originCity,
    month,
    flexible,
  });

  return (
    <section className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <Link to="/" className="text-sm text-sky-400 hover:underline">
        ← Nova busca
      </Link>

      <h1 className="mt-3 text-2xl font-semibold text-white sm:text-3xl">
        🌎 Encontramos destinos que cabem no seu orçamento
      </h1>
      <p className="mt-1 text-sm text-white/50">
        Saindo de {originCity || "sua cidade"}
        {month ? ` em ${month}` : ""} · até {formatCurrencyBRL(budget)} ·{" "}
        <span className="text-white/40">dados de exemplo (mock)</span>
      </p>

      <div className="mt-8 flex flex-col gap-3">
        {status === "loading" && <LoadingState />}
        {status === "error" && <ErrorState message={errorMessage ?? "Algo deu errado."} />}
        {status === "success" && destinations.length === 0 && <EmptyState budget={budget} />}

        {status === "success" &&
          destinations.map((d) => (
            <article
              key={d.city}
              className="flex items-center justify-between rounded-2xl bg-night-800/80 p-5 ring-1 ring-white/10"
            >
              <div>
                <p className="font-medium text-white">
                  {d.city} <span className="text-white/40">— {d.uf}</span>
                </p>
                <p className="text-lg font-semibold text-radar-400">{formatCurrencyBRL(d.price)}</p>
              </div>
              <Link
                to={`/resultados?destino=${encodeURIComponent(d.city)}&preco=${d.price}&origem=${encodeURIComponent(originCity)}`}
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
        <p className="text-3xl font-semibold text-radar-400">{formatCurrencyBRL(preco)}</p>
        <p className="mt-1 text-sm text-white/50">por pessoa, ida</p>
      </article>
    </section>
  );
}

export function Results() {
  const [params] = useSearchParams();
  const orcamento = params.get("orcamento");
  const origemCidade = params.get("origem") ?? "";
  const mes = params.get("mes") ?? "";
  const destino = params.get("destino");
  const preco = params.get("preco");

  if (destino && preco) {
    return <OpportunityDetail destino={destino} preco={Number(preco)} origem={origemCidade} />;
  }

  if (orcamento) {
    return (
      <BudgetResults
        budget={Number(orcamento)}
        originCity={origemCidade}
        month={mes}
        flexible={params.get("flexivel") !== "false"}
      />
    );
  }

  return (
    <section className="mx-auto max-w-2xl px-4 py-10 text-center sm:px-6">
      <Link to="/" className="text-sm text-sky-400 hover:underline">
        ← Nova busca
      </Link>
      <p className="mt-8 text-white/60">Nenhuma busca informada.</p>
    </section>
  );
}
