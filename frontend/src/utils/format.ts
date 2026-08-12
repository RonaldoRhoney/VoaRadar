export function formatCurrencyBRL(value: number): string {
  return `R$ ${value.toLocaleString("pt-BR")}`;
}
