import { Background, Controls, ReactFlow, useEdgesState, useNodesState } from "@xyflow/react";
import { useEffect, useMemo } from "react";
import { governanceEdges, governanceNodes } from "../../modules/execution/constants.js";
import { useUiStore } from "../../store/uiStore.js";

const fitViewOptions = { padding: 0.08, minZoom: 0.68, maxZoom: 1 };

export function GovernanceGraphView({ statuses = {} }) {
  const selectNode = useUiStore((state) => state.selectNode);
  const selectedNodeId = useUiStore((state) => state.selectedNodeId);

  const initialNodes = useMemo(
    () => governanceNodes.map((node) => decorateNode(node, "PENDING", false)),
    []
  );
  const initialEdges = useMemo(
    () => governanceEdges.map((edge) => decorateEdge(edge, {})),
    []
  );
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  useEffect(() => {
    setNodes((currentNodes) =>
      currentNodes.map((node) => decorateNode(node, statuses[node.id] || "PENDING", node.id === selectedNodeId))
    );
  }, [selectedNodeId, setNodes, statuses]);

  useEffect(() => {
    setEdges((currentEdges) => currentEdges.map((edge) => decorateEdge(edge, statuses)));
  }, [setEdges, statuses]);

  return (
    <div className="h-[460px] min-w-0 rounded-lg border border-line bg-white">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={(_, node) => selectNode(node.id)}
        fitView
        fitViewOptions={fitViewOptions}
        minZoom={0.55}
        maxZoom={1.2}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#dbe3ef" gap={18} />
        <Controls showInteractive={false} />
      </ReactFlow>
    </div>
  );
}

function decorateNode(node, status, selected) {
  return {
    ...node,
    data: { label: <NodeLabel label={node.label || node.data?.rawLabel} status={status} />, rawLabel: node.label || node.data?.rawLabel },
    className: selected ? "ring-2 ring-brand" : "",
    style: nodeStyle(status)
  };
}

function decorateEdge(edge, statuses) {
  const active = statuses[edge.source] === "RUNNING" || statuses[edge.target] === "RUNNING";
  const completed = statuses[edge.source] === "COMPLETED" && statuses[edge.target] && statuses[edge.target] !== "PENDING";
  return {
    ...edge,
    animated: active,
    style: {
      stroke: active ? "#1d4ed8" : completed ? "#059669" : "#94a3b8",
      strokeWidth: active ? 2.6 : 2
    },
    labelStyle: { fill: "#475569", fontSize: 11, fontWeight: 700, textTransform: "uppercase" },
    labelBgStyle: { fill: "#ffffff", fillOpacity: 0.9 },
    markerEnd: { type: "arrowclosed", color: active ? "#1d4ed8" : completed ? "#059669" : "#94a3b8" }
  };
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
    width: 176,
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
    PENDING: { background: "#f8fafc", border: "1px solid #cbd5e1" }
  };
  return { ...base, ...(tones[status] || tones.PENDING) };
}
