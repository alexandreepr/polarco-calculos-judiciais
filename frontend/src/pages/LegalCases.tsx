import { AppSidebar } from "@/components/layout/AppSidebar/AppSidebar"
import { DataTable } from "@/components/layout/DataTable/DataTable"
import { SiteHeader } from "@/components/layout/Header/Header"
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"

import data from "./data.json"
import { Button } from "@/components/ui/button"
import { useNavigate } from "@tanstack/react-router"
import { useCompany } from "@/common/CompanyProvider"

export function LegalCases() {
  const navigate = useNavigate();
  const { currentCompany } = useCompany();

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
                <Button variant="default" size="sm" onClick={() => navigate({ to: `/u/company/${currentCompany?.id}/legal-cases/new` })}>
                    + Criar Processo
                </Button>
              </div>
              <DataTable data={data} />
            </div>
          </div>
        </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}