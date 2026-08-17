import { Navigate, Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { ProtectedRoute } from "./features/auth/ProtectedRoute";
import { useAuth } from "./features/auth/useAuth";
import { AdminPanel } from "./pages/AdminPanel";
import { AuthCallback } from "./pages/AuthCallback";
import { Home } from "./pages/Home";
import { Login } from "./pages/Login";
import { Notifications } from "./pages/Notifications";
import { NotFound } from "./pages/NotFound";
import { RadarFormPage } from "./pages/RadarFormPage";
import { Radars } from "./pages/Radars";
import { Results } from "./pages/Results";
import { Signup } from "./pages/Signup";

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
    </Layout>
  );
}

export default App;
