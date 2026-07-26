import { Plus } from "lucide-react";
import { useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { DataTable } from "../../../components/table/DataTable.jsx";
import { Tabs } from "../../../components/tabs/Tabs.jsx";
import { PageHeader } from "../../../layouts/PageHeader.jsx";
import { PolicyFormModal } from "../components/PolicyFormModal.jsx";
import { useGovernanceResources } from "../hooks/useGovernanceResources.js";

const tabs = [
  { id: "policies", label: "OPA Policies" },
  { id: "risk", label: "NIST RMF Risk" },
  { id: "audit", label: "Audit & Observability" }
];

export function GovernanceManagementPage() {
  const { policies, settings, createPolicy } = useGovernanceResources();
  const [active, setActive] = useState("policies");
  const [policyModalOpen, setPolicyModalOpen] = useState(false);

  function submitPolicy(payload, setError) {
    createPolicy.mutate(payload, {
      onSuccess: () => setPolicyModalOpen(false),
      onError: (error) => setError(formatApiError(error))
    });
  }

  return (
    <div>
      <PageHeader
        title="Governance Management"
        description="SentinelAI v2 centralizes policy in OPA, risk in NIST RMF assessment, and observability in Splunk-compatible audit events."
      />
      <Card>
        <CardHeader title="Governance Controls" />
        <CardBody>
          <Tabs tabs={tabs} active={active} onChange={setActive} />
          <div className="mt-5">
            {active === "policies" ? <OpaPolicies policies={policies} onAdd={() => setPolicyModalOpen(true)} /> : null}
            {active === "risk" ? <RiskConfiguration /> : null}
            {active === "audit" ? <AuditConfiguration settings={settings.data} /> : null}
          </div>
        </CardBody>
      </Card>
      <PolicyFormModal open={policyModalOpen} onClose={() => setPolicyModalOpen(false)} onSubmit={submitPolicy} pending={createPolicy.isPending} />
    </div>
  );
}

function formatApiError(error) {
  const detail = error.response?.data?.detail;
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg).join(", ");
  }
  return detail || "Unable to add policy";
}

function OpaPolicies({ policies, onAdd }) {
  const columns = [
    { key: "policy_id", header: "Policy ID" },
    { key: "name", header: "Policy" },
    { key: "package", header: "Package" },
    { key: "engine", header: "Engine" },
    { key: "status", header: "Status", render: (row) => <StatusBadge status={row.status} /> },
    { key: "rules", header: "Rules", render: (row) => row.rules?.length || 0 }
  ];
  return (
    <div>
      <div className="mb-4 flex items-center justify-between gap-3">
        <div>
          <h2 className="text-sm font-semibold text-ink">OPA Policy Bundle</h2>
          <p className="text-sm text-slate-500">Add Rego policies that OPA evaluates during governance execution.</p>
        </div>
        <Button onClick={onAdd}>
          <Plus className="h-4 w-4" />
          Add Policy
        </Button>
      </div>
      <DataTable columns={columns} rows={policies.data || []} loading={policies.isLoading} empty="No Rego policies found" />
    </div>
  );
}

function RiskConfiguration() {
  const rows = [
    { id: "categorize", phase: "Categorize", owner: "Risk Engine", signal: "API sensitivity, operation, transaction amount", output: "System category" },
    { id: "assess", phase: "Assess", owner: "Risk Engine", signal: "Trust score, anomaly score, previous violations, customer sensitivity", output: "Risk score 0-100" },
    { id: "authorize", phase: "Authorize", owner: "OPA + Human Approval", signal: "Risk level and Rego policy result", output: "Allow, deny, or require approval" },
    { id: "monitor", phase: "Monitor", owner: "Splunk Audit", signal: "Structured stage events", output: "Operational telemetry" }
  ];
  return (
    <DataTable
      columns={[
        { key: "phase", header: "RMF Phase" },
        { key: "owner", header: "Owner" },
        { key: "signal", header: "Signals" },
        { key: "output", header: "Output" }
      ]}
      rows={rows}
    />
  );
}

function AuditConfiguration({ settings }) {
  const rows = [
    { id: "sink", setting: "Audit Sink", value: settings?.audit_sink || "sqlite-splunk" },
    { id: "opa", setting: "OPA URL", value: settings?.opa_url || "http://localhost:8181" },
    { id: "decision", setting: "OPA Decision Path", value: settings?.opa_decision_path || "/v1/data/sentinelai/governance/decision" },
    { id: "bundle", setting: "Policy Bundle Path", value: settings?.opa_policy_bundle_path || "./app/policies/rego" }
  ];
  return (
    <DataTable
      columns={[
        { key: "setting", header: "Setting" },
        { key: "value", header: "Value" }
      ]}
      rows={rows}
    />
  );
}
