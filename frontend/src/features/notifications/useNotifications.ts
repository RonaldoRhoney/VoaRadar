import { useContext } from "react";
import { NotificationsContext } from "./notificationsContext";

export function useNotifications() {
  const context = useContext(NotificationsContext);
  if (context === null) throw new Error("useNotifications deve ser usado dentro de <NotificationsProvider>");
  return context;
}
