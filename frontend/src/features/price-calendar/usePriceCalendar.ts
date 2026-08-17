import { useEffect, useState } from "react";
import { ApiError, fetchPriceCalendar } from "../../services/api";
import type { PriceCalendar } from "../../types/flight";

type Status = "loading" | "success" | "error";

interface State {
  status: Status;
  data: PriceCalendar | null;
  errorMessage: string | null;
}

const FALLBACK_ERROR_MESSAGE = "Não conseguimos carregar o calendário de preços agora. Tente novamente em instantes.";

export function usePriceCalendar(destinationId: string, month: string) {
  const [state, setState] = useState<State>({ status: "loading", data: null, errorMessage: null });

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading", data: null, errorMessage: null });

    fetchPriceCalendar(destinationId, month)
      .then((data) => {
        if (cancelled) return;
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
  }, [destinationId, month]);

  return state;
}
