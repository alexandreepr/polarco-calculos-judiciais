import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import { AuthContext } from "@/contexts/AuthContext";
import axios from "axios";


export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [loadingAuth, setLoadingAuth] = useState<boolean>(true);
  const navigate = useNavigate();

  const applyAxiosAuthHeader = (token: string | null) => {
    if (token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common["Authorization"];
    }
  };

  const fetchCurrentUser = async (token?: string) => {
    console.log("ACCESS TOKEN", accessToken)
    try {
      const headers = token ? { Authorization: `Bearer ${token}` } : undefined;
      const res = await axios.get("/api/v1/users/me", { headers, withCredentials: true });
      setCurrentUser(res.data);
    } catch (err) {
      setCurrentUser(null);
    }
  };


  const login = async (username: string, password: string) => {
    const form = new FormData();
    form.append("username", username);
    form.append("password", password);

    const res = await axios.post("/api/v1/auth/token", form, { withCredentials: true });
    if (res.status !== 200) throw new Error("Login failed");

    const data = res.data as { access_token: string; token_type: string };
  
    setAccessToken(data.access_token);
    applyAxiosAuthHeader(data.access_token);
    
    await fetchCurrentUser(data.access_token);

    setLoadingAuth(false);
    navigate({ to: "/u/companies" });
  };

  const logout = async () => {
    await axios.post(
      "/api/v1/auth/logout",
      {},
      {
        headers: { Authorization: `Bearer ${accessToken ?? ""}` },
        withCredentials: true,
      }
    );
    
    setAccessToken(null);
    applyAxiosAuthHeader(null);
    setCurrentUser(null);
    navigate({ to: "/login" });
  };

  // Try to refresh token on mount
  useEffect(() => {
    const tryRefresh = async () => {
      setLoadingAuth(true);
      try {
        const res = await axios.post("/api/v1/auth/refresh", {}, { withCredentials: true });
        if (res.status === 200 && res.data?.access_token) {
          console.log(res.data)
          const token = res.data.access_token as string;
          setAccessToken(token);
          console.log("ACCESS TOKEN IN USEEFFECT", token);

          applyAxiosAuthHeader(token);
          await fetchCurrentUser(token);
        } else {
          setAccessToken(null);
          applyAxiosAuthHeader(null);
          setCurrentUser(null);
        }
      } catch {
        setAccessToken(null);
        applyAxiosAuthHeader(null);
        setCurrentUser(null);
      } finally {
        setLoadingAuth(false);
      }
    };

    tryRefresh();
  }, []);

  const contextValue = React.useMemo(
    () => ({
      accessToken,
      currentUser,
      loadingAuth,
      login,
      logout,
    }),
    [accessToken, currentUser, loadingAuth, login, logout]
  );

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};