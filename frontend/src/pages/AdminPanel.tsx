import { useEffect, useState } from "react";
import { useAuth } from "../features/auth/useAuth";
import { getPlatformMetrics, type PlatformMetrics } from "../services/api";

const FRIENDLY_ERROR = "Não conseguimos carregar as métricas agora. Tente novamente em instantes.";

export function AdminPanel() {
  const { session } = useAuth();
  const [metrics, setMetrics] = useState<PlatformMetrics | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!session) return;
    getPlatformMetrics(session.accessToken)
      .then(setMetrics)
      .catch(() => setError(FRIENDLY_ERROR));
  }, [session]);

  return (
    <section className="mx-auto max-w-5xl px-4 py-16 sm:px-6">
      <h1 className="text-2xl font-semibold text-white">Painel Admin</h1>
      <p className="mt-1 text-sm text-white/60">Métricas gerais da plataforma Voa Radar.</p>

      {error && <p className="mt-6 text-sm text-red-400">{error}</p>}

      {metrics && (
        <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <MetricCard label="Usuários totais" value={metrics.totalUsers} />
          <MetricCard label="Radares criados" value={metrics.totalRadars} />
          <MetricCard label="Radares ativos" value={metrics.activeRadars} />
          <MetricCard label="Oportunidades detectadas" value={metrics.totalRadarEvents} />
          <MetricCard label="Notificações enviadas" value={metrics.totalNotifications} />
          <MetricCard label="Novos usuários (7 dias)" value={metrics.newUsers7d} />
          <MetricCard label="Novos radares (7 dias)" value={metrics.newRadars7d} />
        </div>
      )}
    </section>
  );
}

function MetricCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-2xl bg-night-800/80 p-5 ring-1 ring-white/10">
      <p className="text-xs text-white/50">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-white">{value}</p>
    </div>
  );
}
