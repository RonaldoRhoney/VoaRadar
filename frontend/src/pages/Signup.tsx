import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { ApiError } from "../services/api";

export function Signup() {
  const { signup } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "error" | "confirmation-required">("idle");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setStatus("loading");
    try {
      const { confirmationRequired } = await signup(email, password);
      if (confirmationRequired) {
        setStatus("confirmation-required");
        return;
      }
      navigate("/radares");
    } catch (error) {
      setStatus("error");
      setErrorMessage(error instanceof ApiError ? error.message : "Algo deu errado. Tente de novo.");
    }
  }

  if (status === "confirmation-required") {
    return (
      <section className="mx-auto max-w-md px-4 py-16 text-center sm:px-6">
        <p className="text-5xl">📬</p>
        <h1 className="mt-4 text-2xl font-semibold text-white">Confirme seu e-mail</h1>
        <p className="mt-2 text-white/60">Enviamos um link de confirmação para {email}. Confirme para poder entrar.</p>
        <Link to="/entrar" className="mt-6 inline-block text-sky-400 hover:underline">
          Ir para o login
        </Link>
      </section>
    );
  }

  return (
    <section className="mx-auto max-w-md px-4 py-16 sm:px-6">
      <h1 className="text-2xl font-semibold text-white">Criar conta</h1>
      <p className="mt-1 text-sm text-white/60">Crie Radares e receba notificações de oportunidade.</p>

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
            minLength={8}
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
          {status === "loading" ? "Criando conta..." : "Criar conta"}
        </button>
      </form>

      <p className="mt-4 text-center text-sm text-white/50">
        Já tem conta?{" "}
        <Link to="/entrar" className="text-sky-400 hover:underline">
          Entrar
        </Link>
      </p>
    </section>
  );
}
