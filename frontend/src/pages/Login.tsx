import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { ApiError } from "../services/api";

export function Login() {
  const { login, loginWithGoogle } = useAuth();
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

      <div className="mt-6 flex flex-col gap-4 rounded-2xl bg-night-800/80 p-6 ring-1 ring-white/10">
        <button
          type="button"
          onClick={loginWithGoogle}
          className="flex items-center justify-center gap-2 rounded-lg border border-white/10 bg-night-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-white/5"
        >
          <GoogleIcon />
          Continuar com Google
        </button>

        <div className="flex items-center gap-3 text-xs text-white/40">
          <span className="h-px flex-1 bg-white/10" />
          ou
          <span className="h-px flex-1 bg-white/10" />
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
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
      </div>

      <p className="mt-4 text-center text-sm text-white/50">
        Ainda não tem conta?{" "}
        <Link to="/cadastro" className="text-sky-400 hover:underline">
          Cadastre-se
        </Link>
      </p>
    </section>
  );
}

export function GoogleIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 48 48" aria-hidden="true">
      <path
        fill="#FFC107"
        d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.3 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.1 8 3l5.7-5.7C34.6 6.1 29.6 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.7-.4-3.5z"
      />
      <path
        fill="#FF3D00"
        d="m6.3 14.7 6.6 4.8C14.6 15.9 18.9 13 24 13c3.1 0 5.8 1.1 8 3l5.7-5.7C34.6 6.1 29.6 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"
      />
      <path
        fill="#4CAF50"
        d="M24 44c5.5 0 10.4-1.9 14.2-5.1l-6.5-5.5c-2 1.5-4.7 2.6-7.7 2.6-5.3 0-9.7-3.3-11.3-8l-6.6 5.1C9.6 39.6 16.2 44 24 44z"
      />
      <path
        fill="#1976D2"
        d="M43.6 20.5H42V20H24v8h11.3c-.8 2.3-2.3 4.2-4.2 5.4l6.5 5.5C40.5 36.5 44 30.9 44 24c0-1.3-.1-2.7-.4-3.5z"
      />
    </svg>
  );
}
