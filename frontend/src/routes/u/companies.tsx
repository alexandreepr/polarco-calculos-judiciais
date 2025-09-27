import { createFileRoute } from "@tanstack/react-router";
import { Companies } from "@/pages/Companies";

export const Route = createFileRoute("/u/companies")({
  component: () => (
      <Companies />
  ),
});