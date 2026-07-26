import { Background, Controls, ReactFlow } from "@xyflow/react";
import { useMemo } from "react";
import { governanceEdges, governanceNodes } from "../../modules/execution/constants.js";
import { useUiStore } from "../../store/uiStore.js";

export function GovernanceGraphView({ statuses }) {
  const selectNode = useUiStore((state) => state.selectNode);
  const selectedNodeId = useUiStore((state) => state.selectedNodeId);
  const nodes = useMemo(
    () =>
      governanceNodes.map((node) => ({
        ...node,
        data: { label: <NodeLabel label={node.label} status={statuses[node.id] || "PENDING"} /> },
        className: node.id === selectedNodeId ? "ring-2 ring-brand" : "",
        style: nodeStyle(statuses[node.id])
      })),
    [statuses, selectedNodeId]
  );
  const edges = useMemo(
    () =>
      governanceEdges.map((edge) => ({
        ...edge,
        animated: statuses[edge.source] === "RUNNING",
        style: { stroke: statuses[edge.source] === "RUNNING" ? "#1d4ed8" : "#cbd5e1", strokeWidth: 2 }
      })),
    [statuses]
  );

  return (
    <div className="h-[420px] rounded-lg border border-line bg-white">
      <ReactFlow nodes={nodes} edges={edges} fitView onNodeClick={(_, node) => selectNode(node.id)} nodesDraggable={false} nodesConnectable={false}>
        <Background color="#e2e8f0" gap={18} />
        <Controls showInteractive={false} />
      </ReactFlow>
    </div>
  );
}

function NodeLabel({ label, status }) {
  return (
    <div className="space-y-1">
      <div>{label}</div>
      <div className="text-[10px] font-semibold uppercase text-slate-500">{status.replaceAll("_", " ")}</div>
    </div>
  );
}

function nodeStyle(status) {
  const base = {
    borderRadius: 8,
    border: "1px solid #d8dee9",
    padding: 12,
    width: 190,
    fontSize: 13,
    fontWeight: 700,
    color: "#172033"
  };
  const tones = {
    RUNNING: { background: "#dbeafe", border: "2px solid #1d4ed8" },
    COMPLETED: { background: "#ecfdf5", border: "1px solid #a7f3d0" },
    DENIED: { background: "#fef2f2", border: "1px solid #fecaca" },
    WAITING_APPROVAL: { background: "#fffbeb", border: "1px solid #fde68a" },
    FAILED: { background: "#fef2f2", border: "2px solid #b91c1c" },
    PENDING: { background: "#ffffff" }
  };
  return { ...base, ...(tones[status] || tones.PENDING) };
}
