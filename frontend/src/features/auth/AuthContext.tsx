import { useEffect, useMemo, useState, type ReactNode } from "react";
import * as api from "../../services/api";
import { AuthContext } from "./authContext";
import { redirectToGoogleLogin } from "./oauth";
import { clearSession, isExpired, loadSession, saveSession } from "./session";
import type { Session } from "../../types/auth";
import type { AuthState } from "./authContext";

function initialSession(): Session | null {
  const session = loadSession();
  if (session && isExpired(session)) {
    clearSession();
    return null;
  }
  return session;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<Session | null>(initialSession);
  const [role, setRole] = useState<string | null>(null);
  // Começa "true" quando já existe sessão salva (ex: navegar direto pra
  // /admin depois de já ter feito login antes) — sem isso, o primeiro
  // render do AdminRoute via role=null/roleLoading=false como "confirmado
  // não-admin" e redireciona antes do useEffect abaixo sequer rodar.
  const [roleLoading, setRoleLoading] = useState(() => initialSession() !== null);

  useEffect(() => {
    if (!session) {
      setRole(null);
      setRoleLoading(false);
      return;
    }
    let cancelled = false;
    setRoleLoading(true);
    api
      .getMe(session.accessToken)
      .then((me) => {
        if (!cancelled) setRole(me.role);
      })
      .catch(() => {
        if (!cancelled) setRole(null);
      })
      .finally(() => {
        if (!cancelled) setRoleLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [session]);

  const value = useMemo<AuthState>(
    () => ({
      session,
      role,
      roleLoading,
      async signup(email, password) {
        const newSession = await api.signup(email, password);
        if (newSession === null) return { confirmationRequired: true };
        saveSession(newSession);
        setSession(newSession);
        return { confirmationRequired: false };
      },
      async login(email, password) {
        const newSession = await api.login(email, password);
        saveSession(newSession);
        setSession(newSession);
      },
      loginWithGoogle() {
        redirectToGoogleLogin();
      },
      completeOAuthSession(tokens) {
        const newSession: Session = {
          accessToken: tokens.accessToken,
          refreshToken: tokens.refreshToken,
          expiresAt: Date.now() + tokens.expiresIn * 1000,
        };
        saveSession(newSession);
        setSession(newSession);
      },
      async logout() {
        if (session) {
          await api.logout(session.accessToken).catch(() => undefined);
        }
        clearSession();
        setSession(null);
      },
    }),
    [session, role, roleLoading],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
