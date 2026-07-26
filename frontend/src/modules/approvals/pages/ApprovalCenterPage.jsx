import { useMemo, useState } from "react";
import { Card, CardBody } from "../../../components/card/Card.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { DataTable } from "../../../components/table/DataTable.jsx";
import { PageHeader } from "../../../layouts/PageHeader.jsx";
import { formatDate } from "../../../utils/format.js";
import { ApprovalDetails } from "../components/ApprovalDetails.jsx";
import { useApprovals } from "../hooks/useApprovals.js";

export function ApprovalCenterPage() {
  const { data = [], isLoading, approveApproval, rejectApproval } = useApprovals();
  const [selected, setSelected] = useState(null);
  const [comments, setComments] = useState("");
  const [response, setResponse] = useState(null);
  const columns = useMemo(
    () => [
      { key: "request_id", header: "Request ID" },
      { key: "agent_name", header: "Agent" },
      { key: "operation", header: "Operation" },
      { key: "risk_score", header: "Risk" },
      { key: "amount", header: "Amount" },
      { key: "created_at", header: "Submitted", render: (row) => formatDate(row.created_at) },
      { key: "approver", header: "Approver" },
      { key: "status", header: "Status", render: (row) => <StatusBadge status={row.status} /> }
    ],
    []
  );
  const current = selected || data.find((item) => item.status === "PENDING") || data[0];

  function approve() {
    approveApproval.mutateAsync({ id: current.approval_id, payload: { approver: "Governance Manager", comments } }).then(setResponse);
  }

  function reject() {
    rejectApproval.mutateAsync({ id: current.approval_id, payload: { approver: "Governance Manager", comments } }).then(setResponse);
  }

  return (
    <div>
      <PageHeader
        title="Human Approval Center"
        description="Pending and completed governance reviews with the context needed to resume or deny paused workflows."
      />
      <div className="grid min-w-0 gap-5 xl:grid-cols-[minmax(0,1fr)_minmax(320px,440px)]">
        <Card>
          <CardBody>
            <DataTable
              columns={columns}
              rows={data}
              loading={isLoading}
              empty="No approvals found"
              onRowClick={(row) => {
                setSelected(row);
                setComments(row.comments || "");
                setResponse(null);
              }}
            />
          </CardBody>
        </Card>
        <ApprovalDetails
          approval={current}
          comments={comments}
          setComments={setComments}
          onApprove={approve}
          onReject={reject}
          response={response}
        />
      </div>
    </div>
  );
}
