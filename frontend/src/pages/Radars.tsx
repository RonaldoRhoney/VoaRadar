import { Link } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { useAirports } from "../features/radars/useAirports";
import { RadarCard } from "../features/radars/RadarCard";
import { useRadars } from "../features/radars/useRadars";

function LoadingState() {
  return (
    <div className="flex flex-col gap-3" role="status" aria-live="polite">
      {[0, 1].map((i) => (
        <div key={i} className="h-[120px] animate-pulse rounded-2xl bg-night-800/60 ring-1 ring-white/10" />
      ))}
    </div>
  );
}

export function Radars() {
  const { session } = useAuth();
  const { airports } = useAirports();
  const { status, radars, errorMessage, toggleStatus, remove } = useRadars(session!.accessToken);

  return (
    <section className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-white sm:text-3xl">📡 Meus Radares</h1>
        <Link to="/radares/novo" className="rounded-lg bg-sky-500 px-4 py-2 text-sm font-medium text-white hover:bg-sky-600">
          + Criar Radar
        </Link>
      </div>

      {status === "loading" && (
        <div className="mt-6">
          <LoadingState />
        </div>
      )}

      {status === "error" && (
        <p role="alert" className="mt-6 rounded-2xl bg-night-800/80 p-6 text-center text-white/70 ring-1 ring-white/10">
          {errorMessage}
        </p>
      )}

      {status === "success" && radars.length === 0 && (
        <div className="mt-6 rounded-2xl bg-night-800/80 p-8 text-center ring-1 ring-white/10">
          <p className="text-4xl">📡</p>
          <p className="mt-3 text-white/70">Você ainda não tem Radares ativos.</p>
          <p className="mt-1 text-sm text-white/40">Crie um Radar e a gente avisa quando aparecer uma oportunidade.</p>
          <Link
            to="/radares/novo"
            className="mt-4 inline-block rounded-lg bg-sky-500 px-4 py-2.5 text-sm font-medium text-white hover:bg-sky-600"
          >
            Criar meu primeiro Radar
          </Link>
        </div>
      )}

      {status === "success" && radars.length > 0 && (
        <div className="mt-6 flex flex-col gap-3">
          {radars.map((radar) => (
            <RadarCard key={radar.id} radar={radar} airports={airports} onToggleStatus={toggleStatus} onDelete={remove} />
          ))}
        </div>
      )}
    </section>
  );
}
