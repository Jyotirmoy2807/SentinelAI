import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { DataTable } from "../../../components/table/DataTable.jsx";
import { Tabs } from "../../../components/tabs/Tabs.jsx";
import { PageHeader } from "../../../layouts/PageHeader.jsx";
import { useGovernanceResources } from "../hooks/useGovernanceResources.js";
import { useState } from "react";

const tabs = [
  { id: "policies", label: "OPA Policies" },
  { id: "risk", label: "NIST RMF Risk" },
  { id: "audit", label: "Audit & Observability" }
];

export function GovernanceManagementPage() {
  const { policies, settings } = useGovernanceResources();
  const [active, setActive] = useState("policies");

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
            {active === "policies" ? <OpaPolicies policies={policies} /> : null}
            {active === "risk" ? <RiskConfiguration /> : null}
            {active === "audit" ? <AuditConfiguration settings={settings.data} /> : null}
          </div>
        </CardBody>
      </Card>
    </div>
  );
}

function OpaPolicies({ policies }) {
  const columns = [
    { key: "policy_id", header: "Policy ID" },
    { key: "name", header: "Policy" },
    { key: "package", header: "Package" },
    { key: "engine", header: "Engine" },
    { key: "status", header: "Status", render: (row) => <StatusBadge status={row.status} /> },
    { key: "rules", header: "Rules", render: (row) => row.rules?.length || 0 }
  ];
  return <DataTable columns={columns} rows={policies.data || []} loading={policies.isLoading} empty="No Rego policies found" />;
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
