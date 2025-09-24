import React, { createContext, useContext, useState } from "react";
import { useNavigate } from "@tanstack/react-router";

interface AuthContextType {
  accessToken: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const navigate = useNavigate();

  const login = async (username: string, password: string) => {
    const form = new FormData();
    form.append("username", username);
    form.append("password", password);

    const res = await fetch("http://localhost:8000/api/v1/auth/token", {
      method: "POST",
      body: form,
      credentials: "include",
    });

    if (!res.ok) throw new Error("Login failed");
    const data = await res.json() as { access_token: string, token_type: string };
    setAccessToken(data.access_token);
    console.log(data)
    navigate({ to: "/dashboard" });
  };

  const logout = async () => {
    const res = await fetch("http://localhost:8000/api/v1/auth/logout", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
      credentials: "include",
    });

    if (!res.ok) throw new Error("Logout failed");
  
    setAccessToken(null);

    navigate({ to: "/login" });
  };

  return (
    <AuthContext.Provider value={{ accessToken, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};