export interface AppNotification {
  id: string;
  radarId: string;
  type: string;
  title: string;
  message: string;
  readAt: string | null;
  createdAt: string;
}
