// Domínios oficiais verificados (2026-08-17) — nunca uma URL profunda pra
// um voo/preço específico, porque a oferta ainda é mock (CLAUDE.md §10:
// "nunca afirmar que o sistema pesquisa... sem comprovação"). Leva só pro
// site institucional, onde a pessoa pesquisa por conta própria.
const OFFICIAL_WEBSITES: Record<string, string> = {
  gol: "https://www.voegol.com.br",
  azul: "https://www.voeazul.com.br",
  latam: "https://www.latamairlines.com/br/pt",
};

export function resolveAirlineWebsite(airline: string): string | null {
  const key = airline.trim().toLowerCase();
  return OFFICIAL_WEBSITES[key] ?? null;
}
