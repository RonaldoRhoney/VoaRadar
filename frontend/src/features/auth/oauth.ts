const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;

/** Redireciona o navegador pro fluxo de OAuth do Supabase — o backend não
 * entra nessa etapa (é um redirect de página inteira, não uma chamada de
 * API), só valida o JWT que o Supabase emite depois, igual já faz pro
 * login por e-mail/senha (app/core/auth.py, provider-agnostic). */
export function redirectToGoogleLogin() {
  if (!SUPABASE_URL) {
    throw new Error("VITE_SUPABASE_URL não configurada.");
  }
  const redirectTo = `${window.location.origin}/auth/callback`;
  const url = `${SUPABASE_URL}/auth/v1/authorize?provider=google&redirect_to=${encodeURIComponent(redirectTo)}`;
  window.location.href = url;
}

/** O Supabase devolve a sessão no fragmento da URL (#access_token=...),
 * nunca na query string — não vai pro histórico do navegador nem pra logs
 * de servidor. */
export function parseOAuthCallback(hash: string): { accessToken: string; refreshToken: string; expiresIn: number } | null {
  const params = new URLSearchParams(hash.replace(/^#/, ""));
  const accessToken = params.get("access_token");
  const refreshToken = params.get("refresh_token");
  const expiresIn = params.get("expires_in");
  if (!accessToken || !refreshToken || !expiresIn) return null;
  return { accessToken, refreshToken, expiresIn: Number(expiresIn) };
}
