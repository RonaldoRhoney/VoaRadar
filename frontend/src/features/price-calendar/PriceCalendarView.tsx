import { usePriceCalendar } from "./usePriceCalendar";
import { formatCurrencyBRL } from "../../utils/format";

const WEEKDAY_LABELS = ["D", "S", "T", "Q", "Q", "S", "S"];

function Loading() {
  return (
    <div role="status" aria-live="polite" className="h-[220px] animate-pulse rounded-2xl bg-night-800/60 ring-1 ring-white/10" />
  );
}

function ErrorState({ message }: { message: string }) {
  return (
    <p role="alert" className="rounded-2xl bg-night-800/80 p-5 text-sm text-white/60 ring-1 ring-white/10">
      {message}
    </p>
  );
}

/** Verde = mais barato do mês, vermelho = mais caro — intensidade relativa
 * ao próprio mês exibido, não a um valor absoluto (DEC-008: "o Voa Radar
 * encontrando os melhores dias" dentro do período escolhido). */
function priceColor(price: number, min: number, max: number): string {
  if (max === min) return "bg-night-700";
  const ratio = (price - min) / (max - min);
  if (ratio <= 0.2) return "bg-radar-500/70 text-night-900";
  if (ratio <= 0.5) return "bg-radar-500/25";
  if (ratio <= 0.8) return "bg-amber-500/20";
  return "bg-red-500/20";
}

export function PriceCalendarView({ destinationId, month }: { destinationId: string; month: string }) {
  const { status, data, errorMessage } = usePriceCalendar(destinationId, month);

  if (status === "loading") return <Loading />;
  if (status === "error") return <ErrorState message={errorMessage ?? ""} />;
  if (!data || data.days.length === 0) return null;

  const prices = data.days.map((d) => d.price);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const firstWeekday = new Date(`${data.days[0].date}T00:00:00`).getDay();
  const leadingBlanks = Array.from({ length: firstWeekday }, (_, i) => `blank-${i}`);

  return (
    <div className="rounded-2xl bg-night-800/80 p-5 ring-1 ring-white/10">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-medium text-white/70">📅 Melhores dias pra viajar</h2>
        <span className="text-xs text-white/40">dados de exemplo (mock)</span>
      </div>

      <div className="mt-4 grid grid-cols-7 gap-1 text-center text-[11px] text-white/40">
        {WEEKDAY_LABELS.map((label, i) => (
          <span key={i}>{label}</span>
        ))}
      </div>

      <div className="mt-1 grid grid-cols-7 gap-1">
        {leadingBlanks.map((key) => (
          <span key={key} />
        ))}
        {data.days.map((day) => {
          const isCheapest = day.date === data.cheapestDate;
          const dayNumber = day.date.slice(-2);
          return (
            <div
              key={day.date}
              title={`${formatCurrencyBRL(day.price)} em ${dayNumber}`}
              className={`flex flex-col items-center justify-center rounded-lg px-1 py-1.5 text-[11px] ${priceColor(day.price, min, max)} ${
                isCheapest ? "ring-2 ring-radar-400" : ""
              }`}
            >
              <span className="font-medium">{Number(dayNumber)}</span>
              <span className="text-[10px] opacity-80">{Math.round(day.price)}</span>
            </div>
          );
        })}
      </div>

      {data.cheapestDate && (
        <p className="mt-3 text-xs text-white/50">
          Dia mais barato do mês: <span className="text-radar-400">{data.cheapestDate.split("-").reverse().join("/")}</span>
        </p>
      )}
    </div>
  );
}
