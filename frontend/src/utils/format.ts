export function formatCurrencyBRL(value: number): string {
  return `R$ ${value.toLocaleString("pt-BR")}`;
}

export function formatDuration(minutes: number): string {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return `${h}h${m ? `${m}min` : ""}`;
}

function formatDay(iso: string): string {
  const [, month, day] = iso.split("-");
  return `${Number(day)}/${Number(month)}`;
}

export function formatDateRange(departureDate: string, returnDate: string | null): string {
  if (!returnDate) return formatDay(departureDate);
  return `${formatDay(departureDate)}–${formatDay(returnDate)}`;
}

export function formatStops(stops: number): string {
  if (stops === 0) return "voo direto";
  if (stops === 1) return "1 escala";
  return `${stops} escalas`;
}

export function formatObservedDate(isoDateTime: string): string {
  return new Date(isoDateTime).toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" });
}

export function formatPercentage(value: number): string {
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toLocaleString("pt-BR", { maximumFractionDigits: 1 })}%`;
}
