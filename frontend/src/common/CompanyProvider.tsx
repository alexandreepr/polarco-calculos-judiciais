import React, { createContext, useContext, useState, useEffect } from "react";
import { useParams } from "@tanstack/react-router";
import { Company } from "@/types/company";
import { API_URL } from "./config";
import { useAuth } from "./AuthProvider";

type CompanyContextType = {
  companyId: string | undefined;
  currentCompany?: Company;
  setCurrentCompany: (data: any) => void;
};

const CompanyContext = createContext<CompanyContextType | undefined>(undefined);

export function CompanyProvider({ children }: { children: React.ReactNode }) {
  const { company_id } = useParams({ from: "/u/company/$company_id" });
  const [currentCompany, setCurrentCompany] = useState<Company | undefined>(undefined);
  const { accessToken } = useAuth();

  useEffect(() => {
    if (company_id && accessToken) {
      fetch(`${API_URL}/api/v1/companies/${company_id}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
        credentials: "include",
      })
        .then(res => {
          if (!res.ok){
            throw new Error("Failed to fetch company");
          }
          
          return res.json() as Promise<Company>;
        })
        .then((data: Company) => setCurrentCompany(data))
        .catch(() => setCurrentCompany(undefined));
    }
  }, [company_id, accessToken]);

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