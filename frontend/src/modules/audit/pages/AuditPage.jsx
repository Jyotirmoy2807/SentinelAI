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
      { key: "stage", header: "Stage" },
      { key: "agent", header: "Agent" },
      { key: "action", header: "Action" },
      { key: "policy", header: "Policy" },
      { key: "risk_score", header: "Risk" },
      { key: "decision", header: "Decision", render: (row) => <StatusBadge status={row.decision} /> },
      { key: "timestamp", header: "Timestamp", render: (row) => formatDate(row.timestamp) }
    ],
    []
  );
  const currentDetail = detail.data || (rows[0]?.request_id === requestId ? detail.data : null);

  return (
    <div className="flex h-full min-h-0 flex-col">
      <PageHeader
        title="Audit & Explainability"
        description="Splunk-compatible governance events, decision trail, request detail, execution evidence, and reasoning context."
      />
      <div className="grid min-h-0 min-w-0 flex-1 gap-5 overflow-y-auto overflow-x-hidden xl:grid-cols-[minmax(0,1fr)_minmax(320px,460px)] xl:overflow-hidden">
        <Card className="flex min-h-0 flex-col">
          <CardBody className="min-h-0 flex-1 overflow-y-auto overflow-x-hidden">
            <DataTable
              columns={columns}
              rows={rows}
              loading={list.isLoading}
              empty="No audit records found"
              initialSortKey="timestamp"
              initialDirection="desc"
              onRowClick={(row) => setRequestId(row.request_id)}
            />
          </CardBody>
        </Card>
        <AuditDetails detail={currentDetail} />
      </div>
    </div>
  );
}
