import { Button } from "../../../components/button/Button.jsx";
import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { formatDate } from "../../../utils/format.js";

export function ApprovalDetails({ approval, comments, setComments, onApprove, onReject, response }) {
  if (!approval) {
    return (
      <Card className="flex min-h-0 flex-col">
        <CardBody className="min-h-0 flex-1 overflow-y-auto overflow-x-hidden">
          <div className="text-sm text-slate-500">No approval selected</div>
        </CardBody>
      </Card>
    );
  }
  return (
    <Card className="flex min-h-0 flex-col">
      <CardHeader title={approval.approval_id} action={<StatusBadge status={approval.status} />}>
        {approval.request_id}
      </CardHeader>
      <CardBody className="min-h-0 flex-1 space-y-5 overflow-y-auto overflow-x-hidden">
        <div className="grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
          <Info label="Agent" value={approval.agent_name} />
          <Info label="Passport" value={approval.passport_id} />
          <Info label="Service" value={approval.service} />
          <Info label="Operation" value={approval.operation} />
          <Info label="Risk Score" value={approval.risk_score} />
          <Info label="Amount" value={approval.amount} />
          <Info label="Approver" value={approval.approver} />
          <Info label="Submitted" value={formatDate(approval.created_at)} />
        </div>
        <div className="rounded-md border border-line bg-slate-50 p-3 text-sm text-slate-600">{approval.reason}</div>
        <label className="block text-sm font-medium text-slate-600">
          Comments
          <textarea rows={4} className="mt-1 w-full min-w-0 rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={comments} onChange={(event) => setComments(event.target.value)} />
        </label>
        <div className="flex flex-wrap gap-2">
          <Button onClick={onApprove} disabled={approval.status !== "PENDING"}>
            Approve
          </Button>
          <Button tone="danger" onClick={onReject} disabled={approval.status !== "PENDING"}>
            Reject
          </Button>
        </div>
        {response ? (
          <pre className="json-panel max-h-72 overflow-y-auto overflow-x-hidden rounded-md bg-slate-950 p-3 text-xs text-slate-100">{JSON.stringify(response, null, 2)}</pre>
        ) : null}
      </CardBody>
    </Card>
  );
}

function Info({ label, value }) {
  return (
    <div className="min-w-0">
      <div className="text-xs font-semibold uppercase text-slate-400">{label}</div>
      <div className="mt-1 break-words font-medium text-ink">{value}</div>
    </div>
  );
}
