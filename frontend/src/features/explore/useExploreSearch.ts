import { useEffect, useState } from "react";
import { ApiError, exploreDestinations } from "../../services/api";
import type { ExploreParams, ExploreResult } from "../../types/flight";

type Status = "loading" | "success" | "error";

interface State {
  status: Status;
  result: ExploreResult | null;
  errorMessage: string | null;
}

const FALLBACK_ERROR_MESSAGE =
  "Não conseguimos encontrar destinos neste momento. Tente novamente em instantes.";

export function useExploreSearch(params: ExploreParams) {
  const [state, setState] = useState<State>({ status: "loading", result: null, errorMessage: null });

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading", result: null, errorMessage: null });

    exploreDestinations(params)
      .then((result) => {
        if (cancelled) return;
        setState({ status: "success", result, errorMessage: null });
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        const message = error instanceof ApiError ? error.message : FALLBACK_ERROR_MESSAGE;
        setState({ status: "error", result: null, errorMessage: message });
      });

    return () => {
      cancelled = true;
    };
    // Depende dos campos primitivos de `params`, não do objeto — `params` é
    // recriado a cada render de quem chama o hook, o que causaria um loop
    // infinito se fosse usado diretamente como dependência.
    // oxlint-disable-next-line react-hooks/exhaustive-deps
  }, [params.budget, params.originCity, params.month, params.flexible, params.passengers]);

  return state;
}
