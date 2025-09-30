import axios from "axios";
import { useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useState } from "react";
import { Company } from "@/types/company";
// import { API_URL } from "@/common/config";
import { CreateCompanyForm } from "@/components/forms/CreateCompanyForm";
import { Avatar } from "@radix-ui/react-avatar";
import { useAuth } from "@/common/AuthProvider";
import { useNavigate } from "@tanstack/react-router";
import { AvatarImage } from "@/components/ui/avatar";

export function Companies() {
  const { loadingAuth } = useAuth();
  const [showCreate, setShowCreate] = useState(false);
  const navigate = useNavigate()

  // Fetch companies the user is a member of
  const { data: companies = [], isLoading } = useQuery<Company[]>({
    queryKey: ["companies"],
    enabled: !loadingAuth, // don't run until AuthProvider finished
    queryFn: async () => {
      try {
        const res = await axios.get("/api/v1/companies/me", {
          withCredentials: true,
        });
        return res.data as Company[];
      } catch (err: any) {
        throw new Error(err?.response?.data?.detail || "Failed to fetch companies");
      }
    },
  });

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] bg-background">
      <h1 className="text-3xl font-bold mb-8">Suas Empresas</h1>
      <div className="w-full max-w-2xl flex flex-col gap-6">
        {companies.length === 0 && (
          <div className="text-center text-muted-foreground">Nenhuma empresa encontrada.</div>
        )}
        {companies.map((company) => (
          <Card
            key={company.id}
            className="flex items-center gap-4 p-6 rounded-xl shadow-md bg-card"
            style={{ minHeight: 96 }}
          >
            <Avatar
              className="w-16 h-16 rounded-md bg-primary text-primary-foreground flex items-center justify-center text-2xl font-bold select-none"
            >
              <AvatarImage src="/Logo_PBL_Fundo_Verde.jpg" alt="Company Logo" />
            </Avatar>
            <div className="flex-1">
              <div className="text-lg font-semibold">{company.name}</div>
            </div>
            <Button variant="outline" onClick={() => navigate({ to: `/u/company/${company.id}/dashboard` })}>Selecionar</Button>
          </Card>
        ))}
      </div>
      <Button className="mt-10" onClick={() => setShowCreate(true)}>
        Criar nova empresa
      </Button>
      {showCreate && (
        <div className="mt-6 w-full max-w-md">
          <CreateCompanyForm onSuccess={() => setShowCreate(false)} />
        </div>
      )}
    </div>
  );
}
