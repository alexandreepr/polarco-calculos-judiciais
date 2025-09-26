import { useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useState } from "react";
import { Company } from "@/types/company";
// import { API_URL } from "@/common/config";
import { CreateCompanyForm } from "@/components/forms/CreateCompanyForm";
import { Avatar } from "@radix-ui/react-avatar";
import { useAuth } from "@/common/AuthProvider";

export function Companies() {
  const {accessToken} = useAuth()
  const [showCreate, setShowCreate] = useState(false);

  // Fetch companies the user is a member of
  const { data: companies = [], isLoading } = useQuery<Company[]>({
    queryKey: ["companies"],
    queryFn: async () => {
      const res = await fetch( `http://localhost:8000/api/v1/companies/me`, {     
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      if (!res.ok) {
        throw new Error("Failed to fetch companies");
      }
      return res.json() as Promise<Company[]>;
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
              {company.name?.[0]?.toUpperCase() ?? "?"}
            </Avatar>
            <div className="flex-1">
              <div className="text-lg font-semibold">{company.name}</div>
              {/* Add more company info here if needed */}
            </div>
            <Button variant="outline">Selecionar</Button>
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
