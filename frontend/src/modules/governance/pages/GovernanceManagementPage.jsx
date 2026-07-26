import { Copy, Edit, Play, Plus, RotateCcw, ToggleLeft, ToggleRight, Trash2 } from "lucide-react";
import { useMemo, useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { DataTable } from "../../../components/table/DataTable.jsx";
import { Tabs } from "../../../components/tabs/Tabs.jsx";
import { PageHeader } from "../../../layouts/PageHeader.jsx";
import { formatDate } from "../../../utils/format.js";
import { BudgetPolicyFormModal } from "../components/BudgetPolicyFormModal.jsx";
import { GovernancePolicyFormModal } from "../components/GovernancePolicyFormModal.jsx";
import { useGovernanceResources } from "../hooks/useGovernanceResources.js";

const tabs = [
  { id: "governance", label: "Governance Policies" },
  { id: "budgets", label: "Budget Policies" },
  { id: "builder", label: "Policy Builder" },
  { id: "configuration", label: "Governance Configuration" },
  { id: "history", label: "Policy Version History" },
  { id: "deployment", label: "Deployment Status" }
];

export function GovernanceManagementPage() {
  const resources = useGovernanceResources();
  const [active, setActive] = useState("governance");
  const [governanceModal, setGovernanceModal] = useState(null);
  const [budgetModal, setBudgetModal] = useState(null);
  const [deployNotice, setDeployNotice] = useState("");
  const latestDeployment = resources.deploy.data || resources.deployment.data;

  function submitGovernancePolicy(payload, setError) {
    const mutation = governanceModal ? resources.updateGovernancePolicy.mutateAsync({ id: governanceModal.id, payload }) : resources.createGovernancePolicy.mutateAsync(payload);
    mutation.then(() => setGovernanceModal(null)).catch((error) => setError(apiError(error)));
  }

  function submitBudgetPolicy(payload, setError) {
    const mutation = budgetModal ? resources.updateBudgetPolicy.mutateAsync({ id: budgetModal.id, payload }) : resources.createBudgetPolicy.mutateAsync(payload);
    mutation.then(() => setBudgetModal(null)).catch((error) => setError(apiError(error)));
  }

  function deployPolicies() {
    setActive("deployment");
    setDeployNotice("");
    resources.deploy.reset();
    resources.deploy
      .mutateAsync()
      .then((deployment) => {
        setDeployNotice(deployment.status === "DEPLOYED" ? "Policies deployed successfully." : deployment.message || "Policy deployment completed.");
      })
      .catch((error) => setDeployNotice(apiError(error)));
  }

  return (
    <div className="flex h-full min-h-0 flex-col">
      <PageHeader
        title="Governance Management"
        description="Manage JSON-sourced governance and budget policies, generate one OPA governance bundle, and track deployment history."
        action={
          <Button onClick={deployPolicies} disabled={resources.deploy.isPending}>
            <Play className="h-4 w-4" />
            {resources.deploy.isPending ? "Deploying" : "Deploy Policies"}
          </Button>
        }
      />
      <Card className="flex min-h-0 flex-1 flex-col">
        <CardHeader title="Governance Controls" />
        <CardBody className="flex min-h-0 flex-1 flex-col">
          <Tabs tabs={tabs} active={active} onChange={setActive} />
          <div className="mt-5 min-h-0 flex-1 overflow-y-auto overflow-x-hidden pr-2">
            {active === "governance" ? <GovernancePolicies resources={resources} onCreate={() => setGovernanceModal(false)} onEdit={setGovernanceModal} /> : null}
            {active === "budgets" ? <BudgetPolicies resources={resources} onCreate={() => setBudgetModal(false)} onEdit={setBudgetModal} /> : null}
            {active === "builder" ? <PolicyBuilder onCreate={() => setGovernanceModal(false)} lookups={resources.lookups.data} /> : null}
            {active === "configuration" ? <GovernanceConfiguration settings={resources.settings.data} lookups={resources.lookups.data} /> : null}
            {active === "history" ? <PolicyHistory resources={resources} /> : null}
            {active === "deployment" ? <DeploymentStatus deployment={latestDeployment} onDeploy={deployPolicies} pending={resources.deploy.isPending} notice={deployNotice} error={resources.deploy.error ? apiError(resources.deploy.error) : ""} /> : null}
          </div>
        </CardBody>
      </Card>
      <GovernancePolicyFormModal
        open={governanceModal !== null}
        policy={governanceModal || null}
        lookups={resources.lookups.data}
        pending={resources.createGovernancePolicy.isPending || resources.updateGovernancePolicy.isPending}
        onClose={() => setGovernanceModal(null)}
        onSubmit={submitGovernancePolicy}
      />
      <BudgetPolicyFormModal
        open={budgetModal !== null}
        policy={budgetModal || null}
        lookups={resources.lookups.data}
        pending={resources.createBudgetPolicy.isPending || resources.updateBudgetPolicy.isPending}
        onClose={() => setBudgetModal(null)}
        onSubmit={submitBudgetPolicy}
      />
    </div>
  );
}

function GovernancePolicies({ resources, onCreate, onEdit }) {
  const columns = useMemo(
    () => [
      { key: "policy_id", header: "Policy ID" },
      { key: "name", header: "Name" },
      { key: "decision", header: "Decision", render: (row) => <StatusBadge status={row.decision} /> },
      { key: "priority", header: "Priority" },
      { key: "enabled", header: "Enabled", render: (row) => <StatusBadge status={row.enabled ? "ACTIVE" : "INACTIVE"} /> },
      { key: "conditions", header: "Conditions", render: (row) => row.conditions?.length || 0 },
      {
        key: "actions",
        header: "Actions",
        render: (row) => (
          <ActionGroup>
            <IconAction label="Edit" icon={Edit} onClick={() => onEdit(row)} />
            <IconAction label="Duplicate" icon={Copy} onClick={() => resources.duplicateGovernancePolicy.mutate(row.id)} />
            <IconAction label={row.enabled ? "Disable" : "Enable"} icon={row.enabled ? ToggleLeft : ToggleRight} onClick={() => resources.setGovernancePolicyEnabled.mutate({ id: row.id, enabled: !row.enabled })} />
            <IconAction label="Delete" icon={Trash2} danger onClick={() => resources.deleteGovernancePolicy.mutate(row.id)} />
          </ActionGroup>
        )
      }
    ],
    [onEdit, resources]
  );
  return (
    <SectionHeader title="Governance Policies" description="Individual policy records compiled into the single OPA governance bundle." actionLabel="Create Policy" onAction={onCreate}>
      <DataTable columns={columns} rows={resources.governancePolicies.data || []} loading={resources.governancePolicies.isLoading} empty="No governance policies configured" />
    </SectionHeader>
  );
}

function BudgetPolicies({ resources, onCreate, onEdit }) {
  const columns = [
    { key: "name", header: "Name" },
    { key: "department", header: "Department" },
    { key: "daily_limit", header: "Daily Limit" },
    { key: "monthly_limit", header: "Monthly Limit" },
    { key: "transaction_limit", header: "Transaction Limit" },
    { key: "approval_threshold", header: "Approval Threshold" },
    { key: "spent_today", header: "Spent Today" },
    { key: "spent_month", header: "Spent Month" },
    { key: "status", header: "Status", render: (row) => <StatusBadge status={row.status} /> },
    {
      key: "actions",
      header: "Actions",
      render: (row) => (
        <ActionGroup>
          <IconAction label="Edit" icon={Edit} onClick={() => onEdit(row)} />
          <IconAction label="Duplicate" icon={Copy} onClick={() => resources.duplicateBudgetPolicy.mutate(row.id)} />
          <IconAction label={row.status === "ACTIVE" ? "Deactivate" : "Activate"} icon={row.status === "ACTIVE" ? ToggleLeft : ToggleRight} onClick={() => resources.setBudgetPolicyStatus.mutate({ id: row.id, active: row.status !== "ACTIVE" })} />
          <IconAction label="Delete" icon={Trash2} danger onClick={() => resources.deleteBudgetPolicy.mutate(row.id)} />
        </ActionGroup>
      )
    }
  ];
  return (
    <SectionHeader title="Budget Policies" description="Dedicated budget controls that compile into the shared governance.rego bundle." actionLabel="Create Budget Policy" onAction={onCreate}>
      <DataTable columns={columns} rows={resources.budgetPolicies.data || []} loading={resources.budgetPolicies.isLoading} empty="No budget policies configured" />
    </SectionHeader>
  );
}

function PolicyBuilder({ onCreate, lookups }) {
  return (
    <div className="grid min-w-0 gap-4 lg:grid-cols-[minmax(280px,0.8fr)_minmax(0,1.2fr)]">
      <Card>
        <CardHeader title="Visual Builder" />
        <CardBody className="space-y-3 text-sm text-slate-600">
          <p>Build policies from explicit fields, operators, decisions, priorities, enablement, and reason text. Rego is generated and validated by the backend.</p>
          <Button onClick={onCreate}>
            <Plus className="h-4 w-4" />
            Open Builder
          </Button>
        </CardBody>
      </Card>
      <Card>
        <CardHeader title="Available Condition Fields" />
        <CardBody>
          <div className="grid gap-2 sm:grid-cols-2">
            {(lookups?.condition_fields || []).map((field) => (
              <div key={field.value} className="min-w-0 rounded-md border border-line px-3 py-2 text-sm">
                <div className="font-semibold text-ink">{field.label}</div>
                <div className="break-words text-xs text-slate-500">{field.value}</div>
              </div>
            ))}
          </div>
        </CardBody>
      </Card>
    </div>
  );
}

function GovernanceConfiguration({ settings, lookups }) {
  const rows = [
    { id: "opa", setting: "OPA URL", value: settings?.opa_url },
    { id: "decision", setting: "OPA Decision Path", value: settings?.opa_decision_path },
    { id: "bundle", setting: "Policy Bundle Path", value: settings?.opa_policy_bundle_path },
    { id: "decisions", setting: "Policy Decisions", value: lookups?.decisions?.join(", ") },
    { id: "departments", setting: "Departments", value: lookups?.departments?.join(", ") }
  ];
  return <DataTable columns={[{ key: "setting", header: "Configuration" }, { key: "value", header: "Value" }]} rows={rows} />;
}

function PolicyHistory({ resources }) {
  const [left, setLeft] = useState("");
  const [right, setRight] = useState("");
  const [compare, setCompare] = useState(null);
  const versions = resources.history.data || [];
  function runCompare() {
    if (!left || !right) return;
    resources.compareVersions(left, right).then(setCompare);
  }
  const columns = [
    { key: "version_id", header: "Version" },
    { key: "resource_key", header: "Resource" },
    { key: "action", header: "Action" },
    { key: "created_at", header: "Created", render: (row) => formatDate(row.created_at) },
    { key: "restore", header: "Restore", render: (row) => <IconAction label="Restore" icon={RotateCcw} onClick={() => resources.restore.mutate(row.version_id)} /> }
  ];
  return (
    <div className="space-y-4">
      <div className="grid min-w-0 gap-3 rounded-md border border-line p-3 md:grid-cols-[minmax(0,1fr)_minmax(0,1fr)_auto]">
        <VersionSelect value={left} versions={versions} onChange={setLeft} />
        <VersionSelect value={right} versions={versions} onChange={setRight} />
        <Button onClick={runCompare}>Compare</Button>
      </div>
      {compare ? <div className="rounded-md border border-line bg-slate-50 px-3 py-2 text-sm text-slate-600">{compare.summary?.join(", ")}</div> : null}
      <DataTable columns={columns} rows={versions} loading={resources.history.isLoading} empty="No policy versions yet" />
    </div>
  );
}

function DeploymentStatus({ deployment, onDeploy, pending, notice, error }) {
  const rows = deployment
    ? [
        { id: "deployment", label: "Deployment", value: deployment.deployment_id },
        { id: "status", label: "Status", value: deployment.status },
        { id: "fmt", label: "opa fmt", value: deployment.opa_fmt_status },
        { id: "check", label: "opa check", value: deployment.opa_check_status },
        { id: "reload", label: "OPA Reload", value: deployment.opa_reload_status },
        { id: "created", label: "Created", value: formatDate(deployment.created_at) },
        { id: "message", label: "Message", value: deployment.message }
      ]
    : [];
  return (
    <SectionHeader title="Deployment Status" description="The backend generates governance.rego, validates it, then updates the watched OPA policy file." actionLabel={pending ? "Deploying" : "Deploy Now"} onAction={onDeploy} actionDisabled={pending}>
      {notice ? <div className={`mb-4 rounded-md px-3 py-2 text-sm ${error ? "border border-red-200 bg-red-50 text-danger" : "border border-emerald-200 bg-emerald-50 text-emerald-700"}`}>{notice}</div> : null}
      <DataTable columns={[{ key: "label", header: "Item" }, { key: "value", header: "Value" }]} rows={rows} empty="No deployment has been recorded" />
    </SectionHeader>
  );
}

function SectionHeader({ title, description, actionLabel, onAction, actionDisabled, children }) {
  return (
    <div>
      <div className="mb-4 flex min-w-0 flex-wrap items-center justify-between gap-3">
        <div className="min-w-0">
          <h2 className="text-sm font-semibold text-ink">{title}</h2>
          <p className="break-words text-sm text-slate-500">{description}</p>
        </div>
        {onAction ? (
          <Button onClick={onAction} disabled={actionDisabled}>
            <Plus className="h-4 w-4" />
            {actionLabel}
          </Button>
        ) : null}
      </div>
      {children}
    </div>
  );
}

function VersionSelect({ value, versions, onChange }) {
  return (
    <select className="rounded-md border border-line px-3 py-2 text-sm outline-none focus:border-brand" value={value} onChange={(event) => onChange(event.target.value)}>
      <option value="" disabled>Select version</option>
      {versions.map((version) => (
        <option key={version.version_id} value={version.version_id}>{version.version_id}</option>
      ))}
    </select>
  );
}

function ActionGroup({ children }) {
  return <div className="flex flex-wrap gap-1" onClick={(event) => event.stopPropagation()}>{children}</div>;
}

function IconAction({ icon: Icon, label, danger, ...props }) {
  return (
    <button title={label} className={`rounded-md p-1.5 ${danger ? "text-danger hover:bg-red-50" : "text-slate-500 hover:bg-slate-100 hover:text-ink"}`} {...props}>
      <Icon className="h-4 w-4" />
    </button>
  );
}

function apiError(error) {
  const detail = error?.response?.data?.detail;
  if (Array.isArray(detail)) return detail.map((item) => item.msg || JSON.stringify(item)).join(", ");
  if (detail && typeof detail === "string") return detail;
  if (detail) return JSON.stringify(detail);
  return error?.response?.data?.message || error?.message || "An unexpected error occurred";
}
