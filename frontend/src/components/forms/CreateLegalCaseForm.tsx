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

  const [form, setForm] = useState<any>({
    // basic
    legal_case_number: "",
    clients: [{ name: "", cpf: "" }],
    status: "",
    assignee_from_commercial_team_id: "",
    assignee_from_litigation_team_id: "",

    // case dates (model names)
    filing_date: "",
    final_judgment_date: "",
    citation_date: "",
    damage_event_date: "",
    judgment_date: "",
    appellate_decision_date: "",

    // moral (non-pecuniary) damage
    nominal_moral_damage: "",                      // VALOR DOS DANOS MORAIS (not in model originally, included for form)
    moral_index_start_date: "",                    // ATUALIZAÇÃO A PARTIR (DANOS MORAIS)
    moral_interest_start_date: "",                 // JUROS A PARTIR (DANOS MORAIS)
    moral_index_type: "",                          // INDICE ATUALIZAÇAO DANOS MORAIS (MonetaryIndexType)
    moral_interest_index_type: "",                 // INDICE JUROS DANOS MORAIS (InterestIndexType)

    // material (pecuniary) damage
    first_installment_date: "",                    // DATA DA PRIMEIRA PARCELA
    last_installment_date: "",                     // DATA DA ÚLTIMA PARCELA
    first_installment_amount: "",                  // VALOR DA PRIMEIRA PARCELA
    last_installment_amount: "",                   // VALOR DA ÚLTIMA PARCELA
    material_resolution: "",                       // ANULADO / CONVERTIDO (MaterialResolutionType)
    material_interest_multiplier: "",              // SIMPLES / DOBRADO (InterestMultiplierType)
    material_index_start_date: "",                 // ATUALIZAÇÃO A PARTIR (DANOS MATERIAIS)
    material_interest_start_date: "",              // JUROS A PARTIR (DANOS MATERIAIS)
    material_index_type: "",                       // INDICE ATUALIZACAO DANOS MATERIAIS (MonetaryIndexType)
    material_interest_index_type: "",              // INDICE JUROS DANOS MATERIAIS (InterestIndexType)
    nominal_material_damage: "",                   // VALOR DOS DANOS MATERIAIS (if needed)

    // case value & fees
    case_value_basis: "",                          // CONDEMNATION_AMOUNT / CLAIM_AMOUNT / SPECIFIED_AMOUNT
    case_value: "",
    attorney_fees_value: "",
    percentage_contractual_attorney_fees: "",
    percentage_court_awarded_attorney_fees: "",
    proportion_court_awarded_attorney_fees: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function setField<K extends string>(name: K, value: any) {
    setForm((prev: any) => ({ ...prev, [name]: value }));
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    const { name, value } = e.target;
    setField(name, value);
  }

  function handleClientChange(idx: number, field: "name" | "cpf", value: string) {
    const updatedClients = (form.clients || []).map((client: any, i: number) =>
      i === idx ? { ...client, [field]: value } : client
    );
    setField("clients", updatedClients);
  }

  function addClient() {
    setField("clients", [...(form.clients || []), { name: "", cpf: "" }]);
  }

  function removeClient(idx: number) {
    setField("clients", (form.clients || []).filter((_: any, i: number) => i !== idx));
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
        "nominal_moral_damage",
        "nominal_material_damage",
        "first_installment_amount",
        "last_installment_amount",
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

        // convert dates to ISO if they look like HTML date inputs (they already provide ISO YYYY-MM-DD)
        if (["filing_date","final_judgment_date","citation_date","damage_event_date","judgment_date","appellate_decision_date","moral_index_start_date","moral_interest_start_date","first_installment_date","last_installment_date","material_index_start_date","material_interest_start_date"].includes(key)) {
          payload[key] = value; // keep as string YYYY-MM-DD (backend will parse)
          return;
        }

        if (numberFields.has(key)) {
          const valueAsNumber = Number(value);
          if (!Number.isNaN(valueAsNumber)) payload[key] = valueAsNumber;
          return;
        }

        // selects and enums should be sent as the enum string values expected by API
        payload[key] = value;
      });

      if (company_id) payload.company_id = company_id;

      await axios.post("/api/v1/legal-cases/", payload, { withCredentials: true });
      navigate({ to: `/u/company/${company_id}/legal-cases` });
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
        <div className="col-span-2" />
        <div className="col-span-8">
          <form className="space-y-6" onSubmit={handleSubmit}>
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
                  <Label htmlFor="legal_case_number">Nº do Processo*</Label>
                  <Input id="legal_case_number" name="legal_case_number" value={form.legal_case_number} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label>Clientes*</Label>
                  <div className="space-y-2">
                    {form.clients.map((c: any, i: number) => (
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
                  <Label htmlFor="status">Status*</Label>
                  <Select value={form.status} onValueChange={(v: string) => setField("status", v)}>
                    <SelectTrigger className="h-8">
                      <SelectValue placeholder="Selecione" />
                    </SelectTrigger>
                    <SelectContent align="end">
                      <SelectItem value="ativo">Ativo</SelectItem>
                      <SelectItem value="encerrado">Encerrado</SelectItem>
                    </SelectContent>
                  </Select>

                  <div className="mt-3">
                    <Label htmlFor="assignee_from_commercial_team_id">Responsável Contencioso</Label>
                    <Input id="assignee_from_commercial_team_id" name="assignee_from_commercial_team_id" value={form.assignee_from_commercial_team_id} onChange={handleChange} />
                  </div>

                  <div className="mt-3">
                    <Label htmlFor="assignee_from_litigation_team_id">Responsável Jurídico</Label>
                    <Input id="assignee_from_litigation_team_id" name="assignee_from_litigation_team_id" value={form.assignee_from_litigation_team_id} onChange={handleChange} />
                  </div>
                </div>
              </div>
            </section>

            <section className="bg-white border rounded p-4">
              <h3 className="text-sm font-medium mb-3">Datas do Processo</h3>
              <div className="grid grid-cols-3 gap-4">
                <div className="flex flex-col">
                  <Label htmlFor="filing_date">Data de Ajuizamento</Label>
                  <Input id="filing_date" name="filing_date" type="date" value={form.filing_date} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="final_judgment_date">Data do Trânsito em Julgado</Label>
                  <Input id="final_judgment_date" name="final_judgment_date" type="date" value={form.final_judgment_date} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="citation_date">Data da Citação</Label>
                  <Input id="citation_date" name="citation_date" type="date" value={form.citation_date} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="damage_event_date">Data do Evento Danoso</Label>
                  <Input id="damage_event_date" name="damage_event_date" type="date" value={form.damage_event_date} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="judgment_date">Data da Sentença</Label>
                  <Input id="judgment_date" name="judgment_date" type="date" value={form.judgment_date} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="appellate_decision_date">Data do Acórdão</Label>
                  <Input id="appellate_decision_date" name="appellate_decision_date" type="date" value={form.appellate_decision_date} onChange={handleChange} />
                </div>
              </div>
            </section>

            <section className="bg-white border rounded p-4">
              <h3 className="text-sm font-medium mb-3">Dados Danos Morais</h3>
              <div className="grid grid-cols-4 gap-4">
                <div className="col-span-2 flex flex-col">
                  <Label htmlFor="nominal_moral_damage">Valor dos Danos Morais</Label>
                  <Input id="nominal_moral_damage" name="nominal_moral_damage" type="number" value={form.nominal_moral_damage} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="moral_index_start_date">Atualização a partir</Label>
                  <Input id="moral_index_start_date" name="moral_index_start_date" type="date" value={form.moral_index_start_date} onChange={handleChange} />
                </div>
                <div className="flex flex-col">
                  <Label htmlFor="moral_interest_start_date">Juros a partir</Label>
                  <Input id="moral_interest_start_date" name="moral_interest_start_date" type="date" value={form.moral_interest_start_date} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="moral_index_type">Índice Atualização</Label>
                  <Select value={form.moral_index_type} onValueChange={(v: string) => setField("moral_index_type", v)}>
                    <SelectTrigger className="h-8 w-full">
                      <SelectValue placeholder="Selecione" />
                    </SelectTrigger>
                    <SelectContent align="end">
                      <SelectItem value="IPCA">IPCA</SelectItem>
                      <SelectItem value="INPC">INPC</SelectItem>
                      <SelectItem value="IGP-M">IGP-M</SelectItem>
                      <SelectItem value="OTHER">OTHER</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="moral_interest_index_type">Índice Juros</Label>
                  <Select value={form.moral_interest_index_type} onValueChange={(v: string) => setField("moral_interest_index_type", v)}>
                    <SelectTrigger className="h-8 w-full"><SelectValue placeholder="Selecione" /></SelectTrigger>
                    <SelectContent align="end">
                      <SelectItem value="1_PERCENT">1%</SelectItem>
                      <SelectItem value="SELIC">SELIC</SelectItem>
                      <SelectItem value="LEGAL_RATE">LEGAL_RATE</SelectItem>
                      <SelectItem value="OTHER">OTHER</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </section>

            <section className="bg-white border rounded p-4">
              <h3 className="text-sm font-medium mb-3">Dados Danos Materiais</h3>
              <div className="grid grid-cols-4 gap-4">
                <div className="flex flex-col">
                  <Label htmlFor="first_installment_date">Data da Primeira Parcela</Label>
                  <Input id="first_installment_date" name="first_installment_date" type="date" value={form.first_installment_date} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="last_installment_date">Data da Última Parcela</Label>
                  <Input id="last_installment_date" name="last_installment_date" type="date" value={form.last_installment_date} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="first_installment_amount">Valor da Primeira Parcela</Label>
                  <Input id="first_installment_amount" name="first_installment_amount" type="number" value={form.first_installment_amount} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="last_installment_amount">Valor da Última Parcela</Label>
                  <Input id="last_installment_amount" name="last_installment_amount" type="number" value={form.last_installment_amount} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="material_resolution">Anulado / Convertido</Label>
                  <Select value={form.material_resolution} onValueChange={(v: string) => setField("material_resolution", v)}>
                    <SelectTrigger className="h-8 w-full"><SelectValue placeholder="Selecione" /></SelectTrigger>
                    <SelectContent align="end">
                      <SelectItem value="ANNULLED">Anulado</SelectItem>
                      <SelectItem value="CONVERTED">Convertido</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="material_interest_multiplier">Simples / Dobrado</Label>
                  <Select value={form.material_interest_multiplier} onValueChange={(v: string) => setField("material_interest_multiplier", v)}>
                    <SelectTrigger className="h-8 w-full"><SelectValue placeholder="Selecione" /></SelectTrigger>
                    <SelectContent align="end">
                      <SelectItem value="SIMPLE">Simples</SelectItem>
                      <SelectItem value="DOUBLED">Dobrado</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="material_index_start_date">Atualização a Partir</Label>
                  <Input id="material_index_start_date" name="material_index_start_date" type="date" value={form.material_index_start_date} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="material_interest_start_date">Juros a Partir</Label>
                  <Input id="material_interest_start_date" name="material_interest_start_date" type="date" value={form.material_interest_start_date} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="material_index_type">Índice Atualização</Label>
                  <Select value={form.material_index_type} onValueChange={(v: string) => setField("material_index_type", v)}>
                    <SelectTrigger className="h-8 w-full"><SelectValue placeholder="Selecione" /></SelectTrigger>
                    <SelectContent align="end">
                      <SelectItem value="IPCA">IPCA</SelectItem>
                      <SelectItem value="INPC">INPC</SelectItem>
                      <SelectItem value="IGP-M">IGP-M</SelectItem>
                      <SelectItem value="OTHER">OTHER</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="material_interest_index_type">Índice Juros</Label>
                  <Select value={form.material_interest_index_type} onValueChange={(v: string) => setField("material_interest_index_type", v)}>
                    <SelectTrigger className="h-8 w-full"><SelectValue placeholder="Selecione" /></SelectTrigger>
                    <SelectContent align="end">
                      <SelectItem value="1_PERCENT">1%</SelectItem>
                      <SelectItem value="SELIC">SELIC</SelectItem>
                      <SelectItem value="LEGAL_RATE">LEGAL_RATE</SelectItem>
                      <SelectItem value="OTHER">OTHER</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </section>

            <section className="bg-white border rounded p-4">
              <h3 className="text-sm font-medium mb-3">Honorários & Valor da Causa</h3>
              <div className="grid grid-cols-4 gap-4">
                <div className="flex flex-col">
                  <Label htmlFor="case_value_basis">Parâmetro do Valor</Label>
                  <Select value={form.case_value_basis} onValueChange={(v: string) => setField("case_value_basis", v)}>
                    <SelectTrigger className="h-8 w-full"><SelectValue placeholder="Selecione" /></SelectTrigger>
                    <SelectContent align="end">
                      <SelectItem value="CONDEMNATION_AMOUNT">Valor da Condenação</SelectItem>
                      <SelectItem value="CLAIM_AMOUNT">Valor da Causa</SelectItem>
                      <SelectItem value="SPECIFIED_AMOUNT">Quantia Certa</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="case_value">Valor da Causa</Label>
                  <Input id="case_value" name="case_value" type="number" value={form.case_value} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="attorney_fees_value">Valor dos Honorários</Label>
                  <Input id="attorney_fees_value" name="attorney_fees_value" type="number" value={form.attorney_fees_value} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="percentage_contractual_attorney_fees">Percentual Honorários Contratuais</Label>
                  <Input id="percentage_contractual_attorney_fees" name="percentage_contractual_attorney_fees" value={form.percentage_contractual_attorney_fees} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="percentage_court_awarded_attorney_fees">Percentual Honorários Sucumbenciais</Label>
                  <Input id="percentage_court_awarded_attorney_fees" name="percentage_court_awarded_attorney_fees" value={form.percentage_court_awarded_attorney_fees} onChange={handleChange} />
                </div>

                <div className="flex flex-col">
                  <Label htmlFor="proportion_court_awarded_attorney_fees">Proporção Honorários Sucumbenciais</Label>
                  <Input id="proportion_court_awarded_attorney_fees" name="proportion_court_awarded_attorney_fees" value={form.proportion_court_awarded_attorney_fees} onChange={handleChange} />
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