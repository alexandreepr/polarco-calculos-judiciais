import { AppSidebar } from "@/components/layout/AppSidebar/AppSidebar"
import { ChartAreaInteractive } from "@/components/layout/ChartAreaInteractive/ChartAreaInteractive"
import { DataTable } from "@/components/layout/DataTable/DataTable"
import { DashboardSectionCards } from "@/components/layout/DashboardSectionCards/DashboardSectionCards"
import { SiteHeader } from "@/components/layout/Header/Header"
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"

import { useCompany } from "@/common/CompanyProvider"
import { useQuery } from "@tanstack/react-query"
import axios from "axios"

export function Dashboard() {
  const { currentCompany } = useCompany()

  const { data: cases, isLoading, error } = useQuery({
    queryKey: ["legal-cases", currentCompany?.id],
    queryFn: async () => {
      const url = currentCompany?.id
        ? `/api/v1/legal-cases/?company_id=${currentCompany.id}`
        : `/api/v1/legal-cases/`
      const res = await axios.get(url, { withCredentials: true })
      return res.data as any[]
    },
    enabled: true,
    staleTime: 1000 * 60,
  })

  const tableData = (cases ?? []).map((c: any, i: number) => ({
    id: i + 1,
    company_id: currentCompany?.id ?? "",
    legal_case_id: c.id,
    type: c.legal_case_number ?? "—",
    header:
      (Array.isArray(c.clients) && c.clients[0]?.name) ||
      c.defendant ||
      "—",
    status: c.status ?? "—",
    target: c.attorney ?? c.assignee_from_litigation_team_id ?? "—",
    reviewer: c.assignee_from_commercial_team_id ?? "Selecionar responsável",
    _rawId: c.id,
  }))

  return (
    <SidebarProvider>
      <AppSidebar variant="inset" />
      <SidebarInset className="flex-1 min-w-0">
        <div style={{ marginLeft: "12rem" }}>
          <SiteHeader />
          <div className="flex flex-1 flex-col">
            <div className="@container/main flex flex-1 flex-col gap-2">
              <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
                <DashboardSectionCards />
                <div className="px-4 lg:px-6">
                  <ChartAreaInteractive />
                </div>

                {isLoading ? (
                  <div className="p-4 text-sm text-muted-foreground">Carregando processos…</div>
                ) : error ? (
                  <div className="p-4 text-sm text-red-600">Erro ao carregar processos do backend.</div>
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