import { useState } from "react";
import { Button } from "@/components/ui/button";
import { API_URL } from "@/common/config";
import { useNavigate } from "@tanstack/react-router";
import { useAuth } from "@/common/AuthProvider";
// import { API_URL } from "@/common/config";

export interface CreateCompanyFormProps {
  onSuccess: () => void;
}

export function CreateCompanyForm({ onSuccess }: CreateCompanyFormProps) {
  const [name, setName] = useState("");
  const [cnpj, setCnpj] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate()

  const { accessToken } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const res = await fetch(`${API_URL}/api/v1/companies`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Bearer ${accessToken}`,
      },
      body: JSON.stringify({ name, cnpj }),
      credentials: "include",
    });
    setLoading(false);
    if (res.ok) {
      setName("");
      setCnpj("");
      onSuccess()
      navigate({ to: "/dashboard" });
    } else {
      const data: any = await res.json().catch(() => ({}));
      setError(data.detail || "Erro ao criar empresa");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2">
      <input
        className="border px-2 py-1 rounded"
        value={name}
        onChange={e => setName(e.target.value)}
        placeholder="Nome da empresa"
        required
        disabled={loading}
      />
      <input
        className="border px-2 py-1 rounded"
        value={cnpj}
        onChange={e => setCnpj(e.target.value)}
        placeholder="CNPJ"
        required
        disabled={loading}
      />
      <Button type="submit" disabled={loading || !name.trim() || !cnpj.trim()}>
        {loading ? "Criando..." : "Criar"}
      </Button>
      {error && <span className="text-red-500 text-xs">{error}</span>}
    </form>
  );
}