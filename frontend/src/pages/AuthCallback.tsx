import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { parseOAuthCallback } from "../features/auth/oauth";

const FRIENDLY_ERROR = "Não foi possível concluir o login com Google. Tente novamente.";

export function AuthCallback() {
  const { completeOAuthSession } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState(false);

  useEffect(() => {
    const tokens = parseOAuthCallback(window.location.hash);
    if (!tokens) {
      setError(true);
      return;
    }
    completeOAuthSession(tokens);
    // Limpa o fragmento com o token da URL antes de navegar, pra não ficar
    // visível na barra de endereço nem em qualquer histórico.
    window.history.replaceState(null, "", window.location.pathname);
    navigate("/radares", { replace: true });
  }, [completeOAuthSession, navigate]);

  if (error) {
    return (
      <section className="mx-auto max-w-md px-4 py-16 text-center sm:px-6">
        <p className="text-sm text-red-400">{FRIENDLY_ERROR}</p>
        <Link to="/entrar" className="mt-4 inline-block text-sky-400 hover:underline">
          Voltar pro login
        </Link>
      </section>
    );
  }

  return (
    <section className="mx-auto max-w-md px-4 py-16 text-center sm:px-6">
      <p className="text-sm text-white/60">Entrando…</p>
    </section>
  );
}
