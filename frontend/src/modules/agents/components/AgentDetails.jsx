import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { formatDate } from "../../../utils/format.js";

export function AgentDetails({ agent }) {
  if (!agent) {
    return (
      <Card>
        <CardBody>
          <div className="text-sm text-slate-500">Select an agent to inspect passport, API access, OPA profile, and activity.</div>
        </CardBody>
      </Card>
    );
  }
  return (
    <Card>
      <CardHeader title={agent.name}>
        {agent.passport_id}
      </CardHeader>
      <CardBody className="max-h-[calc(100vh-12rem)] space-y-5 overflow-y-auto overflow-x-hidden">
        <div className="grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
          <Info label="Department" value={agent.department} />
          <Info label="Owner" value={agent.owner} />
          <Info label="Trust Score" value={agent.trust_score} />
          <Info label="Reputation" value={agent.reputation} />
          <Info label="Risk Tier" value={agent.risk_tier} />
          <div>
            <div className="text-xs font-semibold uppercase text-slate-400">Status</div>
            <StatusBadge status={agent.status} />
          </div>
          <Info label="OPA Budget Profile" value={agent.budget_profile} />
          <Info label="Last Activity" value={formatDate(agent.last_activity)} />
        </div>
        <Section title="Allowed APIs" items={agent.allowed_apis} />
        <Section title="Allowed Operations" items={agent.allowed_operations} />
        <Section title="Policy Groups" items={agent.policy_groups} />
        <div className="rounded-md border border-line bg-slate-50 p-3 text-sm text-slate-600">
          Execution history is persisted through governance request and audit records, keyed by this Agent Passport.
        </div>
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

function Section({ title, items }) {
  return (
    <div className="min-w-0">
      <div className="mb-2 text-xs font-semibold uppercase text-slate-400">{title}</div>
      <div className="flex flex-wrap gap-2">
        {items?.map((item) => (
          <span key={item} className="max-w-full break-words rounded-md bg-slate-100 px-2 py-1 text-xs font-medium text-slate-600">
            {item}
          </span>
        ))}
      </div>
    </div>
  );
}
