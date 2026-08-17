import { createContext } from "react";
import type { Session } from "../../types/auth";

export interface AuthState {
  session: Session | null;
  signup: (email: string, password: string) => Promise<{ confirmationRequired: boolean }>;
  login: (email: string, password: string) => Promise<void>;
  loginWithGoogle: () => void;
  completeOAuthSession: (tokens: { accessToken: string; refreshToken: string; expiresIn: number }) => void;
  logout: () => Promise<void>;
}

export const AuthContext = createContext<AuthState | null>(null);
