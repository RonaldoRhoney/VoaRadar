import { useCallback, useEffect, useMemo, useState, type ReactNode } from "react";
import * as api from "../../services/api";
import { ApiError } from "../../services/api";
import { useAuth } from "../auth/useAuth";
import { NotificationsContext, type NotificationsState, type NotificationsStatus } from "./notificationsContext";
import type { AppNotification } from "../../types/notification";

const FALLBACK_ERROR_MESSAGE = "Não conseguimos carregar suas notificações agora. Tente novamente em instantes.";

interface State {
  status: NotificationsStatus;
  notifications: AppNotification[];
  errorMessage: string | null;
}

/** Fonte única de verdade das notificações — sino no Header e a página
 * /notificacoes leem do mesmo estado, então marcar como lida num lugar
 * atualiza o outro na hora, sem precisar de reload da página. */
export function NotificationsProvider({ children }: { children: ReactNode }) {
  const { session } = useAuth();
  const [state, setState] = useState<State>({ status: "loading", notifications: [], errorMessage: null });

  const reload = useCallback(() => {
    if (!session) {
      setState({ status: "idle", notifications: [], errorMessage: null });
      return;
    }
    setState((s) => ({ ...s, status: "loading" }));
    api
      .listNotifications(session.accessToken)
      .then((notifications) => setState({ status: "success", notifications, errorMessage: null }))
      .catch((error: unknown) => {
        const message = error instanceof ApiError ? error.message : FALLBACK_ERROR_MESSAGE;
        setState({ status: "error", notifications: [], errorMessage: message });
      });
  }, [session]);

  useEffect(() => {
    reload();
  }, [reload]);

  const value = useMemo<NotificationsState>(
    () => ({
      ...state,
      unreadCount: state.notifications.filter((n) => n.readAt === null).length,
      reload,
      async markRead(notificationId: string) {
        if (!session) return;
        const updated = await api.markNotificationRead(session.accessToken, notificationId);
        setState((s) => ({
          ...s,
          notifications: s.notifications.map((n) => (n.id === updated.id ? updated : n)),
        }));
      },
    }),
    [state, reload, session],
  );

  return <NotificationsContext.Provider value={value}>{children}</NotificationsContext.Provider>;
}
