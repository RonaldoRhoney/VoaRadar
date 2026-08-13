import { useEffect, useState } from "react";
import { ApiError, fetchPriceIntelligence } from "../../services/api";
import type { PriceIntelligence } from "../../types/priceIntelligence";

type Status = "loading" | "success" | "not-found" | "error";

interface State {
  status: Status;
  data: PriceIntelligence | null;
  errorMessage: string | null;
}

const FALLBACK_ERROR_MESSAGE = "Não conseguimos analisar esse preço agora. Tente novamente em instantes.";

export function usePriceIntelligence(offerId: string, currentPrice: number) {
  const [state, setState] = useState<State>({ status: "loading", data: null, errorMessage: null });

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading", data: null, errorMessage: null });

    fetchPriceIntelligence(offerId, currentPrice)
      .then((data) => {
        if (cancelled) return;
        if (data === null) {
          setState({ status: "not-found", data: null, errorMessage: null });
          return;
        }
        setState({ status: "success", data, errorMessage: null });
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        const message = error instanceof ApiError ? error.message : FALLBACK_ERROR_MESSAGE;
        setState({ status: "error", data: null, errorMessage: message });
      });

    return () => {
      cancelled = true;
    };
  }, [offerId, currentPrice]);

  return state;
}
