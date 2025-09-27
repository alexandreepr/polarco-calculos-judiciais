import { createFileRoute } from "@tanstack/react-router";
import { Dashboard } from "@/pages/Dashboard";
import { RequireAuth } from "@/common/RequireAuth";
import { CompanyProvider } from "@/common/CompanyProvider";

export const Route = createFileRoute("/u/company/$company_id/dashboard")({
  component: () => (
    <RequireAuth>
      <CompanyProvider>
        <Dashboard />
      </CompanyProvider>
    </RequireAuth>
  ),
});