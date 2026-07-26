import { Link } from "react-router-dom";
import { Button } from "../../../components/button/Button.jsx";
import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { DataTable } from "../../../components/table/DataTable.jsx";
import { PageHeader } from "../../../layouts/PageHeader.jsx";
import { formatDate } from "../../../utils/format.js";
import { KpiCard } from "../components/KpiCard.jsx";
import { useDashboard } from "../hooks/useDashboard.js";

export function DashboardPage() {
  const { data, isLoading, error } = useDashboard();
  const executionColumns = [
    { key: "request_id", header: "Request" },
    { key: "service", header: "Service" },
    { key: "operation", header: "Operation" },
    { key: "decision", header: "Decision", render: (row) => <StatusBadge status={row.decision} /> },
    { key: "status", header: "Status", render: (row) => <StatusBadge status={row.status} /> },
    { key: "created_at", header: "Created", render: (row) => formatDate(row.created_at) }
  ];
  const auditColumns = [
    { key: "stage", header: "Stage" },
    { key: "request_id", header: "Request" },
    { key: "decision", header: "Decision", render: (row) => <StatusBadge status={row.decision} /> },
    { key: "reason", header: "Reason" },
    { key: "timestamp", header: "Timestamp", render: (row) => formatDate(row.timestamp) }
  ];

  return (
    <div className="pb-10">
      <PageHeader
        title="Dashboard"
        description="High-level operational summary for SentinelAI governance runtime, policy deployment, approvals, and observability."
        action={
          <div className="flex flex-wrap gap-2">
            <Link to="/approvals">
              <Button tone="secondary">Human Approval</Button>
            </Link>
            <Link to="/simulation">
              <Button>Simulation Lab</Button>
            </Link>
          </div>
        }
      />
      {error ? (
        <Card>
          <CardBody>{error.message}</CardBody>
        </Card>
      ) : null}
      <div className="grid min-w-0 gap-4 md:grid-cols-2 xl:grid-cols-3">
        {(data?.kpis || Array.from({ length: 6 }, (_, index) => ({ label: "Loading", value: index ? "" : "..." }))).map((kpi, index) => (
          <KpiCard key={`${kpi.label}-${index}`} kpi={kpi} />
        ))}
      </div>
      <div className="mt-6 grid min-w-0 gap-4 xl:grid-cols-2">
        <Card className="flex h-[620px] flex-col">
          <CardHeader title="Recent Executions" />
          <CardBody className="min-h-0 flex-1 overflow-y-auto overflow-x-hidden pr-2">
            <DataTable columns={executionColumns} rows={data?.recent_executions || []} loading={isLoading} empty="No executions yet" />
          </CardBody>
        </Card>
        <Card className="flex h-[620px] flex-col">
          <CardHeader title="Recent Audit Events" />
          <CardBody className="min-h-0 flex-1 overflow-y-auto overflow-x-hidden pr-2">
            <DataTable columns={auditColumns} rows={data?.recent_audit_events || []} loading={isLoading} empty="No audit events yet" />
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
