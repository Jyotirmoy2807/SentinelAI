import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { formatDate } from "../../../utils/format.js";

export function AuditDetails({ detail }) {
  if (!detail) {
    return (
      <Card>
        <CardBody>
          <div className="text-sm text-slate-500">Select an audit record to inspect its governance trail.</div>
        </CardBody>
      </Card>
    );
  }
  return (
    <Card>
      <CardHeader title={detail.request_id} />
      <CardBody className="space-y-5">
        <div>
          <div className="mb-2 text-xs font-semibold uppercase text-slate-400">Audit Timeline</div>
          <div className="space-y-3">
            {detail.audit_logs?.map((log) => (
              <div key={log.id} className="rounded-md border border-line p-3">
                <div className="flex items-center justify-between gap-3">
                  <div className="text-sm font-semibold text-ink">{log.stage.replaceAll("_", " ")}</div>
                  <StatusBadge status={log.decision} />
                </div>
                <div className="mt-1 text-xs text-slate-500">{formatDate(log.timestamp)} | {log.agent} | {log.enterprise_api}</div>
                <p className="mt-2 text-sm text-slate-600">{log.reason}</p>
                <div className="mt-2 text-xs text-slate-500">Policy: {log.policy || "n/a"} | Risk: {log.risk_score}</div>
              </div>
            ))}
          </div>
        </div>
        <div>
          <div className="mb-2 text-xs font-semibold uppercase text-slate-400">Execution Summary</div>
          {detail.execution_logs?.length ? (
            detail.execution_logs.map((log) => (
              <pre key={log.id} className="mb-3 max-h-72 overflow-auto rounded-md bg-slate-950 p-3 text-xs text-slate-100">
                {JSON.stringify(log, null, 2)}
              </pre>
            ))
          ) : (
            <div className="rounded-md border border-line bg-slate-50 p-3 text-sm text-slate-500">No enterprise execution log for this request</div>
          )}
        </div>
      </CardBody>
    </Card>
  );
}
