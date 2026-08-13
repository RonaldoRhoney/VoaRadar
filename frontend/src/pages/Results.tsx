import { useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { DestinationCard } from "../features/explore/DestinationCard";
import {
  applyFilters,
  DEFAULT_FILTERS,
  sortDestinations,
  type Filters,
  type SortOption,
} from "../features/explore/exploreFilters";
import { useExploreSearch } from "../features/explore/useExploreSearch";
import { PriceIntelligenceView } from "../features/price-intelligence/PriceIntelligenceView";
import type { Destination, ExploreParams, Offer } from "../types/flight";
import { formatCurrencyBRL, formatDateRange, formatDuration, formatStops } from "../utils/format";

function LoadingState() {
  return (
    <div className="flex flex-col gap-3" role="status" aria-live="polite">
      <p className="mb-1 text-sm text-white/60">🔎 Procurando oportunidades para você...</p>
      {[0, 1, 2].map((i) => (
        <div key={i} className="h-[96px] animate-pulse rounded-2xl bg-night-800/60 ring-1 ring-white/10" />
      ))}
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

function backToSearchHref(params: ExploreParams) {
  const qs = new URLSearchParams({
    orcamento: String(params.budget),
    origem: params.originCity,
    mes: params.month,
    flexivel: String(params.flexible),
    passageiros: String(params.passengers),
  });
  return `/resultados?${qs.toString()}`;
}

function FiltersPanel({ filters, onChange }: { filters: Filters; onChange: (f: Filters) => void }) {
  return (
    <div className="grid grid-cols-1 gap-4 rounded-2xl bg-night-800/80 p-4 ring-1 ring-white/10 sm:grid-cols-3">
      <label className="flex flex-col gap-1 text-xs text-white/60">
        Preço máximo
        <input
          type="number"
          min={0}
          placeholder="sem limite"
          value={filters.maxPrice ?? ""}
          onChange={(e) => onChange({ ...filters, maxPrice: e.target.value ? Number(e.target.value) : null })}
          className="rounded-lg border border-white/10 bg-night-900 px-2.5 py-2 text-white outline-none focus:border-sky-500"
        />
      </label>

      <label className="flex flex-col gap-1 text-xs text-white/60">
        Duração máxima (min)
        <input
          type="number"
          min={0}
          placeholder="sem limite"
          value={filters.maxDurationMinutes ?? ""}
          onChange={(e) =>
            onChange({ ...filters, maxDurationMinutes: e.target.value ? Number(e.target.value) : null })
          }
          className="rounded-lg border border-white/10 bg-night-900 px-2.5 py-2 text-white outline-none focus:border-sky-500"
        />
      </label>

      <label className="flex items-center gap-2 self-end text-xs text-white/60">
        <input
          type="checkbox"
          checked={filters.nonstopOnly}
          onChange={(e) => onChange({ ...filters, nonstopOnly: e.target.checked })}
          className="h-4 w-4 accent-sky-500"
        />
        Somente voos diretos
      </label>
    </div>
  );
}

function ExploreResultsView({ params, destinations, nearBudget }: {
  params: ExploreParams;
  destinations: Destination[];
  nearBudget: Destination[];
}) {
  const [sortBy, setSortBy] = useState<SortOption>("price");
  const [filters, setFilters] = useState<Filters>(DEFAULT_FILTERS);
  const [showFilters, setShowFilters] = useState(false);
  const [showNearBudget, setShowNearBudget] = useState(false);

  const visible = useMemo(
    () => sortDestinations(applyFilters(destinations, filters), sortBy),
    [destinations, filters, sortBy],
  );

  const hasFiltersActive =
    filters.maxPrice !== null || filters.maxDurationMinutes !== null || filters.nonstopOnly;

  return (
    <section className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <Link to="/" className="text-sm text-sky-400 hover:underline">
        ← Nova busca
      </Link>

      {destinations.length > 0 ? (
        <>
          <h1 className="mt-3 text-2xl font-semibold text-white sm:text-3xl">
            Encontramos {destinations.length} possibilidade{destinations.length > 1 ? "s" : ""}.
          </h1>
          <p className="mt-1 text-sm text-white/50">
            Saindo de {params.originCity || "sua cidade"} • {params.month} • até{" "}
            {formatCurrencyBRL(params.budget)} · <span className="text-white/40">dados de exemplo (mock)</span>
          </p>

          <div className="mt-5 flex flex-wrap items-center gap-3">
            <button
              onClick={() => setShowFilters((v) => !v)}
              className="rounded-lg border border-white/10 px-3 py-1.5 text-sm text-white/70 hover:text-white"
            >
              Filtros{hasFiltersActive ? " •" : ""}
            </button>

            <label className="ml-auto flex items-center gap-2 text-sm text-white/60">
              Ordenar
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as SortOption)}
                className="rounded-lg border border-white/10 bg-night-900 px-2.5 py-1.5 text-white outline-none focus:border-sky-500"
              >
                <option value="price">Menor preço</option>
                <option value="opportunity">Melhor oportunidade</option>
                <option value="duration">Menor duração</option>
                <option value="stops">Menos escalas</option>
              </select>
            </label>
          </div>

          {showFilters && (
            <div className="mt-3">
              <FiltersPanel filters={filters} onChange={setFilters} />
            </div>
          )}

          <div className="mt-6 flex flex-col gap-3">
            {visible.length === 0 && (
              <p className="rounded-2xl bg-night-800/80 p-6 text-center text-white/60 ring-1 ring-white/10">
                Nenhum resultado com esses filtros.{" "}
                <button onClick={() => setFilters(DEFAULT_FILTERS)} className="text-sky-400 hover:underline">
                  Limpar filtros
                </button>
              </p>
            )}
            {visible.map((d) => (
              <DestinationCard
                key={d.id}
                destination={d}
                detailHref={`${backToSearchHref(params)}&destino=${d.id}&oferta=${d.bestOffer.id}`}
              />
            ))}
          </div>
        </>
      ) : (
        <>
          <h1 className="mt-3 text-2xl font-semibold text-white sm:text-3xl">
            Não encontramos oportunidades até {formatCurrencyBRL(params.budget)}.
          </h1>
          {nearBudget.length > 0 && (
            <p className="mt-2 text-white/60">
              Encontramos opções a partir de {formatCurrencyBRL(nearBudget[0].bestOffer.price)}.
            </p>
          )}
          <p className="mt-1 text-sm text-white/40">
            Tente aumentar o orçamento, ampliar o período ou aceitar uma escala.
          </p>

          {nearBudget.length > 0 && !showNearBudget && (
            <button
              onClick={() => setShowNearBudget(true)}
              className="mt-4 rounded-lg bg-sky-500 px-4 py-2 text-sm font-medium text-white transition hover:bg-sky-600"
            >
              Ver opções
            </button>
          )}

          {showNearBudget && (
            <div className="mt-6 flex flex-col gap-3">
              {nearBudget.map((d) => (
                <DestinationCard
                  key={d.id}
                  destination={d}
                  detailHref={`${backToSearchHref(params)}&destino=${d.id}&oferta=${d.bestOffer.id}`}
                />
              ))}
            </div>
          )}
        </>
      )}
    </section>
  );
}

function OfferDetail({
  params,
  destination,
  offer,
}: {
  params: ExploreParams;
  destination: Destination;
  offer: Offer;
}) {
  return (
    <section className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <Link to={backToSearchHref(params)} className="text-sm text-sky-400 hover:underline">
        ← Voltar para os resultados
      </Link>

      <h1 className="mt-3 text-2xl font-semibold text-white sm:text-3xl">
        {params.originCity || "Origem"} → {destination.city}
        <span className="text-white/40"> ({destination.id})</span>
      </h1>
      <p className="mt-1 text-sm text-white/50">
        <span className="text-white/40">dados de exemplo (mock)</span>
      </p>

      <article className="mt-8 flex flex-col gap-4 rounded-2xl bg-night-800/80 p-6 ring-1 ring-white/10">
        <div>
          <p className="text-3xl font-semibold text-radar-400">{formatCurrencyBRL(offer.price)}</p>
          <p className="mt-1 text-sm text-white/50">por pessoa, ida e volta</p>
        </div>

        <dl className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <dt className="text-white/40">Datas</dt>
            <dd className="text-white">{formatDateRange(offer.departureDate, offer.returnDate)}</dd>
          </div>
          <div>
            <dt className="text-white/40">Companhia</dt>
            <dd className="text-white">{offer.airline}</dd>
          </div>
          <div>
            <dt className="text-white/40">Duração</dt>
            <dd className="text-white">{formatDuration(offer.durationMinutes)}</dd>
          </div>
          <div>
            <dt className="text-white/40">Escalas</dt>
            <dd className="text-white">{formatStops(offer.stops)}</dd>
          </div>
        </dl>

        <button
          type="button"
          disabled
          title="Redirecionamento para o fornecedor ainda não implementado nesta versão."
          className="cursor-not-allowed rounded-lg bg-white/10 px-4 py-2.5 text-center text-sm font-medium text-white/50"
        >
          Ir para o fornecedor (em breve)
        </button>
      </article>

      <div className="mt-4">
        <PriceIntelligenceView offerId={offer.id} currentPrice={offer.price} />
      </div>
    </section>
  );
}

function NotFoundOffer({ params }: { params: ExploreParams }) {
  return (
    <section className="mx-auto max-w-md px-4 py-24 text-center sm:px-6">
      <p className="text-5xl">🔍</p>
      <h1 className="mt-4 text-2xl font-semibold text-white">Não encontramos mais essa oferta</h1>
      <p className="mt-2 text-white/60">Ela pode ter saído da faixa da sua busca. Que tal tentar de novo?</p>
      <Link
        to={backToSearchHref(params)}
        className="mt-6 inline-block rounded-lg bg-sky-500 px-4 py-2.5 font-medium text-white transition hover:bg-sky-600"
      >
        Ver resultados
      </Link>
    </section>
  );
}

export function Results() {
  const [searchParams] = useSearchParams();
  const orcamento = searchParams.get("orcamento");
  const destinoId = searchParams.get("destino");
  const ofertaId = searchParams.get("oferta");

  const params: ExploreParams | null = orcamento
    ? {
        budget: Number(orcamento),
        originCity: searchParams.get("origem") ?? "",
        month: searchParams.get("mes") ?? "",
        flexible: searchParams.get("flexivel") !== "false",
        passengers: Number(searchParams.get("passageiros") ?? "1"),
      }
    : null;

  const { status, result, errorMessage } = useExploreSearch(
    params ?? { budget: 0, originCity: "", month: "", flexible: true, passengers: 1 },
  );

  if (!params) {
    return (
      <section className="mx-auto max-w-2xl px-4 py-10 text-center sm:px-6">
        <Link to="/" className="text-sm text-sky-400 hover:underline">
          ← Nova busca
        </Link>
        <p className="mt-8 text-white/60">Nenhuma busca informada.</p>
      </section>
    );
  }

  if (status === "loading") {
    return (
      <section className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
        <LoadingState />
      </section>
    );
  }

  if (status === "error") {
    return (
      <section className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
        <ErrorState message={errorMessage ?? "Algo deu errado."} />
      </section>
    );
  }

  const allDestinations = [...result!.destinations, ...result!.nearBudget];

  if (destinoId && ofertaId) {
    const destination = allDestinations.find((d) => d.id === destinoId);
    const offer = destination?.offers.find((o) => o.id === ofertaId);
    if (!destination || !offer) return <NotFoundOffer params={params} />;
    return <OfferDetail params={params} destination={destination} offer={offer} />;
  }

  return (
    <ExploreResultsView params={params} destinations={result!.destinations} nearBudget={result!.nearBudget} />
  );
}
