import { CompanyProvider } from '@/common/CompanyProvider'
import { RequireAuth } from '@/common/RequireAuth'
import { createFileRoute } from '@tanstack/react-router'
import { LegalCasesNew } from '@/pages/LegalCasesNew'

export const Route = createFileRoute('/u/company/$company_id/legal-cases/new')({
  component: () => (
    <RequireAuth>
      <CompanyProvider>
        <LegalCasesNew />
      </CompanyProvider>
    </RequireAuth>
  ),
})