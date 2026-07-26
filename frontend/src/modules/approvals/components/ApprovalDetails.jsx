import { Button } from "../../../components/button/Button.jsx";
import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { formatDate } from "../../../utils/format.js";

export function ApprovalDetails({ approval, comments, setComments, onApprove, onReject, response }) {
  if (!approval) {
    return (
      <Card>
        <CardBody>
          <div className="text-sm text-slate-500">No approval selected</div>
        </CardBody>
      </Card>
    );
  }
  return (
    <Card>
      <CardHeader title={approval.approval_id} action={<StatusBadge status={approval.status} />}>
        {approval.request_id}
      </CardHeader>
      <CardBody className="space-y-5">
        <div className="grid grid-cols-2 gap-3 text-sm">
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
          <textarea rows={4} className="mt-1 w-full rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={comments} onChange={(event) => setComments(event.target.value)} />
        </label>
        <div className="flex gap-2">
          <Button onClick={onApprove} disabled={approval.status !== "PENDING"}>
            Approve
          </Button>
          <Button tone="danger" onClick={onReject} disabled={approval.status !== "PENDING"}>
            Reject
          </Button>
        </div>
        {response ? (
          <pre className="max-h-72 overflow-auto rounded-md bg-slate-950 p-3 text-xs text-slate-100">{JSON.stringify(response, null, 2)}</pre>
        ) : null}
      </CardBody>
    </Card>
  );
}

function Info({ label, value }) {
  return (
    <div>
      <div className="text-xs font-semibold uppercase text-slate-400">{label}</div>
      <div className="mt-1 font-medium text-ink">{value}</div>
    </div>
  );
}
