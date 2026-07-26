import { Ban, CheckCircle, Edit, PauseCircle, Plus, Trash2 } from "lucide-react";
import { useMemo, useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Card, CardBody } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { DataTable } from "../../../components/table/DataTable.jsx";
import { PageHeader } from "../../../layouts/PageHeader.jsx";
import { formatDate } from "../../../utils/format.js";
import { AgentDetails } from "../components/AgentDetails.jsx";
import { AgentFormModal } from "../components/AgentFormModal.jsx";
import { useAgents } from "../hooks/useAgents.js";
import { useGovernanceResources } from "../../governance/hooks/useGovernanceResources.js";

export function AgentsPage() {
  const { data = [], isLoading, createAgent, updateAgent, suspendAgent, activateAgent, blockAgent, deleteAgent } = useAgents();
  const governance = useGovernanceResources();
  const [selected, setSelected] = useState(null);
  const [editing, setEditing] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const columns = useMemo(
    () => [
      { key: "passport_id", header: "Passport ID" },
      { key: "name", header: "Agent" },
      { key: "department", header: "Department" },
      { key: "status", header: "Status", render: (row) => <StatusBadge status={row.status} /> },
      { key: "trust_score", header: "Trust" },
      { key: "risk_tier", header: "Risk" },
      { key: "last_activity", header: "Last Activity", render: (row) => formatDate(row.last_activity) },
      {
        key: "actions",
        header: "Actions",
        render: (row) => (
          <div className="flex flex-wrap gap-1" onClick={(event) => event.stopPropagation()}>
            <IconButton label="Edit" onClick={() => openEdit(row)} icon={Edit} />
            <IconButton label="Activate" onClick={() => activateAgent.mutate(row.id)} icon={CheckCircle} />
            <IconButton label="Suspend" onClick={() => suspendAgent.mutate(row.id)} icon={PauseCircle} />
            <IconButton label="Block" onClick={() => blockAgent.mutate(row.id)} icon={Ban} />
            <IconButton label="Delete" onClick={() => deleteAgent.mutate(row.id)} icon={Trash2} danger />
          </div>
        )
      }
    ],
    [activateAgent, blockAgent, deleteAgent, suspendAgent]
  );

  function openCreate() {
    setEditing(null);
    setModalOpen(true);
  }

  function openEdit(agent) {
    setEditing(agent);
    setModalOpen(true);
  }

  function submit(payload) {
    const mutation = editing ? updateAgent.mutateAsync({ id: editing.id, payload }) : createAgent.mutateAsync(payload);
    mutation.then(() => {
      setModalOpen(false);
      setEditing(null);
    });
  }

  return (
    <div>
      <PageHeader
        title="Agent Management"
        description="Managed Agent Passports, API access, OPA policy profiles, trust scores, and execution posture for autonomous AI agents."
        action={
          <Button onClick={openCreate}>
            <Plus className="h-4 w-4" />
            Register Agent
          </Button>
        }
      />
      <div className="grid min-w-0 gap-5 xl:grid-cols-[minmax(0,1fr)_minmax(320px,420px)]">
        <Card>
          <CardBody>
            <DataTable columns={columns} rows={data} loading={isLoading} empty="No agents registered" onRowClick={setSelected} />
          </CardBody>
        </Card>
        <AgentDetails agent={selected || data[0]} />
      </div>
      <AgentFormModal open={modalOpen} onClose={() => setModalOpen(false)} agent={editing} onSubmit={submit} lookups={governance.lookups.data} />
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
