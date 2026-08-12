import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";

export function SearchForm() {
  const navigate = useNavigate();
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [departureDate, setDepartureDate] = useState("");
  const [returnDate, setReturnDate] = useState("");
  const [passengers, setPassengers] = useState(1);

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const params = new URLSearchParams({
      origem: origin,
      destino: destination,
      ida: departureDate,
      passageiros: String(passengers),
    });
    if (returnDate) params.set("volta", returnDate);
    navigate(`/resultados?${params.toString()}`);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="grid grid-cols-1 gap-4 rounded-2xl bg-night-800/80 p-5 shadow-xl ring-1 ring-white/10 sm:grid-cols-2 sm:p-6 lg:grid-cols-6"
    >
      <label className="flex flex-col gap-1.5 text-sm text-white/70 lg:col-span-1">
        Origem
        <input
          required
          value={origin}
          onChange={(e) => setOrigin(e.target.value.toUpperCase())}
          placeholder="GRU"
          maxLength={3}
          className="rounded-lg border border-white/10 bg-night-900 px-3 py-2.5 uppercase text-white placeholder-white/30 outline-none focus:border-sky-500"
        />
      </label>

      <label className="flex flex-col gap-1.5 text-sm text-white/70 lg:col-span-1">
        Destino
        <input
          required
          value={destination}
          onChange={(e) => setDestination(e.target.value.toUpperCase())}
          placeholder="LIS"
          maxLength={3}
          className="rounded-lg border border-white/10 bg-night-900 px-3 py-2.5 uppercase text-white placeholder-white/30 outline-none focus:border-sky-500"
        />
      </label>

      <label className="flex flex-col gap-1.5 text-sm text-white/70 lg:col-span-1">
        Ida
        <input
          required
          type="date"
          value={departureDate}
          onChange={(e) => setDepartureDate(e.target.value)}
          className="rounded-lg border border-white/10 bg-night-900 px-3 py-2.5 text-white outline-none focus:border-sky-500"
        />
      </label>

      <label className="flex flex-col gap-1.5 text-sm text-white/70 lg:col-span-1">
        Volta <span className="text-white/40">(opcional)</span>
        <input
          type="date"
          value={returnDate}
          onChange={(e) => setReturnDate(e.target.value)}
          className="rounded-lg border border-white/10 bg-night-900 px-3 py-2.5 text-white outline-none focus:border-sky-500"
        />
      </label>

      <label className="flex flex-col gap-1.5 text-sm text-white/70 lg:col-span-1">
        Passageiros
        <input
          required
          type="number"
          min={1}
          max={9}
          value={passengers}
          onChange={(e) => setPassengers(Number(e.target.value))}
          className="rounded-lg border border-white/10 bg-night-900 px-3 py-2.5 text-white outline-none focus:border-sky-500"
        />
      </label>

      <button
        type="submit"
        className="self-end rounded-lg bg-sky-500 px-4 py-2.5 font-medium text-white transition hover:bg-sky-600 lg:col-span-1"
      >
        Buscar voos
      </button>
    </form>
  );
}
