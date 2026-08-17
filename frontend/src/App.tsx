import { lazy, Suspense } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { ProtectedRoute } from "./features/auth/ProtectedRoute";
import { useAuth } from "./features/auth/useAuth";
import { Home } from "./pages/Home";
import { Results } from "./pages/Results";

// Carregadas sob demanda — só o Home e o Results (as duas telas de entrada
// do produto) precisam estar no bundle inicial. O resto (auth, radares,
// admin) só é baixado quando a pessoa de fato navega pra lá.
const AdminPanel = lazy(() => import("./pages/AdminPanel").then((m) => ({ default: m.AdminPanel })));
const AuthCallback = lazy(() => import("./pages/AuthCallback").then((m) => ({ default: m.AuthCallback })));
const Login = lazy(() => import("./pages/Login").then((m) => ({ default: m.Login })));
const Notifications = lazy(() => import("./pages/Notifications").then((m) => ({ default: m.Notifications })));
const NotFound = lazy(() => import("./pages/NotFound").then((m) => ({ default: m.NotFound })));
const RadarFormPage = lazy(() => import("./pages/RadarFormPage").then((m) => ({ default: m.RadarFormPage })));
const Radars = lazy(() => import("./pages/Radars").then((m) => ({ default: m.Radars })));
const Signup = lazy(() => import("./pages/Signup").then((m) => ({ default: m.Signup })));

function AdminRoute({ children }: { children: React.ReactNode }) {
  const { session, role, roleLoading } = useAuth();
  if (!session) return <Navigate to="/entrar" replace />;
  if (roleLoading) return null;
  if (role !== "admin") return <Navigate to="/" replace />;
  return <>{children}</>;
}

function App() {
  return (
    <Layout>
      <Suspense fallback={null}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/resultados" element={<Results />} />
          <Route path="/entrar" element={<Login />} />
          <Route path="/cadastro" element={<Signup />} />
          <Route path="/auth/callback" element={<AuthCallback />} />
          <Route
            path="/radares"
            element={
              <ProtectedRoute>
                <Radars />
              </ProtectedRoute>
            }
          />
          <Route
            path="/radares/novo"
            element={
              <ProtectedRoute>
                <RadarFormPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/radares/:radarId/editar"
            element={
              <ProtectedRoute>
                <RadarFormPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/notificacoes"
            element={
              <ProtectedRoute>
                <Notifications />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin"
            element={
              <AdminRoute>
                <AdminPanel />
              </AdminRoute>
            }
          />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Suspense>
    </Layout>
  );
}

export default App;
