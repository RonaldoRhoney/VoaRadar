import { Link } from "react-router-dom";

export function Header() {
  return (
    <header className="sticky top-0 z-10 border-b border-white/10 bg-night-900/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
        <Link to="/" className="flex items-center gap-2 text-lg font-semibold text-white">
          <span className="text-radar-400">📡</span>
          Voa Radar
        </Link>
        <nav className="hidden items-center gap-6 text-sm text-white/70 sm:flex">
          <Link to="/" className="hover:text-white">
            Buscar viagens
          </Link>
        </nav>
      </div>
    </header>
  );
}
