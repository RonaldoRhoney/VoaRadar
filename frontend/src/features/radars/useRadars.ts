import { useCallback, useEffect, useState } from "react";
import * as api from "../../services/api";
import { ApiError } from "../../services/api";
import type { Radar, RadarStatus } from "../../types/radar";

type Status = "loading" | "success" | "error";

interface State {
  status: Status;
  radars: Radar[];
  errorMessage: string | null;
}

const FALLBACK_ERROR_MESSAGE = "Não conseguimos carregar seus Radares agora. Tente novamente em instantes.";

export function useRadars(accessToken: string) {
  const [state, setState] = useState<State>({ status: "loading", radars: [], errorMessage: null });

  const reload = useCallback(() => {
    setState((s) => ({ ...s, status: "loading" }));
    api
      .listRadars(accessToken)
      .then((radars) => setState({ status: "success", radars, errorMessage: null }))
      .catch((error: unknown) => {
        const message = error instanceof ApiError ? error.message : FALLBACK_ERROR_MESSAGE;
        setState({ status: "error", radars: [], errorMessage: message });
      });
  }, [accessToken]);

  useEffect(() => {
    reload();
  }, [reload]);

  async function toggleStatus(radar: Radar) {
    const nextStatus: RadarStatus = radar.status === "ACTIVE" ? "PAUSED" : "ACTIVE";
    const updated = await api.updateRadar(accessToken, radar.id, { status: nextStatus });
    setState((s) => ({ ...s, radars: s.radars.map((r) => (r.id === updated.id ? updated : r)) }));
  }

  async function remove(radarId: string) {
    await api.deleteRadar(accessToken, radarId);
    setState((s) => ({ ...s, radars: s.radars.filter((r) => r.id !== radarId) }));
  }

  return { ...state, reload, toggleStatus, remove };
}
