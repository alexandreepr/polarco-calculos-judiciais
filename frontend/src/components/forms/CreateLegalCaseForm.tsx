import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { useNavigate, useParams } from "@tanstack/react-router";
import axios from "axios";

export function CreateLegalCaseForm() {
  const navigate = useNavigate();
  const { company_id } = useParams({ from: "/u/company/$company_id/legal-cases/new" });

  const [form, setForm] = useState({
    legal_case_number: "",
    case_value: "",
    attorney_fees_value: "",
    percentage_court_awarded_attorney_fees: "",
    proportion_court_awarded_attorney_fees: "",
    percentage_contractual_attorney_fees: "",
    case_subject: "",
    state: "",
    jurisdiction: "",
    judicial_district: "",
    court: "",
    defendant: "",
    attorney: "",
    status: "",
    clients: [{ name: "", cpf: "" }],
    assignee_from_commercial_team_id: "",
    assignee_from_litigation_team_id: "",
    // dates
    date_ajustamento: "",
    date_transito: "",
    date_citacao: "",
    date_evento_danoso: "",
    date_sentenca: "",
    date_acordo: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function setField<K extends string>(name: K, value: any) {
    setForm(prev => ({ ...prev, [name]: value }));
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    const { name, value } = e.target;
    setField(name, value);
  }

  function handleClientChange(idx: number, field: "name" | "cpf", value: string) {
    const updatedClients = form.clients.map((client, i) =>
      i === idx ? { ...client, [field]: value } : client
    );
    setField("clients", updatedClients);
  }

  function addClient() {
    setField("clients", [...form.clients, { name: "", cpf: "" }]);
  }

  function removeClient(idx: number) {
    setField("clients", form.clients.filter((_, i) => i !== idx));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const numberFields = new Set([
        "case_value",
        "attorney_fees_value",
        "percentage_court_awarded_attorney_fees",
        "proportion_court_awarded_attorney_fees",
        "percentage_contractual_attorney_fees",
        "valor_danos_morais",
        "valor_primeira_parcela",
        "valor_ultima_parcela",
      ]);

      const payload: any = {};
      Object.entries(form).forEach(([key, value]) => {
        if (key === "clients") {
          const clients = (value as any[]).filter(
            c => (c.name && c.name.trim()) || (c.cpf && c.cpf.trim())
          );
          if (clients.length) payload.clients = clients;
          return;
        }

        if (value === "" || value === null || value === undefined) return;

        if (numberFields.has(key)) {
          const valueAsNumber = Number(value);
          if (!Number.isNaN(valueAsNumber)) payload[key] = valueAsNumber;
          return;
        }

        payload[key] = value;
      });

      if (company_id) payload.company_id = company_id;

      await axios.post("/api/v1/legal-cases/", payload, { withCredentials: true }).then(() => {
          navigate({ to: `/u/company/${company_id}/legal-cases` });
      });
    } catch (err: any) {
      const msg =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        err?.message ||
        "Erro ao criar processo";
      setError(Array.isArray(msg) ? JSON.stringify(msg) : String(msg));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen px-6 py-8">
      <div className="max-w-14xl mx-auto grid grid-cols-12 gap-6">
        {/* left gutter */}
        <div className="col-span-2" />
        {/* centered form column */}
        <div className="col-span-8">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {/* header + actions */}
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold">Criar Processo</h2>
            </div>

            <div className="flex gap-2">
              <Button variant="outline" size="sm">DADOS DO CÁLCULO</Button>
              <Button variant="outline" size="sm">DADOS CONTRATO</Button>
              <Button variant="outline" size="sm">CÁLCULOS JURÍDICO</Button>
              <Button variant="outline" size="sm">CÁLCULOS CUMPRIMENTO</Button>
            </div>

            <section className="bg-white border rounded p-4">
              <h3 className="text-sm font-medium mb-3">Dados do Processo</h3>

              <div className="grid grid-cols-3 gap-4">
                <div className="flex flex-col">
                  <Label htmlFor="legal_case_number">Número do Processo</Label>
                  <Input id="legal_case_number" name="legal_case_number" value={form.legal_case_number} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label>Clientes</Label>
                  <div className="space-y-2">
                    {form.clients.map((c, i) => (
                      <div key={i} className="grid grid-cols-3 gap-2 items-end">
                        <div className="col-span-2">
                          <Label htmlFor={`client_name_${i}`} className="sr-only">Nome</Label>
                          <Input id={`client_name_${i}`} name={`client_name_${i}`} placeholder="Nome" value={c.name} onChange={e => handleClientChange(i, "name", e.target.value)} />
                        </div>
                        <div>
                          <Label htmlFor={`client_cpf_${i}`} className="sr-only">CPF</Label>
                          <Input id={`client_cpf_${i}`} name={`client_cpf_${i}`} placeholder="CPF" value={c.cpf} onChange={e => handleClientChange(i, "cpf", e.target.value)} />
                        </div>
                      </div>
                    ))}
                    <div className="flex gap-2">
                      <Button type="button" size="sm" onClick={addClient}>+ Adicionar Cliente</Button>
                    </div>
                  </div>
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="status">Status</Label>
                  <Select value={form.status} onValueChange={v => setField("status", v)}>
                    <SelectTrigger className="h-8">
                      <SelectValue placeholder="Selecione" />
                    </SelectTrigger>
                    <SelectContent align="end">
                      <SelectItem value="ativo">Ativo</SelectItem>
                      <SelectItem value="encerrado">Encerrado</SelectItem>
                    </SelectContent>
                  </Select>

                  <div className="mt-3">
                    <Label htmlFor="assignee_from_commercial_team_id">Responsável Comercial (ID)</Label>
                    <Input id="assignee_from_commercial_team_id" name="assignee_from_commercial_team_id" value={form.assignee_from_commercial_team_id} onChange={handleChange} />
                  </div>

                  <div className="mt-3">
                    <Label htmlFor="assignee_from_litigation_team_id">Responsável Jurídico (ID)</Label>
                    <Input id="assignee_from_litigation_team_id" name="assignee_from_litigation_team_id" value={form.assignee_from_litigation_team_id} onChange={handleChange} />
                  </div>
                </div>
              </div>
            </section>

            <section className="bg-white border rounded p-4">
              <h3 className="text-sm font-medium mb-3">Datas do Processo</h3>
              <div className="grid grid-cols-3 gap-4">
                <div className="flex flex-col">
                  <Label htmlFor="date_ajustamento">Data de Ajustamento</Label>
                  <Input id="date_ajustamento" name="date_ajustamento" type="date" value={form.date_ajustamento} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="date_transito">Data do Trânsito em Julgado</Label>
                  <Input id="date_transito" name="date_transito" type="date" value={form.date_transito} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="date_citacao">Data da Citação</Label>
                  <Input id="date_citacao" name="date_citacao" type="date" value={form.date_citacao} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="date_evento_danoso">Data do Evento Danoso</Label>
                  <Input id="date_evento_danoso" name="date_evento_danoso" type="date" value={form.date_evento_danoso} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="date_sentenca">Data da Sentença</Label>
                  <Input id="date_sentenca" name="date_sentenca" type="date" value={form.date_sentenca} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="date_acordo">Data do Acordo</Label>
                  <Input id="date_acordo" name="date_acordo" type="date" value={form.date_acordo} onChange={handleChange} />
                </div>
              </div>
            </section>

            <section className="bg-white border rounded p-4">
              <h3 className="text-sm font-medium mb-3">Dados Danos Morais</h3>
              <div className="grid grid-cols-4 gap-4">
                <div className="col-span-2 flex flex-col">
                  <Label htmlFor="valor_danos_morais">Valor Danos Morais</Label>
                  <Input id="valor_danos_morais" name="valor_danos_morais" value={(form as any).valor_danos_morais || ""} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="indice_atualizacao_danos_morais">Índice Atualização</Label>
                  <Input id="indice_atualizacao_danos_morais" name="indice_atualizacao_danos_morais" value={(form as any).indice_atualizacao_danos_morais || ""} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="juros_danos_morais">Juros a partir</Label>
                  <Input id="juros_danos_morais" name="juros_danos_morais" value={(form as any).juros_danos_morais || ""} onChange={handleChange} />
                </div>
              </div>
            </section>

            <section className="bg-white border rounded p-4">
              <h3 className="text-sm font-medium mb-3">Dados Danos Materiais</h3>
              <div className="grid grid-cols-4 gap-4">
                <div className="flex flex-col">
                  <Label htmlFor="tipo_danos_materiais">Tipo</Label>
                  <Select value={(form as any).tipo_danos_materiais || ""} onValueChange={v => setField("tipo_danos_materiais", v)}>
                    <SelectTrigger className="h-8 w-full">
                      <SelectValue placeholder="Selecione" />
                    </SelectTrigger>
                    <SelectContent align="end">
                      <SelectItem value="simples">Simples</SelectItem>
                      <SelectItem value="dobrado">Dobrado</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="valor_primeira_parcela">Valor Primeira Parcela</Label>
                  <Input id="valor_primeira_parcela" name="valor_primeira_parcela" value={(form as any).valor_primeira_parcela || ""} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="valor_ultima_parcela">Valor Última Parcela</Label>
                  <Input id="valor_ultima_parcela" name="valor_ultima_parcela" value={(form as any).valor_ultima_parcela || ""} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="indice_atualizacao_danos_materiais">Índice Atualização</Label>
                  <Input id="indice_atualizacao_danos_materiais" name="indice_atualizacao_danos_materiais" value={(form as any).indice_atualizacao_danos_materiais || ""} onChange={handleChange} />
                </div>
              </div>
            </section>

            <section className="bg-white border rounded p-4">
              <h3 className="text-sm font-medium mb-3">Honorários Sucumbenciais</h3>
              <div className="grid grid-cols-4 gap-4">
                <div className="flex flex-col">
                  <Label htmlFor="parametro_honorarios">Parâmetro dos Honorários</Label>
                  <Input id="parametro_honorarios" name="parametro_honorarios" value={(form as any).parametro_honorarios || ""} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="valor_da_causa">Valor da Causa</Label>
                  <Input id="valor_da_causa" name="case_value" type="number" value={form.case_value} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="percentual_honorarios">Percentual</Label>
                  <Input id="percentual_honorarios" name="percentage_court_awarded_attorney_fees" value={form.percentage_court_awarded_attorney_fees} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="indice_juros_honorarios">Índice Juros</Label>
                  <Input id="indice_juros_honorarios" name="indice_juros_honorarios" value={(form as any).indice_juros_honorarios || ""} onChange={handleChange} />
                </div>
              </div>
            </section>

            {error && <div className="text-red-600">{error}</div>}
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="sm" onClick={() => navigate({ to: `/u/company/${company_id}/legal-cases` })}>
                Cancelar
              </Button>
              <Button type="submit" size="sm" disabled={loading}>
                {loading ? "Criando..." : "+ Criar Processo"}
              </Button>
            </div>
          </form>
        </div>

        <div className="col-span-2" />
      </div>
    </div>
  );
}