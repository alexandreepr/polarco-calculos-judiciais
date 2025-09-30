import React, { createContext, useContext, useState, useEffect } from "react";
import { useParams } from "@tanstack/react-router";
import { Company } from "@/types/company";
import { useAuth } from "./AuthProvider";
import axios from "axios";

type CompanyContextType = {
  companyId: string | undefined;
  currentCompany?: Company;
  setCurrentCompany: (data: any) => void;
};

const CompanyContext = createContext<CompanyContextType | undefined>(undefined);

export function CompanyProvider({ children }: { children: React.ReactNode }) {
  const { company_id } = useParams({ from: "/u/company/$company_id" });
  const [currentCompany, setCurrentCompany] = useState<Company | undefined>(undefined);
  const { loadingAuth } = useAuth(); // wait until AuthProvider finished (axios defaults applied)

  useEffect(() => {
    // don't run until AuthProvider finished (so axios.defaults.Authorization is set if available)
    if (!company_id || loadingAuth) {
      if (!company_id) setCurrentCompany(undefined);
      return;
    }

    const source = axios.CancelToken.source();

    (async () => {
      try {
        const res = await axios.get(`/api/v1/companies/${company_id}`, {
          withCredentials: true,
          cancelToken: source.token,
        });
        setCurrentCompany(res.data as Company);
      } catch (err: any) {
        if (axios.isCancel(err)) return;
        setCurrentCompany(undefined);
      }
    })();

    return () => {
      source.cancel("Request canceled by cleanup");
    };
  }, [company_id, loadingAuth]);

  return (
    <CompanyContext.Provider value={{ companyId: company_id, currentCompany, setCurrentCompany }}>
      {children}
    </CompanyContext.Provider>
  );
}

export function useCompany() {
  const ctx = useContext(CompanyContext);
  if (!ctx) throw new Error("useCompany must be used within a CompanyProvider");
  return ctx;
}