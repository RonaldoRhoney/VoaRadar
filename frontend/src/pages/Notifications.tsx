import { Link } from "react-router-dom";
import { useNotifications } from "../features/notifications/useNotifications";
import { formatObservedDate } from "../utils/format";

export function Notifications() {
  const { status, notifications, errorMessage, markRead } = useNotifications();

  return (
    <section className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <h1 className="text-2xl font-semibold text-white sm:text-3xl">🔔 Notificações</h1>

      {status === "loading" && (
        <div className="mt-6 flex flex-col gap-3" role="status" aria-live="polite">
          {[0, 1].map((i) => (
            <div key={i} className="h-[96px] animate-pulse rounded-2xl bg-night-800/60 ring-1 ring-white/10" />
          ))}
        </div>
      )}

      {status === "error" && (
        <p role="alert" className="mt-6 rounded-2xl bg-night-800/80 p-6 text-center text-white/70 ring-1 ring-white/10">
          {errorMessage}
        </p>
      )}

      {status === "success" && notifications.length === 0 && (
        <div className="mt-6 rounded-2xl bg-night-800/80 p-8 text-center ring-1 ring-white/10">
          <p className="text-4xl">🔔</p>
          <p className="mt-3 text-white/70">Nenhuma notificação ainda.</p>
          <p className="mt-1 text-sm text-white/40">Quando um Radar encontrar uma oportunidade, ela aparece aqui.</p>
        </div>
      )}

      {status === "success" && notifications.length > 0 && (
        <div className="mt-6 flex flex-col gap-3">
          {notifications.map((n) => {
            const isUnread = n.readAt === null;
            return (
              <button
                key={n.id}
                onClick={() => isUnread && markRead(n.id)}
                className={`flex flex-col gap-1 rounded-2xl p-5 text-left ring-1 transition ${
                  isUnread ? "bg-night-800/80 ring-radar-400/40" : "bg-night-800/40 ring-white/10"
                }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <p className="font-medium text-white">
                    {isUnread && <span className="mr-1 text-radar-400">●</span>}
                    🔥 {n.title}
                  </p>
                  <span className="shrink-0 text-xs text-white/40">{formatObservedDate(n.createdAt)}</span>
                </div>
                <p className="text-sm text-white/60">{n.message}</p>
              </button>
            );
          })}
        </div>
      )}

      <Link to="/radares" className="mt-6 inline-block text-sm text-sky-400 hover:underline">
        ← Meus Radares
      </Link>
    </section>
  );
}
