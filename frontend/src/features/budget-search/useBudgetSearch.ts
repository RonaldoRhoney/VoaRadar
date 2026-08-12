import { useEffect, useState } from "react";
import { ApiError, searchBudgetDestinations } from "../../services/api";
import type { BudgetDestination, BudgetSearchParams } from "../../types/flight";

type Status = "loading" | "success" | "error";

interface State {
  status: Status;
  destinations: BudgetDestination[];
  errorMessage: string | null;
}

const FALLBACK_ERROR_MESSAGE =
  "Não conseguimos encontrar destinos neste momento. Tente novamente em instantes.";

export function useBudgetSearch(params: BudgetSearchParams) {
  const [state, setState] = useState<State>({
    status: "loading",
    destinations: [],
    errorMessage: null,
  });

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading", destinations: [], errorMessage: null });

    searchBudgetDestinations(params)
      .then((destinations) => {
        if (cancelled) return;
        setState({ status: "success", destinations, errorMessage: null });
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        const message = error instanceof ApiError ? error.message : FALLBACK_ERROR_MESSAGE;
        setState({ status: "error", destinations: [], errorMessage: message });
      });

    return () => {
      cancelled = true;
    };
  }, [params.budget, params.originCity, params.month, params.flexible]);

  return state;
}
