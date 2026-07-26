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
  const { data = [], isLoading, adapters, createApi, updateApi, activateApi, deactivateApi, deleteApi } = useEnterpriseApis();
  const governance = useGovernanceResources();
  const [selected, setSelected] = useState(null);
  const [editing, setEditing] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const columns = useMemo(
    () => [
      { key: "service_name", header: "Service" },
      { key: "adapter", header: "Adapter" },
      { key: "version", header: "Version" },
      { key: "status", header: "Status", render: (row) => <StatusBadge status={row.status} /> },
      { key: "supported_operations", header: "Supported Operations", render: (row) => row.supported_operations?.join(", ") },
      { key: "required_policies", header: "Policies", render: (row) => row.required_policies?.join(", ") },
      {
        key: "actions",
        header: "Actions",
        render: (row) => (
          <div className="flex gap-1" onClick={(event) => event.stopPropagation()}>
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
    <div>
      <PageHeader
        title="Enterprise API Registry"
        description="Registered enterprise capabilities, adapter assignments, policy requirements, and service health posture."
        action={
          <Button onClick={openCreate}>
            <Plus className="h-4 w-4" />
            Register API
          </Button>
        }
      />
      <div className="grid min-w-0 gap-5 xl:grid-cols-[minmax(0,1fr)_minmax(320px,420px)]">
        <Card>
          <CardBody>
            <DataTable columns={columns} rows={data} loading={isLoading} empty="No enterprise APIs registered" onRowClick={setSelected} />
          </CardBody>
        </Card>
        <Card>
          <CardHeader title={detail?.service_name || "API Details"} />
          <CardBody className="max-h-[calc(100vh-12rem)] space-y-4 overflow-y-auto overflow-x-hidden">
            {detail ? (
              <>
                <div className="grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
                  <Info label="Adapter" value={detail.adapter} />
                  <Info label="Version" value={detail.version} />
                  <Info label="Status" value={<StatusBadge status={detail.status} />} />
                  <Info label="Operations" value={detail.supported_operations?.length || 0} />
                </div>
                <TagBlock title="Supported Operations" items={detail.supported_operations} />
                <TagBlock title="Required Policies" items={detail.required_policies} />
                <pre className="json-panel max-h-52 overflow-y-auto overflow-x-hidden rounded-md bg-slate-950 p-3 text-xs text-slate-100">{JSON.stringify(detail.endpoint_metadata, null, 2)}</pre>
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
        adapters={adapters.data ?? EMPTY_LOOKUP_LIST}
        policies={governance.governancePolicies.data ?? EMPTY_LOOKUP_LIST}
        versions={governance.lookups.data?.versions ?? EMPTY_LOOKUP_LIST}
        statuses={governance.lookups.data?.statuses ?? EMPTY_LOOKUP_LIST}
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
