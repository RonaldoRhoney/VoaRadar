import { useState, type FormEvent } from "react";
import type { Airport, ConditionType, Radar } from "../../types/radar";
import type { RadarInput } from "../../services/api";

export function RadarForm({
  airports,
  initialRadar,
  onSubmit,
  submitLabel,
}: {
  airports: Airport[];
  initialRadar?: Radar;
  onSubmit: (input: RadarInput) => Promise<void>;
  submitLabel: string;
}) {
  const [name, setName] = useState(initialRadar?.name ?? "");
  const [originAirportId, setOriginAirportId] = useState(initialRadar?.originAirportId ?? "");
  const [destinationAirportId, setDestinationAirportId] = useState(initialRadar?.destinationAirportId ?? "");
  const [conditionType, setConditionType] = useState<ConditionType>(initialRadar?.conditionType ?? "PRICE_BELOW");
  const [conditionPrice, setConditionPrice] = useState(initialRadar?.conditionPrice ?? 500);
  const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setStatus("loading");
    try {
      await onSubmit({
        name,
        originAirportId,
        destinationAirportId,
        conditionType,
        conditionPrice: conditionType === "PRICE_BELOW" ? conditionPrice : null,
        conditionClassification: conditionType === "OPPORTUNITY_CLASSIFICATION" ? "EXCELLENT" : null,
      });
    } catch (error) {
      setStatus("error");
      setErrorMessage(error instanceof Error ? error.message : "Algo deu errado. Tente de novo.");
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 rounded-2xl bg-night-800/80 p-6 ring-1 ring-white/10">
      <label className="flex flex-col gap-2 text-sm text-white/70">
        Nome do Radar
        <input
          required
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Meu Radar Recife"
          className="rounded-lg border border-white/10 bg-night-900 px-3 py-2.5 text-white placeholder-white/30 outline-none focus:border-sky-500"
        />
      </label>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <label className="flex flex-col gap-2 text-sm text-white/70">
          Origem
          <select
            required
            value={originAirportId}
            onChange={(e) => setOriginAirportId(e.target.value)}
            className="rounded-lg border border-white/10 bg-night-900 px-3 py-2.5 text-white outline-none focus:border-sky-500"
          >
            <option value="" disabled>
              Selecione
            </option>
            {airports.map((a) => (
              <option key={a.id} value={a.id}>
                {a.city} ({a.code})
              </option>
            ))}
          </select>
        </label>

        <label className="flex flex-col gap-2 text-sm text-white/70">
          Destino
          <select
            required
            value={destinationAirportId}
            onChange={(e) => setDestinationAirportId(e.target.value)}
            className="rounded-lg border border-white/10 bg-night-900 px-3 py-2.5 text-white outline-none focus:border-sky-500"
          >
            <option value="" disabled>
              Selecione
            </option>
            {airports.map((a) => (
              <option key={a.id} value={a.id}>
                {a.city} ({a.code})
              </option>
            ))}
          </select>
        </label>
      </div>

      <label className="flex flex-col gap-2 text-sm text-white/70">
        Avisar quando
        <select
          value={conditionType}
          onChange={(e) => setConditionType(e.target.value as ConditionType)}
          className="rounded-lg border border-white/10 bg-night-900 px-3 py-2.5 text-white outline-none focus:border-sky-500"
        >
          <option value="PRICE_BELOW">O preço ficar abaixo de um valor</option>
          <option value="OPPORTUNITY_CLASSIFICATION">For classificado como Excelente oportunidade</option>
        </select>
      </label>

      {conditionType === "PRICE_BELOW" && (
        <label className="flex flex-col gap-2 text-sm text-white/70">
          Valor
          <input
            required
            type="number"
            min={1}
            value={conditionPrice}
            onChange={(e) => setConditionPrice(Number(e.target.value))}
            className="rounded-lg border border-white/10 bg-night-900 px-3 py-2.5 text-white outline-none focus:border-sky-500"
          />
        </label>
      )}

      {status === "error" && (
        <p role="alert" className="text-sm text-red-400">
          {errorMessage}
        </p>
      )}

      <button
        type="submit"
        disabled={status === "loading"}
        className="rounded-lg bg-sky-500 px-4 py-3 font-medium text-white transition hover:bg-sky-600 disabled:opacity-50"
      >
        {status === "loading" ? "Salvando..." : submitLabel}
      </button>
    </form>
  );
}
