import { ExploreSearchForm } from "../features/explore/ExploreSearchForm";

export function Home() {
  return (
    <section className="mx-auto max-w-6xl px-4 py-12 sm:px-6 sm:py-16">
      <div className="text-center">
        <h1 className="text-3xl font-semibold text-white sm:text-5xl">✈️ Voa Radar</h1>
        <p className="mx-auto mt-3 max-w-xl text-white/60">
          Diz pra gente quanto você quer gastar — a gente encontra pra onde dá pra ir.
        </p>
      </div>

      <div className="mt-8">
        <ExploreSearchForm />
      </div>
    </section>
  );
}
