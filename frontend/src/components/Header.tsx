import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { useNotifications } from "../features/notifications/useNotifications";

function NotificationBell() {
  const { unreadCount } = useNotifications();

  return (
    <Link to="/notificacoes" className="relative text-white/70 hover:text-white" aria-label="Notificações">
      🔔
      {unreadCount > 0 && (
        <span className="absolute -right-1.5 -top-1.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-radar-500 px-1 text-[10px] font-semibold text-night-900">
          {unreadCount}
        </span>
      )}
    </Link>
  );
}

export function Header() {
  const { session, logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate("/");
  }

  return (
    <header className="sticky top-0 z-10 border-b border-white/10 bg-night-900/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
        <Link to="/" className="flex items-center gap-2 text-lg font-semibold text-white">
          <span className="text-radar-400">📡</span>
          Voa Radar
        </Link>
        <nav className="flex items-center gap-4 text-sm text-white/70 sm:gap-6">
          <Link to="/" className="hidden hover:text-white sm:inline">
            Buscar viagens
          </Link>

          {session ? (
            <>
              <Link to="/radares" className="hidden hover:text-white sm:inline">
                Meus Radares
              </Link>
              <NotificationBell />
              <button onClick={handleLogout} className="hover:text-white">
                Sair
              </button>
            </>
          ) : (
            <Link to="/entrar" className="rounded-lg bg-sky-500 px-3 py-1.5 font-medium text-white hover:bg-sky-600">
              Entrar
            </Link>
          )}
        </nav>
      </div>
    </header>
  );
}
