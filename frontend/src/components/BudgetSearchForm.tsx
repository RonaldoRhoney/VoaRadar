import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";

const MONTHS = [
  "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
];

export function BudgetSearchForm() {
  const navigate = useNavigate();
  const [budget, setBudget] = useState(800);
  const [origin, setOrigin] = useState("");
  const [month, setMonth] = useState("");
  const [flexible, setFlexible] = useState(true);

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const params = new URLSearchParams({
      orcamento: String(budget),
      origem: origin,
      mes: month,
      flexivel: String(flexible),
    });
    navigate(`/resultados?${params.toString()}`);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="mx-auto flex max-w-xl flex-col gap-6 rounded-2xl bg-night-800/80 p-6 shadow-xl ring-1 ring-white/10 sm:p-8"
    >
      <label className="flex flex-col gap-2 text-sm text-white/70">
        Quanto você quer gastar?
        <div className="flex items-center gap-3">
          <input
            type="range"
            min={200}
            max={5000}
            step={50}
            value={budget}
            onChange={(e) => setBudget(Number(e.target.value))}
            className="w-full accent-sky-500"
          />
          <span className="w-24 shrink-0 text-right text-xl font-semibold text-radar-400">
            R$ {budget.toLocaleString("pt-BR")}
          </span>
        </div>
      </label>

      <label className="flex flex-col gap-2 text-sm text-white/70">
        De onde você quer sair?
        <input
          required
          value={origin}
          onChange={(e) => setOrigin(e.target.value)}
          placeholder="Belém"
          className="rounded-lg border border-white/10 bg-night-900 px-3 py-2.5 text-white placeholder-white/30 outline-none focus:border-sky-500"
        />
      </label>

      <label className="flex flex-col gap-2 text-sm text-white/70">
        Quando você quer viajar?
        <select
          required
          value={month}
          onChange={(e) => setMonth(e.target.value)}
          className="rounded-lg border border-white/10 bg-night-900 px-3 py-2.5 text-white outline-none focus:border-sky-500"
        >
          <option value="" disabled>
            Selecione um mês
          </option>
          {MONTHS.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>
      </label>

      <label className="flex items-center gap-2 text-sm text-white/70">
        <input
          type="checkbox"
          checked={flexible}
          onChange={(e) => setFlexible(e.target.checked)}
          className="h-4 w-4 accent-sky-500"
        />
        Não sei para onde ir
      </label>

      <button
        type="submit"
        className="rounded-lg bg-sky-500 px-4 py-3 font-medium text-white transition hover:bg-sky-600"
      >
        Encontrar viagens
      </button>
    </form>
  );
}
