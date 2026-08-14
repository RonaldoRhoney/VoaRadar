import { useCallback, useEffect, useState } from "react";
import * as api from "../../services/api";
import { ApiError } from "../../services/api";
import type { AppNotification } from "../../types/notification";

type Status = "loading" | "success" | "error";

interface State {
  status: Status;
  notifications: AppNotification[];
  errorMessage: string | null;
}

const FALLBACK_ERROR_MESSAGE = "Não conseguimos carregar suas notificações agora. Tente novamente em instantes.";

export function useNotifications(accessToken: string) {
  const [state, setState] = useState<State>({ status: "loading", notifications: [], errorMessage: null });

  const reload = useCallback(() => {
    setState((s) => ({ ...s, status: "loading" }));
    api
      .listNotifications(accessToken)
      .then((notifications) => setState({ status: "success", notifications, errorMessage: null }))
      .catch((error: unknown) => {
        const message = error instanceof ApiError ? error.message : FALLBACK_ERROR_MESSAGE;
        setState({ status: "error", notifications: [], errorMessage: message });
      });
  }, [accessToken]);

  useEffect(() => {
    reload();
  }, [reload]);

  async function markRead(notificationId: string) {
    const updated = await api.markNotificationRead(accessToken, notificationId);
    setState((s) => ({ ...s, notifications: s.notifications.map((n) => (n.id === updated.id ? updated : n)) }));
  }

  const unreadCount = state.notifications.filter((n) => n.readAt === null).length;

  return { ...state, reload, markRead, unreadCount };
}
