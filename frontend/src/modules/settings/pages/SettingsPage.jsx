import { useQuery } from "@tanstack/react-query";
import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { PageHeader } from "../../../layouts/PageHeader.jsx";
import { settingsService } from "../services/settingsService.js";

export function SettingsPage() {
  const settings = useQuery({ queryKey: ["settings"], queryFn: settingsService.read });
  const health = useQuery({ queryKey: ["health"], queryFn: settingsService.health, refetchInterval: 15000 });

  return (
    <div>
      <PageHeader
        title="Settings"
        description="Runtime configuration, environment state, adapter registry, and backend health for the prototype deployment."
      />
      <div className="grid gap-5 xl:grid-cols-[0.8fr_1.2fr]">
        <Card>
          <CardHeader title="Backend Health" action={<StatusBadge status={health.data?.status || "PENDING"} />} />
          <CardBody>
            <pre className="rounded-md bg-slate-950 p-4 text-xs text-slate-100">{JSON.stringify(health.data || {}, null, 2)}</pre>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Environment Configuration" />
          <CardBody>
            <div className="grid gap-3 text-sm md:grid-cols-2">
              {Object.entries(settings.data || {}).map(([key, value]) => (
                <div key={key} className="rounded-md border border-line p-3">
                  <div className="text-xs font-semibold uppercase text-slate-400">{key.replaceAll("_", " ")}</div>
                  <div className="mt-2 break-words font-medium text-ink">{Array.isArray(value) ? value.join(", ") : String(value)}</div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
