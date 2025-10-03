import { AppSidebar } from "@/components/layout/AppSidebar/AppSidebar"
import { DataTable } from "@/components/layout/DataTable/DataTable"
import { SiteHeader } from "@/components/layout/Header/Header"
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"

import data from "./data.json"
import { Button } from "@/components/ui/button"
import { useNavigate } from "@tanstack/react-router"
import { useCompany } from "@/common/CompanyProvider"

import { useQuery } from "@tanstack/react-query"
import axios from "axios"

export function LegalCases() {
  const navigate = useNavigate();
  const { currentCompany } = useCompany();

  const { data: cases, isLoading, error } = useQuery({
    queryKey: ["legal-cases", currentCompany?.id],
    queryFn: async () => {
      // request backend; include company_id to scope results if available
      const url = currentCompany?.id
        ? `/api/v1/legal-cases/?company_id=${currentCompany.id}`
        : `/api/v1/legal-cases/`
      const res = await axios.get(url, { withCredentials: true })
      return res.data as any[]
    },
    enabled: !!currentCompany?.id,
  })

  // map backend shape to DataTable schema
  if (!currentCompany?.id) {
    return (
      <SidebarProvider>
        <AppSidebar variant="inset" />
        <SidebarInset className="flex-1 min-w-0">
          <div style={{ marginLeft: "12rem" }}>
            <SiteHeader />
            <div className="p-4 text-sm text-muted-foreground">
              Loading...
            </div>
          </div>
        </SidebarInset>
      </SidebarProvider>
    );
  }

  const tableData = (cases ?? data).map((c: any, i: number) => ({
    id: i + 1,
    company_id: currentCompany!.id,
    legal_case_id: c.id,
    type: c.legal_case_number ?? "—",
    header:
      // prefer first client name, then defendant, then fallback
      (Array.isArray(c.clients) && c.clients[0]?.name) ||
      c.defendant ||
      "—",
    status: c.status ?? "—",
    // map to the columns used in DataTable
    target: c.attorney ?? c.assignee_from_litigation_team_id ?? "—",
    reviewer: c.assignee_from_commercial_team_id ?? "Selecionar responsável",
    _rawId: c.id,
  }))


  return (
    <SidebarProvider>
      <AppSidebar variant="inset"/>
      <SidebarInset className="flex-1 min-w-0">
        <div style={{ marginLeft: '12rem'}}>
        <SiteHeader />
        <div className="flex flex-1 flex-col">
          <div className="@container/main flex flex-1 flex-col gap-2">
            <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
              <div className="flex justify-end mr-2">
                <Button
                  variant="default"
                  size="sm"
                  onClick={() =>
                    navigate({
                      //TODO FIX
                      to: `/u/company/${currentCompany!.id}/legal-cases/new/`,
                    })
                  }
                >
                    + Criar Processo
                </Button>
              </div>

              {isLoading ? (
                <div className="p-4 text-sm text-muted-foreground">Carregando processos…</div>
              ) : error ? (
                <div className="p-4 text-sm text-red-600">Erro ao carregar processos</div>
              ) : (
                <DataTable data={tableData} />
              )}
            </div>
          </div>
        </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}