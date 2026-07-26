import { Edit, Plus, Trash2 } from "lucide-react";
import { useMemo, useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { DataTable } from "../../../components/table/DataTable.jsx";
import { Tabs } from "../../../components/tabs/Tabs.jsx";
import { PageHeader } from "../../../layouts/PageHeader.jsx";
import { ResourceFormModal } from "../components/ResourceFormModal.jsx";
import { useGovernanceResources } from "../hooks/useGovernanceResources.js";

const tabs = [
  { id: "policies", label: "Policies" },
  { id: "firewall", label: "Firewall Rules" },
  { id: "compliance", label: "Compliance Rules" },
  { id: "budget", label: "Budget Rules" },
  { id: "risk", label: "Risk Configuration" }
];

export function GovernanceManagementPage() {
  const resources = useGovernanceResources();
  const [active, setActive] = useState("policies");
  const [editing, setEditing] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const query = resources[active];
  const rows = active === "risk" ? riskRows : query?.data || [];
  const columns = useMemo(() => columnsFor(active, openEdit, resources.deleteResource), [active, resources.deleteResource]);

  function openCreate() {
    setEditing(null);
    setModalOpen(true);
  }

  function openEdit(item) {
    setEditing(item);
    setModalOpen(true);
  }

  function submit(payload) {
    const action = editing
      ? resources.updateResource.mutateAsync({ kind: active, id: editing.id, payload })
      : resources.createResource.mutateAsync({ kind: active, payload });
    action.then(() => {
      setModalOpen(false);
      setEditing(null);
    });
  }

  return (
    <div>
      <PageHeader
        title="Governance Management"
        description="Configuration-driven policy, firewall, compliance, risk, and budget controls for the governance graph."
        action={
          active !== "risk" ? (
            <Button onClick={openCreate}>
              <Plus className="h-4 w-4" />
              Create
            </Button>
          ) : null
        }
      />
      <Card>
        <CardHeader title="Governance Controls" />
        <CardBody>
          <Tabs tabs={tabs} active={active} onChange={setActive} />
          <div className="mt-5">
            <DataTable columns={columns} rows={rows} loading={query?.isLoading} empty="No governance configuration found" />
          </div>
        </CardBody>
      </Card>
      {active !== "risk" ? (
        <ResourceFormModal kind={active} open={modalOpen} item={editing} onClose={() => setModalOpen(false)} onSubmit={submit} />
      ) : null}
    </div>
  );
}

function columnsFor(kind, openEdit, deleteResource) {
  const actionColumn = {
    key: "actions",
    header: "Actions",
    render: (row) => (
      <div className="flex gap-1">
        <button title="Edit" className="rounded-md p-1.5 text-slate-500 hover:bg-slate-100 hover:text-ink" onClick={() => openEdit(row)}>
          <Edit className="h-4 w-4" />
        </button>
        <button title="Delete" className="rounded-md p-1.5 text-danger hover:bg-red-50" onClick={() => deleteResource.mutate({ kind, id: row.id })}>
          <Trash2 className="h-4 w-4" />
        </button>
      </div>
    )
  };
  if (kind === "policies") {
    return [
      { key: "policy_id", header: "Policy ID" },
      { key: "name", header: "Policy" },
      { key: "priority", header: "Priority" },
      { key: "status", header: "Status", render: (row) => <StatusBadge status={row.status} /> },
      { key: "version", header: "Version" },
      { key: "department", header: "Department" },
      actionColumn
    ];
  }
  if (kind === "firewall") {
    return [
      { key: "rule_id", header: "Rule ID" },
      { key: "name", header: "Rule" },
      { key: "category", header: "Category" },
      { key: "severity", header: "Severity" },
      { key: "status", header: "Status", render: (row) => <StatusBadge status={row.status} /> },
      actionColumn
    ];
  }
  if (kind === "compliance") {
    return [
      { key: "rule_id", header: "Rule ID" },
      { key: "name", header: "Rule" },
      { key: "framework", header: "Framework" },
      { key: "version", header: "Version" },
      { key: "status", header: "Status", render: (row) => <StatusBadge status={row.status} /> },
      actionColumn
    ];
  }
  if (kind === "budget") {
    return [
      { key: "name", header: "Profile" },
      { key: "department", header: "Department" },
      { key: "daily_limit", header: "Daily Limit" },
      { key: "transaction_limit", header: "Transaction Limit" },
      { key: "approval_threshold", header: "Approval Threshold" },
      { key: "status", header: "Status", render: (row) => <StatusBadge status={row.status} /> },
      actionColumn
    ];
  }
  return [
    { key: "name", header: "Configuration" },
    { key: "value", header: "Value" },
    { key: "impact", header: "Impact" },
    { key: "status", header: "Status", render: (row) => <StatusBadge status={row.status} /> }
  ];
}

const riskRows = [
  { id: "risk-1", name: "High Amount Threshold", value: "2000", impact: "Adds financial exposure weight", status: "ACTIVE" },
  { id: "risk-2", name: "Trust Score Weight", value: "15", impact: "Raises risk for low-trust agents", status: "ACTIVE" },
  { id: "risk-3", name: "Critical Operation Weight", value: "14", impact: "Raises risk for refund, payment, delete", status: "ACTIVE" }
];
