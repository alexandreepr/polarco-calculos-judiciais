import { useAuth } from "./AuthProvider";
import { Navigate } from "@tanstack/react-router";

export function RequireAuth({ children }: { children: React.ReactNode }) {
  const { accessToken } = useAuth();

  if (!accessToken) {
    return <Navigate to="/login" />;
  }

  return <>{children}</>;
}