import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { useAirports } from "../features/radars/useAirports";
import { RadarForm } from "../features/radars/RadarForm";
import * as api from "../services/api";
import type { Radar } from "../types/radar";
import type { RadarInput } from "../services/api";

export function RadarFormPage() {
  const { session } = useAuth();
  const { radarId } = useParams();
  const navigate = useNavigate();
  const { airports, loading: loadingAirports } = useAirports();
  const isEditing = radarId !== undefined;

  const [radar, setRadar] = useState<Radar | null>(null);
  const [loadingRadar, setLoadingRadar] = useState(isEditing);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    if (!isEditing || !radarId) return;
    api
      .listRadars(session!.accessToken)
      .then((radars) => {
        const found = radars.find((r) => r.id === radarId);
        if (!found) {
          setNotFound(true);
          return;
        }
        setRadar(found);
      })
      .finally(() => setLoadingRadar(false));
  }, [isEditing, radarId, session]);

  async function handleSubmit(input: RadarInput) {
    if (isEditing && radarId) {
      await api.updateRadar(session!.accessToken, radarId, input);
    } else {
      await api.createRadar(session!.accessToken, input);
    }
    navigate("/radares");
  }

  if (notFound) {
    return (
      <section className="mx-auto max-w-md px-4 py-24 text-center sm:px-6">
        <p className="text-5xl">🔍</p>
        <h1 className="mt-4 text-2xl font-semibold text-white">Radar não encontrado</h1>
        <Link to="/radares" className="mt-6 inline-block text-sky-400 hover:underline">
          Voltar para Meus Radares
        </Link>
      </section>
    );
  }

  return (
    <section className="mx-auto max-w-xl px-4 py-10 sm:px-6">
      <Link to="/radares" className="text-sm text-sky-400 hover:underline">
        ← Meus Radares
      </Link>
      <h1 className="mt-3 text-2xl font-semibold text-white sm:text-3xl">
        {isEditing ? "Editar Radar" : "Criar Radar"}
      </h1>

      <div className="mt-6">
        {loadingAirports || loadingRadar ? (
          <div className="h-[300px] animate-pulse rounded-2xl bg-night-800/60 ring-1 ring-white/10" />
        ) : (
          <RadarForm
            airports={airports}
            initialRadar={radar ?? undefined}
            onSubmit={handleSubmit}
            submitLabel={isEditing ? "Salvar alterações" : "Ativar Radar"}
          />
        )}
      </div>
    </section>
  );
}
