import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { ApiError } from "../services/api";

export function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setStatus("loading");
    try {
      await login(email, password);
      navigate("/radares");
    } catch (error) {
      setStatus("error");
      setErrorMessage(error instanceof ApiError ? error.message : "Algo deu errado. Tente de novo.");
    }
  }

  return (
    <section className="mx-auto max-w-md px-4 py-16 sm:px-6">
      <h1 className="text-2xl font-semibold text-white">Entrar</h1>
      <p className="mt-1 text-sm text-white/60">Acesse seus Radares e notificações.</p>

      <form onSubmit={handleSubmit} className="mt-6 flex flex-col gap-4 rounded-2xl bg-night-800/80 p-6 ring-1 ring-white/10">
        <label className="flex flex-col gap-2 text-sm text-white/70">
          E-mail
          <input
            required
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="rounded-lg border border-white/10 bg-night-900 px-3 py-2.5 text-white outline-none focus:border-sky-500"
          />
        </label>

        <label className="flex flex-col gap-2 text-sm text-white/70">
          Senha
          <input
            required
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="rounded-lg border border-white/10 bg-night-900 px-3 py-2.5 text-white outline-none focus:border-sky-500"
          />
        </label>

        {status === "error" && (
          <p role="alert" className="text-sm text-red-400">
            {errorMessage}
          </p>
        )}

        <button
          type="submit"
          disabled={status === "loading"}
          className="rounded-lg bg-sky-500 px-4 py-3 font-medium text-white transition hover:bg-sky-600 disabled:opacity-50"
        >
          {status === "loading" ? "Entrando..." : "Entrar"}
        </button>
      </form>

      <p className="mt-4 text-center text-sm text-white/50">
        Ainda não tem conta?{" "}
        <Link to="/cadastro" className="text-sky-400 hover:underline">
          Cadastre-se
        </Link>
      </p>
    </section>
  );
}
