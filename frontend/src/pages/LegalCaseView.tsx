import { AppSidebar } from "@/components/layout/AppSidebar/AppSidebar";
import { SiteHeader } from "@/components/layout/Header/Header";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { useParams, useNavigate } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { useAuth } from "@/common/AuthProvider";
import { Button } from "@/components/ui/button";
import React from "react";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

function formatValue(v: any) {
  if (v === null || v === undefined || v === "") {
    return "—";
  }

  if (typeof v === "string" && /\d{4}-\d{2}-\d{2}/.test(v)) {
    try {
      return new Date(v).toLocaleDateString();
    } catch {
      /* fallthrough */
    }
  }
  if (typeof v === "number") {
    return v.toLocaleString();
  }
  return String(v);
}

function formatLegalCaseNumber(v: any) {
  if (v === null || v === undefined || v === "") return "—";
  const digits = String(v).replace(/\D/g, "");

  if (digits.length !== 20) {
    return String(v);
  }

  return `${digits.slice(0, 7)}-${digits.slice(7, 9)}.${digits.slice(9, 13)}.${digits.slice(
    13,
    14
  )}.${digits.slice(14, 16)}.${digits.slice(16, 20)}`;
}

/**
 * Simple calculations table component adapted to project UI.
 * - shows columns inspired by provided screenshot: ID, Description, Version, User, Date, Value
 * - top-right button to create a new calculation (navigates to a route; adapt route if needed)
 */
function CalculationsTable({
  title,
  companyId,
  legalCaseId,
  calculations,
  onCreate,
  loading,
}: {
  title: string;
  companyId?: string | null;
  legalCaseId?: string | null;
  calculations?: any[];
  onCreate: () => void;
  loading?: boolean;
}) {
  const rows = calculations || [];

  return (
    <section className="bg-white border rounded p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium">{title}</h3>
        <div className="flex items-center gap-2">
          <Button
            size="sm"
            onClick={onCreate}
            className="ml-auto"
          >
            Novo cálculo avulso
          </Button>
        </div>
      </div>

      <div className="overflow-hidden rounded border">
        <Table>
          <TableHeader className="sticky top-0 z-10 bg-muted">
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Descrição</TableHead>
              <TableHead>Versão</TableHead>
              <TableHead>Usuário</TableHead>
              <TableHead>Data</TableHead>
              <TableHead className="text-right">Valor</TableHead>
            </TableRow>
          </TableHeader>

          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={6} className="h-24 text-center">
                  Loading...
                </TableCell>
              </TableRow>
            ) : rows.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="h-24 text-center">
                  Nenhum cálculo
                </TableCell>
              </TableRow>
            ) : (
              rows.map((c) => (
                <TableRow key={c.id}>
                  <TableCell>{String(c.id).slice(-6)}</TableCell>
                  <TableCell className="max-w-md truncate">{c.description || c.calculation_type || "—"}</TableCell>
                  <TableCell>{c.version ?? "1"}</TableCell>
                  <TableCell>{c.created_by_name ?? c.created_by_id ?? "—"}</TableCell>
                  <TableCell>{formatValue(c.created_at ?? c.calculation_date)}</TableCell>
                  <TableCell className="text-right">{formatValue(c.total_judgement_amount ?? c.total_judgment_without_interest ?? c.nominal_material_damage ?? c.nominal_moral_damage)}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </section>
  );
}

export function LegalCasesView() {
  const navigate = useNavigate();
  const { company_id, legal_case_id } = useParams({
    from: "/u/company/$company_id/legal-cases/$legal_case_id/",
  });
  const { loadingAuth } = useAuth();
  const [activeTab, setActiveTab] = React.useState("legalCaseDetails");

  const { data: legalCase, isLoading, error } = useQuery({
    queryKey: ["legal-case", legal_case_id],
    queryFn: async () => {
      const res = await axios.get(`/api/v1/legal-cases/${legal_case_id}`, { withCredentials: true });
      return res.data;
    },
    enabled: !!legal_case_id && !loadingAuth,
  });

  const { data: calculations = [], isLoading: loadingCalculations } = useQuery({
    queryKey: ["legal-case-calculations", legal_case_id],
    queryFn: async () => {
      const res = await axios.get(`/api/v1/legal-calculations/calculations-by-legal-case/${legal_case_id}`, {
        withCredentials: true,
      });
      return res.data;
    },
    enabled: !!legal_case_id && !loadingAuth,
    staleTime: 1000 * 60, // 1 minute
  });

  // helpers to split calculations by logical type
  const filterByType = (list: any[], kind: "juridical" | "contencioso") => {
    if (!list) return [];
    return list.filter((c) => {
      const t = String(c.calculation_type || "").toLowerCase();
      if (kind === "juridical") {
        return t.includes("jurid") || t.includes("juríd") || t.includes("juridico");
      }
      // contencioso / contencioso spelling
      return t.includes("contenc") || t.includes("contencioso");
    });
  };

  const juridicalCalculations = filterByType(calculations, "juridical");
  const contenciosoCalculations = filterByType(calculations, "contencioso");

  if (loadingAuth || isLoading) {
    return (
      <SidebarProvider>
        <AppSidebar variant="inset" />
        <SidebarInset className="flex-1 min-w-0">
          <div style={{ marginLeft: "12rem" }}>
            <SiteHeader />
            <div className="p-8">Loading...</div>
          </div>
        </SidebarInset>
      </SidebarProvider>
    );
  }

  if (error) {
    return (
      <SidebarProvider>
        <AppSidebar variant="inset" />
        <SidebarInset className="flex-1 min-w-0">
          <div style={{ marginLeft: "12rem" }}>
            <SiteHeader />
            <div className="p-8 text-red-600">Failed to load legal case.</div>
          </div>
        </SidebarInset>
      </SidebarProvider>
    );
  }

  // navigation target for create button (adjust route if your app has a different path)
  const handleCreateCalculation = (type: string) => {
    navigate({
      to: `/u/company/${company_id}/legal-cases/${legal_case_id}/calculations/new`,
      search: (old) => ({ ...(old || {}), type }),
    });
  };

  return (
    <SidebarProvider>
      <AppSidebar variant="inset" />
      <SidebarInset className="flex-1 min-w-0">
        <div style={{ marginLeft: "12rem" }}>
          <SiteHeader />
          <div className="flex flex-1 flex-col p-6 gap-6">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold">Processo</h2>
              <div className="flex gap-2">
                <Button variant="ghost" size="sm" onClick={() => navigate({ to: `/u/company/${company_id}/legal-cases` })}>
                  Voltar
                </Button>
                <Button size="sm" onClick={() => navigate({ to: `/u/company/${company_id}/legal-cases/${legal_case_id}/edit/` })}>
                  Editar
                </Button>
              </div>
            </div>

            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setActiveTab("legalCaseDetails")}
                aria-pressed={activeTab === "legalCaseDetails"}
                className={activeTab === "legalCaseDetails" ? "bg-muted text-muted-foreground" : ""}
              >
                DADOS DO CÁLCULO
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setActiveTab("contractDetails")}
                aria-pressed={activeTab === "contractDetails"}
                className={activeTab === "contractDetails" ? "bg-muted text-muted-foreground" : ""}
              >
                DADOS CONTRATO
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setActiveTab("juridicalCalculations")}
                aria-pressed={activeTab === "juridicalCalculations"}
                className={activeTab === "juridicalCalculations" ? "bg-muted text-muted-foreground" : ""}
              >
                CÁLCULOS JURÍDICO
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setActiveTab("complianceCalculations")}
                aria-pressed={activeTab === "complianceCalculations"}
                className={activeTab === "complianceCalculations" ? "bg-muted text-muted-foreground" : ""}
              >
                CÁLCULOS CONTENCIOSO
              </Button>
            </div>

            {activeTab === "legalCaseDetails" && (
              <>
                <section className="bg-white border rounded p-4">
                  <h3 className="text-sm font-medium mb-3">Dados do Processo</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="flex flex-col">
                      <div className="text-xs text-muted-foreground">Número do Processo</div>
                      <div className="text-base font-medium">{formatLegalCaseNumber(legalCase?.legal_case_number)}</div>
                    </div>

                    <div className="flex flex-col col-span-2">
                      <div className="text-xs text-muted-foreground">Clientes</div>
                      <div className="space-y-2 mt-1">
                        {(legalCase?.clients || []).length === 0 && <div className="text-sm text-muted-foreground">Nenhum cliente</div>}
                        {(legalCase?.clients || []).map((c: any, i: number) => (
                          <div key={i} className="flex items-center gap-4">
                            <div className="text-sm font-medium">{formatValue(c.name)}</div>
                            <div className="text-sm text-muted-foreground">{formatValue(c.cpf)}</div>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="flex flex-col">
                      <div className="text-xs text-muted-foreground">Status</div>
                      <div className="text-base">{formatValue(legalCase?.status)}</div>
                    </div>
                  </div>
                </section>

                <section className="bg-white border rounded p-4">
                  <h3 className="text-sm font-medium mb-3">Datas do Processo</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <div className="text-xs text-muted-foreground">Ajustamento</div>
                      <div>{formatValue(legalCase?.date_ajustamento)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground">Trânsito em Julgado</div>
                      <div>{formatValue(legalCase?.date_transito)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground">Citação</div>
                      <div>{formatValue(legalCase?.date_citacao)}</div>
                    </div>

                    <div>
                      <div className="text-xs text-muted-foreground">Evento Danoso</div>
                      <div>{formatValue(legalCase?.date_evento_danoso)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground">Sentença</div>
                      <div>{formatValue(legalCase?.date_sentenca)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground">Acordo</div>
                      <div>{formatValue(legalCase?.date_acordo)}</div>
                    </div>
                  </div>
                </section>

                <section className="bg-white border rounded p-4">
                  <h3 className="text-sm font-medium mb-3">Valores e Honorários</h3>
                  <div className="grid grid-cols-4 gap-4">
                    <div>
                      <div className="text-xs text-muted-foreground">Valor da Causa</div>
                      <div>{formatValue(legalCase?.case_value)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground">Honorários Sucumbenciais</div>
                      <div>{formatValue(legalCase?.percentage_court_awarded_attorney_fees)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground">Honorários Contratuais</div>
                      <div>{formatValue(legalCase?.percentage_contractual_attorney_fees)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground">Valor Honorários</div>
                      <div>{formatValue(legalCase?.attorney_fees_value)}</div>
                    </div>
                  </div>
                </section>

                <section className="bg-white border rounded p-4">
                  <h3 className="text-sm font-medium mb-3">Outros</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <div className="text-xs text-muted-foreground">Réu</div>
                      <div>{formatValue(legalCase?.defendant)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground">Advogado</div>
                      <div>{formatValue(legalCase?.attorney)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground">Assignee Comercial (ID)</div>
                      <div>{formatValue(legalCase?.assignee_from_commercial_team_id)}</div>
                    </div>
                  </div>
                </section>
              </>
            )}

            {activeTab === "juridicalCalculations" && (
              <CalculationsTable
                title="Cálculos Jurídico"
                companyId={company_id}
                legalCaseId={legal_case_id}
                calculations={juridicalCalculations}
                loading={loadingCalculations}
                onCreate={() => handleCreateCalculation("juridical")}
              />
            )}

            {activeTab === "complianceCalculations" && (
              <CalculationsTable
                title="Cálculos Contencioso"
                companyId={company_id}
                legalCaseId={legal_case_id}
                calculations={contenciosoCalculations}
                loading={loadingCalculations}
                onCreate={() => handleCreateCalculation("contencioso")}
              />
            )}
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}