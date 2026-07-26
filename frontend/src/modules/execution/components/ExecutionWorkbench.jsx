import { Play, RotateCcw } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { Button } from "../../../components/button/Button.jsx";
import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { GovernanceGraphView } from "../../../components/graph/GovernanceGraphView.jsx";
import { Tabs } from "../../../components/tabs/Tabs.jsx";
import { PageHeader } from "../../../layouts/PageHeader.jsx";
import { useUiStore } from "../../../store/uiStore.js";
import { formatDate, titleize } from "../../../utils/format.js";
import { governanceNodes } from "../constants.js";
import { useExecutionSamples } from "../hooks/useExecutionSamples.js";
import { useLiveExecution } from "../hooks/useLiveExecution.js";

export function ExecutionWorkbench({ simulation = false }) {
  const { data: samples = [] } = useExecutionSamples();
  const selectedNodeId = useUiStore((state) => state.selectedNodeId);
  const selectNode = useUiStore((state) => state.selectNode);
  const [sampleId, setSampleId] = useState("");
  const selectedSample = samples.find((sample) => sample.id === sampleId) || samples[0];
  const execution = useLiveExecution();
  const selectedNode = useMemo(() => governanceNodes.find((node) => node.id === selectedNodeId) || governanceNodes[0], [selectedNodeId]);
  const selectedNodeEvents = useMemo(() => execution.events.filter((event) => event.node === selectedNode?.id), [execution.events, selectedNode?.id]);
  const selectedNodeStatus = execution.nodeStatuses[selectedNode?.id] || "PENDING";
  const runStatus = execution.finalResponse?.governance?.decision || (execution.connected ? "RUNNING" : "PENDING");

  useEffect(() => {
    if (samples[0] && !sampleId) setSampleId(samples[0].id);
  }, [samples, sampleId]);

  function start() {
    if (selectedSample) {
      selectNode("api_ingestion");
      execution.start(selectedSample.request, simulation);
    }
  }

  return (
    <div>
      <PageHeader
        title={simulation ? "Simulation Lab" : "Live Governance Execution"}
        description={simulation ? "Replay governed requests with enterprise execution disabled." : "Monitor governed requests across risk, OPA, approval, audit, and response stages."}
        action={
          <div className="flex min-w-0 flex-wrap gap-2">
            <select className="h-10 min-w-0 max-w-full rounded-md border border-line bg-white px-3 text-sm outline-none focus:border-brand" value={sampleId} onChange={(event) => setSampleId(event.target.value)}>
              {samples.map((sample) => (
                <option key={sample.id} value={sample.id}>
                  {sample.name}
                </option>
              ))}
            </select>
            <Button onClick={start} disabled={!selectedSample || execution.connected}>
              <Play className="h-4 w-4" />
              {execution.connected ? "Running" : simulation ? "Replay" : "Execute"}
            </Button>
            <Button tone="secondary" onClick={() => window.location.reload()}>
              <RotateCcw className="h-4 w-4" />
              Reset
            </Button>
          </div>
        }
      />
      {execution.error ? <div className="mb-4 rounded-md bg-red-50 p-3 text-sm text-danger">{execution.error}</div> : null}

      <div className="grid gap-5">
        <div className="grid min-w-0 items-stretch gap-5 xl:grid-cols-[minmax(0,1fr)_minmax(320px,380px)]">
          <Card>
            <CardHeader title="Governance Flow" action={<StatusBadge status={runStatus} />}>
              {selectedSample?.description}
            </CardHeader>
            <CardBody className="p-3 sm:p-4">
              <GovernanceGraphView statuses={execution.nodeStatuses} />
            </CardBody>
          </Card>
          <NodeDetails node={selectedNode} status={selectedNodeStatus} events={selectedNodeEvents} />
        </div>

        <DecisionSummary response={execution.finalResponse} rawState={execution.rawState} eventCount={execution.events.length} />
        <ExecutionMonitor events={execution.events} />
        <TraceExplorer response={execution.finalResponse} rawState={execution.rawState} sampleRequest={selectedSample?.request} />
      </div>
    </div>
  );
}

function ExecutionMonitor({ events }) {
  return (
    <Card>
      <CardHeader title="Execution Monitor" action={<span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">{events.length} events</span>} />
      <CardBody className="p-0 sm:p-0">
        {events.length ? (
          <div className="max-h-[560px] overflow-y-auto overflow-x-hidden">
            <div className="hidden grid-cols-[minmax(0,1fr)_150px_110px_170px] gap-3 border-b border-line bg-slate-50 px-5 py-3 text-xs font-semibold uppercase text-slate-500 md:grid">
              <div>Stage</div>
              <div>Status</div>
              <div>Latency</div>
              <div>Request</div>
            </div>
            <div className="divide-y divide-line">
              {events.map((event, index) => (
                <div key={`${event.timestamp}-${index}`} className="grid min-w-0 gap-3 px-4 py-4 md:grid-cols-[minmax(0,1fr)_150px_110px_170px] md:px-5">
                  <div className="flex min-w-0 gap-3">
                    <div className="relative flex w-4 shrink-0 justify-center">
                      <span className={`mt-1.5 h-2.5 w-2.5 rounded-full ${eventTone(event.status)}`} />
                      {index < events.length - 1 ? <span className="absolute top-5 h-[calc(100%+1rem)] w-px bg-line" /> : null}
                    </div>
                    <div className="min-w-0">
                      <div className="break-words text-sm font-semibold text-ink">{titleize(event.node)}</div>
                      <div className="mt-1 text-xs text-slate-500">{formatDate(event.timestamp)}</div>
                    </div>
                  </div>
                  <div className="min-w-0 md:self-center">
                    <StatusBadge status={event.status} />
                  </div>
                  <div className="text-sm text-slate-600 md:self-center">{formatDuration(event.duration_ms)}</div>
                  <div className="min-w-0 truncate text-sm font-medium text-slate-600 md:self-center" title={event.request_id}>
                    {event.request_id || "Pending"}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="p-6 text-sm text-slate-500">No execution events yet.</div>
        )}
      </CardBody>
    </Card>
  );
}

function DecisionSummary({ response, rawState, eventCount }) {
  const risk = rawState?.risk || { score: response?.governance?.riskScore };
  const opa = rawState?.policy || { decision: response?.governance?.decision };
  const timeline = rawState?.audit?.events || rawState?.events || [];
  const items = [
    { label: "Risk", value: risk.level || risk.category || "Pending", detail: risk.score !== undefined ? `Score ${risk.score}` : "NIST RMF pending" },
    { label: "OPA", value: opa.decision || "Pending", detail: opa.matched_policy || "No policy result" },
    { label: "Audit", value: timeline.length || eventCount, detail: "Structured events" },
    { label: "Latency", value: totalDuration(rawState), detail: "Workflow runtime" }
  ];

  return (
    <Card>
      <CardHeader title="Decision Summary" action={opa.decision ? <StatusBadge status={opa.decision} /> : null} />
      <CardBody className="py-3 sm:py-4">
        <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
          {items.map((item) => (
            <div key={item.label} className="min-w-0 rounded-md border border-line bg-slate-50 px-3 py-2.5">
              <div className="text-xs font-semibold uppercase text-slate-400">{item.label}</div>
              <div className="mt-1.5 break-words text-base font-semibold text-ink">{item.value}</div>
              <div className="mt-1 break-words text-xs leading-4 text-slate-500">{item.detail}</div>
            </div>
          ))}
        </div>
      </CardBody>
    </Card>
  );
}

function NodeDetails({ node, status, events }) {
  const latestEvent = events.at(-1);

  return (
    <Card className="flex h-full flex-col">
      <CardHeader title="Selected Node" action={<StatusBadge status={status} />} />
      <CardBody className="flex min-h-0 flex-1 flex-col">
        <div className="break-words text-sm font-semibold text-ink">{node?.label}</div>
        <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
          <Metric label="Events" value={events.length} />
          <Metric label="Last Latency" value={formatDuration(latestEvent?.duration_ms)} />
        </div>
        <pre className="json-panel mt-4 min-h-0 flex-1 overflow-y-auto overflow-x-hidden rounded-md bg-slate-50 p-3 text-xs text-slate-700">
          {JSON.stringify(latestEvent?.payload || {}, null, 2)}
        </pre>
      </CardBody>
    </Card>
  );
}

function TraceExplorer({ response, rawState, sampleRequest }) {
  const [active, setActive] = useState("state");
  const workflowState = rawState || sampleRequest || {};
  const panels = [
    { id: "state", label: "State", payload: workflowState },
    { id: "policy", label: "Policy", payload: workflowState.policy || {} },
    { id: "api", label: "API", payload: workflowState.execution || {} },
    { id: "approval", label: "Approvals", payload: workflowState.approval || { status: "NOT_REQUIRED" } },
    { id: "audit", label: "Audit", payload: workflowState.audit?.events || [] },
    { id: "agent_response", label: "Agent Response", payload: response || {} },
    { id: "explainability", label: "Explainability", payload: workflowState.explainability?.timeline || [] }
  ];
  const selected = panels.find((panel) => panel.id === active) || panels[0];

  return (
    <Card>
      <CardHeader title="Execution Artifacts">
        {workflowState.explainability?.narrative || "Artifacts populate as the workflow runs."}
      </CardHeader>
      <CardBody>
        <Tabs tabs={panels.map(({ id, label }) => ({ id, label }))} active={selected.id} onChange={setActive} />
        <pre className="json-panel mt-4 max-h-[420px] overflow-y-auto overflow-x-hidden rounded-md bg-slate-950 p-4 text-xs leading-5 text-slate-100">
          {JSON.stringify(selected.payload, null, 2)}
        </pre>
      </CardBody>
    </Card>
  );
}

function Metric({ label, value }) {
  return (
    <div className="min-w-0 rounded-md bg-slate-50 p-3">
      <div className="text-xs font-semibold uppercase text-slate-400">{label}</div>
      <div className="mt-2 break-words font-semibold text-ink">{value}</div>
    </div>
  );
}

function formatDuration(value) {
  const duration = Number(value || 0);
  if (duration >= 1000) return `${(duration / 1000).toFixed(2)} s`;
  return `${Number.isInteger(duration) ? duration : duration.toFixed(2)} ms`;
}

function totalDuration(rawState) {
  const events = rawState?.audit?.events || rawState?.events || [];
  const total = events.reduce((sum, event) => sum + Number(event.latency || event.duration_ms || 0), 0);
  return total ? formatDuration(total) : "Pending";
}

function eventTone(status) {
  const normalized = String(status || "").toUpperCase();
  if (normalized.includes("COMPLETE") || normalized === "ALLOW" || normalized === "APPROVED") return "bg-emerald-500";
  if (normalized.includes("RUNNING")) return "bg-blue-500";
  if (normalized.includes("WAIT") || normalized.includes("PENDING")) return "bg-amber-500";
  if (normalized.includes("FAIL") || normalized.includes("DENY") || normalized.includes("REJECT")) return "bg-red-500";
  return "bg-slate-400";
}
