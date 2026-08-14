import { createContext } from "react";
import type { AppNotification } from "../../types/notification";

export type NotificationsStatus = "idle" | "loading" | "success" | "error";

export interface NotificationsState {
  status: NotificationsStatus;
  notifications: AppNotification[];
  errorMessage: string | null;
  unreadCount: number;
  reload: () => void;
  markRead: (notificationId: string) => Promise<void>;
}

export const NotificationsContext = createContext<NotificationsState | null>(null);
