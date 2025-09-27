import { createFileRoute } from "@tanstack/react-router";
import { RequireAuth } from "@/common/RequireAuth";

export const Route = createFileRoute("/u/_layout")({
  component: (props: { children?: React.ReactNode }) => (
    <RequireAuth>
      {props.children}
    </RequireAuth>
  ),
});