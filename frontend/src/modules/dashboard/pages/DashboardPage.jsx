import { Link } from "react-router-dom";
import { Button } from "../../../components/button/Button.jsx";
import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { ApprovalTrendChart, DistributionChart, RequestTrendChart } from "../../../components/charts/MetricCharts.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { PageHeader } from "../../../layouts/PageHeader.jsx";
import { formatDate } from "../../../utils/format.js";
import { KpiCard } from "../components/KpiCard.jsx";
import { useDashboard } from "../hooks/useDashboard.js";

export function DashboardPage() {
  const { data, isLoading, error } = useDashboard();

  return (
    <div>
      <PageHeader
        title="Dashboard"
        description="Operational view of governed autonomous agent activity, pending reviews, enterprise execution health, and risk movement."
        action={
          <div className="flex gap-2">
            <Link to="/approvals">
              <Button tone="secondary">Pending Approvals</Button>
            </Link>
            <Link to="/simulation">
              <Button>Launch Simulation</Button>
            </Link>
          </div>
        }
      />
      {error ? <Card><CardBody>{error.message}</CardBody></Card> : null}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        {(data?.kpis || Array.from({ length: 10 }, (_, index) => ({ label: "Loading", value: index ? "" : "..." }))).map((kpi, index) => (
          <KpiCard key={`${kpi.label}-${index}`} kpi={kpi} />
        ))}
      </div>
      <div className="mt-6 grid gap-4 xl:grid-cols-3">
        <Card className="xl:col-span-2">
          <CardHeader title="Governance Requests Over Time" />
          <CardBody>
            <RequestTrendChart data={data?.request_trend || []} />
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Risk Distribution" />
          <CardBody>
            <DistributionChart data={data?.risk_distribution || []} />
          </CardBody>
        </Card>
      </div>
      <div className="mt-6 grid gap-4 xl:grid-cols-[0.9fr_1.1fr]">
        <Card>
          <CardHeader title="Approval Trend" />
          <CardBody>
            <ApprovalTrendChart data={data?.approval_trend || []} />
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Recent Activity" />
          <CardBody>
            <div className="space-y-3">
              {isLoading ? (
                <div className="text-sm text-slate-500">Loading activity</div>
              ) : (
                data?.recent_activity?.map((item) => (
                  <div key={`${item.timestamp}-${item.description}`} className="flex items-center justify-between gap-4 rounded-md border border-line p-3">
                    <div>
                      <div className="text-sm font-semibold text-ink">{item.title}</div>
                      <div className="text-xs text-slate-500">{item.description}</div>
                    </div>
                    <div className="text-right">
                      <StatusBadge status={item.status} />
                      <div className="mt-1 text-xs text-slate-400">{formatDate(item.timestamp)}</div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
