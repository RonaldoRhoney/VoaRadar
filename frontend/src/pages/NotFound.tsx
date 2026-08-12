import { Link } from "react-router-dom";

export function NotFound() {
  return (
    <section className="mx-auto max-w-md px-4 py-24 text-center sm:px-6">
      <p className="text-5xl">🧭</p>
      <h1 className="mt-4 text-2xl font-semibold text-white">Página não encontrada</h1>
      <p className="mt-2 text-white/60">
        Esse caminho não existe no Voa Radar. Que tal começar uma nova busca?
      </p>
      <Link
        to="/"
        className="mt-6 inline-block rounded-lg bg-sky-500 px-4 py-2.5 font-medium text-white transition hover:bg-sky-600"
      >
        Voltar para a Home
      </Link>
    </section>
  );
}
