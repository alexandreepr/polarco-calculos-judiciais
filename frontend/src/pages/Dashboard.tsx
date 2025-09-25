import { AppSidebar } from "@/components/layout/AppSidebar/AppSidebar"
import { ChartAreaInteractive } from "@/components/layout/ChartAreaInteractive/ChartAreaInteractive"
import { DataTable } from "@/components/layout/DataTable/DataTable"
import { DashboardSectionCards } from "@/components/layout/DashboardSectionCards/DashboardSectionCards"
import { SiteHeader } from "@/components/layout/Header/Header"
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"

import data from "./data.json"

export function Dashboard() {
  return (
    <SidebarProvider>
      <AppSidebar variant="inset"/>
      <SidebarInset className="flex-1 min-w-0">
        <div style={{ marginLeft: '12rem'}}>
        <SiteHeader />
        <div className="flex flex-1 flex-col">
          <div className="@container/main flex flex-1 flex-col gap-2">
            <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
              <DashboardSectionCards />
              <div className="px-4 lg:px-6">
                <ChartAreaInteractive />
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