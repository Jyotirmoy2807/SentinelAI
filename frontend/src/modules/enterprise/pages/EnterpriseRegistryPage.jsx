import { CheckCircle, Edit, PauseCircle, Plus, Trash2 } from "lucide-react";
import { useMemo, useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { DataTable } from "../../../components/table/DataTable.jsx";
import { PageHeader } from "../../../layouts/PageHeader.jsx";
import { EnterpriseFormModal } from "../components/EnterpriseFormModal.jsx";
import { useEnterpriseApis } from "../hooks/useEnterpriseApis.js";

export function EnterpriseRegistryPage() {
  const { data = [], isLoading, createApi, updateApi, activateApi, deactivateApi, deleteApi } = useEnterpriseApis();
  const [selected, setSelected] = useState(null);
  const [editing, setEditing] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const columns = useMemo(
    () => [
      { key: "service_name", header: "Service" },
      { key: "adapter", header: "Adapter" },
      { key: "version", header: "Version" },
      { key: "status", header: "Status", render: (row) => <StatusBadge status={row.status} /> },
      { key: "allowed_agents", header: "Allowed Agents", render: (row) => row.allowed_agents?.length || 0 },
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
      <div className="grid gap-5 xl:grid-cols-[1fr_420px]">
        <Card>
          <CardBody>
            <DataTable columns={columns} rows={data} loading={isLoading} empty="No enterprise APIs registered" onRowClick={setSelected} />
          </CardBody>
        </Card>
        <Card>
          <CardHeader title={detail?.service_name || "API Details"} />
          <CardBody className="space-y-4">
            {detail ? (
              <>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <Info label="Adapter" value={detail.adapter} />
                  <Info label="Version" value={detail.version} />
                  <Info label="Status" value={<StatusBadge status={detail.status} />} />
                  <Info label="Allowed Agents" value={detail.allowed_agents?.length || 0} />
                </div>
                <TagBlock title="Permissions" items={detail.permissions} />
                <TagBlock title="Required Policies" items={detail.required_policies} />
                <pre className="max-h-52 overflow-auto rounded-md bg-slate-950 p-3 text-xs text-slate-100">{JSON.stringify(detail.endpoint_metadata, null, 2)}</pre>
              </>
            ) : (
              <div className="text-sm text-slate-500">No service selected</div>
            )}
          </CardBody>
        </Card>
      </div>
      <EnterpriseFormModal open={modalOpen} onClose={() => setModalOpen(false)} item={editing} onSubmit={submit} />
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
    <div>
      <div className="text-xs font-semibold uppercase text-slate-400">{label}</div>
      <div className="mt-1 font-medium text-ink">{value}</div>
    </div>
  );
}

function TagBlock({ title, items }) {
  return (
    <div>
      <div className="mb-2 text-xs font-semibold uppercase text-slate-400">{title}</div>
      <div className="flex flex-wrap gap-2">
        {items?.map((item) => (
          <span key={item} className="rounded-md bg-slate-100 px-2 py-1 text-xs font-medium text-slate-600">
            {item}
          </span>
        ))}
      </div>
    </div>
  );
}
