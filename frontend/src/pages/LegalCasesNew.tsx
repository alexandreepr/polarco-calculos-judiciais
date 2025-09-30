import { AppSidebar } from "@/components/layout/AppSidebar/AppSidebar"
import { SiteHeader } from "@/components/layout/Header/Header"
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"

import { CreateLegalCaseForm } from "@/components/forms/CreateLegalCaseForm"

export function LegalCasesNew() {

  return (
    <SidebarProvider>
      <AppSidebar variant="inset"/>
      <SidebarInset className="flex-1 min-w-0">
        <div style={{ marginLeft: '12rem'}}>
        <SiteHeader />
        <div className="flex flex-1 flex-col">
            <CreateLegalCaseForm />
        </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}