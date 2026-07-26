import { CheckCircle, Edit, PauseCircle, Plus, Trash2 } from "lucide-react";
import { useMemo, useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { DataTable } from "../../../components/table/DataTable.jsx";
import { PageHeader } from "../../../layouts/PageHeader.jsx";
import { EnterpriseFormModal } from "../components/EnterpriseFormModal.jsx";
import { useEnterpriseApis } from "../hooks/useEnterpriseApis.js";
import { useGovernanceResources } from "../../governance/hooks/useGovernanceResources.js";

const EMPTY_LOOKUP_LIST = [];

export function EnterpriseRegistryPage() {
  const { data = [], isLoading, lookups, createApi, updateApi, activateApi, deactivateApi, deleteApi } = useEnterpriseApis();
  const governance = useGovernanceResources();
  const [selected, setSelected] = useState(null);
  const [editing, setEditing] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const columns = useMemo(
    () => [
      { key: "service_name", header: "Service" },
      { key: "operation", header: "Operation" },
      { key: "method", header: "Method" },
      { key: "version", header: "Version" },
      { key: "status", header: "Status", render: (row) => <StatusBadge status={row.status} /> },
      { key: "authentication_type", header: "Auth" },
      { key: "required_policies", header: "Policies", render: (row) => row.required_policies?.join(", ") },
      {
        key: "actions",
        header: "Actions",
        width: "150px",
        headerClassName: "text-right pr-6",
        cellClassName: "pr-6",
        render: (row) => (
          <div className="flex min-w-[124px] justify-end gap-1" onClick={(event) => event.stopPropagation()}>
            <IconButton label="Edit" icon={Edit} onClick={() => openEdit(row)} />
            <IconButton label="Activate" icon={CheckCircle} onClick={() => activateApi.mutate(row.id)} />
            <IconButton label="Deactivate" icon={PauseCircle} onClick={() => deactivateApi.mutate(row.id)} />
            <IconButton label="Delete" icon={Trash2} danger onClick={() => deleteApi.mutate(row.id)} />
          </div>
        )
      }
    ],
    [activateApi, deactivateApi, deleteApi]
  );

  function openCreate() {
    setEditing(null);
    setModalOpen(true);
  }

  function openEdit(api) {
    setEditing(api);
    setModalOpen(true);
  }

  function submit(payload) {
    const action = editing ? updateApi.mutateAsync({ id: editing.id, payload }) : createApi.mutateAsync(payload);
    action.then(() => {
      setModalOpen(false);
      setEditing(null);
    });
  }

  const detail = selected || data[0];

  return (
    <div className="flex h-full min-h-0 flex-col">
      <PageHeader
        title="Enterprise API Registry"
        description="Registered enterprise service operations, endpoint contracts, policy requirements, and service health posture."
        action={
          <Button onClick={openCreate}>
            <Plus className="h-4 w-4" />
            Register API
          </Button>
        }
      />
      <div className="grid min-h-0 min-w-0 flex-1 gap-5 overflow-y-auto overflow-x-hidden xl:grid-cols-[minmax(0,1fr)_minmax(320px,420px)] xl:overflow-hidden">
        <Card className="flex min-h-0 flex-col">
          <CardBody className="min-h-0 flex-1 overflow-y-auto overflow-x-hidden pr-3">
            <DataTable columns={columns} rows={data} loading={isLoading} empty="No enterprise APIs registered" onRowClick={setSelected} />
          </CardBody>
        </Card>
        <Card className="flex min-h-0 flex-col">
          <CardHeader title={detail?.service_name || "API Details"} />
          <CardBody className="min-h-0 flex-1 space-y-4 overflow-y-auto overflow-x-hidden">
            {detail ? (
              <>
                <div className="grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
                  <Info label="Operation" value={detail.operation} />
                  <Info label="Method" value={detail.method} />
                  <Info label="Version" value={detail.version} />
                  <Info label="Status" value={<StatusBadge status={detail.status} />} />
                  <Info label="Auth" value={detail.authentication_type} />
                  <Info label="Timeout" value={`${detail.timeout_seconds || 0}s`} />
                  <Info label="Retries" value={detail.retry_count ?? 0} />
                </div>
                <div className="rounded-md border border-line bg-slate-50 p-3 text-sm">
                  <div className="text-xs font-semibold uppercase text-slate-400">Endpoint</div>
                  <div className="mt-1 break-words font-medium text-ink">{detail.base_url}{detail.path}</div>
                </div>
                <TagBlock title="Required Policies" items={detail.required_policies} />
                <pre className="json-panel max-h-44 overflow-y-auto overflow-x-hidden rounded-md bg-slate-950 p-3 text-xs text-slate-100">{JSON.stringify({ authentication_config: detail.authentication_config, endpoint_metadata: detail.endpoint_metadata }, null, 2)}</pre>
              </>
            ) : (
              <div className="text-sm text-slate-500">No service selected</div>
            )}
          </CardBody>
        </Card>
      </div>
      <EnterpriseFormModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        item={editing}
        onSubmit={submit}
        lookups={lookups.data ?? {}}
        policies={governance.governancePolicies.data ?? EMPTY_LOOKUP_LIST}
        versions={governance.lookups.data?.versions ?? EMPTY_LOOKUP_LIST}
        statuses={lookups.data?.statuses ?? governance.lookups.data?.statuses ?? EMPTY_LOOKUP_LIST}
      />
    </div>
  );
}

function IconButton({ icon: Icon, label, danger, ...props }) {
  return (
    <button title={label} className={`rounded-md p-1.5 ${danger ? "text-danger hover:bg-red-50" : "text-slate-500 hover:bg-slate-100 hover:text-ink"}`} {...props}>
      <Icon className="h-4 w-4" />
    </button>
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

function TagBlock({ title, items }) {
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
