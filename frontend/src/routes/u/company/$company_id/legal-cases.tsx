import { CompanyProvider } from '@/common/CompanyProvider'
import { RequireAuth } from '@/common/RequireAuth'
import { LegalCases } from '@/pages/LegalCases'
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/u/company/$company_id/legal-cases')({
  component: () => (
    <RequireAuth>
      <CompanyProvider>
        <LegalCases />
      </CompanyProvider>
    </RequireAuth>
  ),
})

