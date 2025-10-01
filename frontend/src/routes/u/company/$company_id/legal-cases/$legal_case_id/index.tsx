import { CompanyProvider } from '@/common/CompanyProvider'
import { RequireAuth } from '@/common/RequireAuth'
import { LegalCasesView } from '@/pages/LegalCaseView'
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute(
  '/u/company/$company_id/legal-cases/$legal_case_id/'
)({
  component: () => (
    <RequireAuth>
      <CompanyProvider>
        <LegalCasesView />
      </CompanyProvider>
    </RequireAuth>
  ),
})

export const legalCaseRoute = Route