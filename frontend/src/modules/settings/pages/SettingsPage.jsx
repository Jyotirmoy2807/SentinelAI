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
        description="Runtime configuration, environment state, API registry execution, and backend health for the prototype deployment."
      />
      <div className="grid min-w-0 gap-5 xl:grid-cols-[minmax(280px,0.8fr)_minmax(0,1.2fr)]">
        <Card>
          <CardHeader title="Backend Health" action={<StatusBadge status={health.data?.status || "PENDING"} />} />
          <CardBody>
            <pre className="json-panel max-h-80 overflow-y-auto overflow-x-hidden rounded-md bg-slate-950 p-4 text-xs text-slate-100">{JSON.stringify(health.data || {}, null, 2)}</pre>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Environment Configuration" />
          <CardBody className="max-h-[calc(100vh-12rem)] overflow-y-auto overflow-x-hidden">
            <div className="grid gap-3 text-sm md:grid-cols-2">
              {Object.entries(settings.data || {}).map(([key, value]) => (
                <div key={key} className="min-w-0 rounded-md border border-line p-3">
                  <div className="text-xs font-semibold uppercase text-slate-400">{key.replaceAll("_", " ")}</div>
                  <div className="mt-2 break-words font-medium text-ink">{formatSettingValue(value)}</div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}

function formatSettingValue(value) {
  if (Array.isArray(value)) {
    if (value.every((item) => typeof item === "string")) return value.join(", ");
    return JSON.stringify(value);
  }
  if (value && typeof value === "object") return JSON.stringify(value);
  return String(value);
}
