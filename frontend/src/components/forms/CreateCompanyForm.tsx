import { useState } from "react";
import { Button } from "@/components/ui/button";
import { API_URL } from "@/common/config";
import { useNavigate } from "@tanstack/react-router";
import { useAuth } from "@/common/AuthProvider";
import axios from "axios";
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
  const { loadingAuth } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await axios.post(
        "/api/v1/companies",
        { name, cnpj },
        { withCredentials: true }
      );

      const data: any = res.data;
      setName("");
      setCnpj("");
      onSuccess();
      navigate({ to: `/u/company/${data.id}/dashboard` });
    } catch (err: any) {
      const msg =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        err?.message ||
        "Erro ao criar empresa";
      setError(msg);
    } finally {
      setLoading(false);
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
        disabled={loading || loadingAuth}
      />
      <input
        className="border px-2 py-1 rounded"
        value={cnpj}
        onChange={e => setCnpj(e.target.value)}
        placeholder="CNPJ"
        required
        disabled={loading || loadingAuth}
      />
      <Button type="submit" disabled={loading || !name.trim() || !cnpj.trim()}>
        {loading ? "Criando..." : "Criar"}
      </Button>
      {error && <span className="text-red-500 text-xs">{error}</span>}
    </form>
  );
}