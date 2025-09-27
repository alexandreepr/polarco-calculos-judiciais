import { createFileRoute } from "@tanstack/react-router";
import { CompanyProvider } from "@/common/CompanyProvider";
import { RequireAuth } from "@/common/RequireAuth";

export const Route = createFileRoute("/u/company/$company_id/_layout")({
  component: (props: { children?: React.ReactNode }) => (
    <RequireAuth>
      <CompanyProvider>
        {props.children}
      </CompanyProvider>
    </RequireAuth>
  ),
})