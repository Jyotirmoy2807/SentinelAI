import { useMemo, useState } from "react";
import { Card, CardBody } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { DataTable } from "../../../components/table/DataTable.jsx";
import { PageHeader } from "../../../layouts/PageHeader.jsx";
import { formatDate } from "../../../utils/format.js";
import { AuditDetails } from "../components/AuditDetails.jsx";
import { useAudit } from "../hooks/useAudit.js";

export function AuditPage() {
  const [requestId, setRequestId] = useState("");
  const { list, detail } = useAudit(requestId);
  const rows = list.data || [];
  const columns = useMemo(
    () => [
      { key: "request_id", header: "Request ID" },
      { key: "node", header: "Node" },
      { key: "event_type", header: "Event" },
      { key: "decision", header: "Decision", render: (row) => <StatusBadge status={row.decision} /> },
      { key: "message", header: "Message" },
      { key: "created_at", header: "Timestamp", render: (row) => formatDate(row.created_at) }
    ],
    []
  );
  const currentDetail = detail.data || (rows[0]?.request_id === requestId ? detail.data : null);

  return (
    <div>
      <PageHeader
        title="Audit & Explainability"
        description="Immutable governance history, decision trail, request detail, execution evidence, and reasoning context."
      />
      <div className="grid gap-5 xl:grid-cols-[1fr_460px]">
        <Card>
          <CardBody>
            <DataTable
              columns={columns}
              rows={rows}
              loading={list.isLoading}
              empty="No audit records found"
              onRowClick={(row) => setRequestId(row.request_id)}
            />
          </CardBody>
        </Card>
        <AuditDetails detail={currentDetail} />
      </div>
    </div>
  );
}
