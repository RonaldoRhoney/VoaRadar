import type { BudgetDestination, BudgetSearchParams } from "../types/flight";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {}

export async function searchBudgetDestinations(
  params: BudgetSearchParams,
): Promise<BudgetDestination[]> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/flights/budget-search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        budget: params.budget,
        origin_city: params.originCity,
        month: params.month,
        flexible: params.flexible,
      }),
    });
  } catch {
    throw new ApiError("Não conseguimos falar com o servidor agora. Verifique sua conexão e tente novamente.");
  }

  if (!response.ok) {
    throw new ApiError("Não conseguimos encontrar destinos neste momento. Tente novamente em instantes.");
  }

  return response.json();
}
