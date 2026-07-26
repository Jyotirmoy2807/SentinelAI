import { ArrowUpRight } from "lucide-react";
import { Card, CardBody } from "../../../components/card/Card.jsx";

const toneClass = {
  info: "text-brand bg-blue-50",
  success: "text-teal bg-emerald-50",
  warning: "text-amber bg-amber-50",
  danger: "text-danger bg-red-50"
};

export function KpiCard({ kpi }) {
  return (
    <Card>
      <CardBody>
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="text-sm font-medium text-slate-500">{kpi.label}</div>
            <div className="mt-3 text-2xl font-semibold text-ink">{kpi.value}</div>
          </div>
          <span className={`rounded-md p-2 ${toneClass[kpi.tone] || toneClass.info}`}>
            <ArrowUpRight className="h-4 w-4" />
          </span>
        </div>
        {kpi.change ? <div className="mt-3 text-xs text-slate-500">{kpi.change}</div> : null}
      </CardBody>
    </Card>
  );
}
