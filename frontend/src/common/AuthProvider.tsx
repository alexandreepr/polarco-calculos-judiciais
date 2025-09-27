import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import { AuthContext } from "@/contexts/AuthContext";


export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [accessToken, setAccessToken] = useState<string | null>(null);
   const [currentUser, setCurrentUser] = useState<User | null>(null);
  const navigate = useNavigate();

  const fetchCurrentUser = async (token: string) => {
    const res = await fetch("http://localhost:8000/api/v1/users/me", {
      headers: { Authorization: `Bearer ${token}` },
      credentials: "include",
    });
    if (res.ok) {
      const user = await res.json() as User;
      setCurrentUser(user);
    } else {
      setCurrentUser(null);
    }
  };

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
    await fetchCurrentUser(data.access_token);
    
    navigate({ to: "/u/companies" });
  };
  
  const logout = async () => {
    const res = await fetch("http://localhost:8000/api/v1/auth/logout", {
      method: "POST",
      headers: { Authorization: `Bearer ${accessToken}` },
      credentials: "include",
    });
    if (!res.ok) throw new Error("Logout failed");
    setAccessToken(null);
    setCurrentUser(null);
    navigate({ to: "/login" });
  };

  // Try to refresh token on mount
  useEffect(() => {
    const tryRefresh = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/v1/auth/refresh", {
          method: "POST",
          credentials: "include",
        });

        if (res.ok) {
          const data = await res.json() as { access_token: string, token_type: string };
          setAccessToken(data.access_token);
          await fetchCurrentUser(data.access_token);
        } else {
          setAccessToken(null);
          setCurrentUser(null);
        }
      } catch {
        setAccessToken(null);
        setCurrentUser(null);
      }
    };
    tryRefresh();
  }, []);

  return (
    <AuthContext.Provider value={{ accessToken, currentUser, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};