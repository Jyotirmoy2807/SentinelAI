import { Play, RotateCcw } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Card, CardBody, CardHeader } from "../../../components/card/Card.jsx";
import { GovernanceGraphView } from "../../../components/graph/GovernanceGraphView.jsx";
import { StatusBadge } from "../../../components/badge/StatusBadge.jsx";
import { Timeline } from "../../../components/timeline/Timeline.jsx";
import { PageHeader } from "../../../layouts/PageHeader.jsx";
import { useUiStore } from "../../../store/uiStore.js";
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
  const selectedNodeEvents = execution.events.filter((event) => event.node === selectedNode?.id);

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
        description={
          simulation
            ? "Replay governed requests through the graph with enterprise execution disabled."
            : "Real-time view of the governance graph, node status, GovernanceState, audit path, and explainability output."
        }
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
        <Card>
          <CardHeader title="Governance Flow">
            {selectedSample?.description}
          </CardHeader>
          <CardBody>
            <GovernanceGraphView statuses={execution.nodeStatuses} />
          </CardBody>
        </Card>
        <GovernanceSummary response={execution.finalResponse} />
        <TracePanels response={execution.finalResponse} />
        <div className="grid min-w-0 gap-5 xl:grid-cols-[minmax(0,0.72fr)_minmax(280px,0.28fr)]">
          <Card>
            <CardHeader title="Governance State" action={execution.finalResponse ? <StatusBadge status={execution.finalResponse.governance?.decision} /> : null} />
            <CardBody>
              <pre className="json-panel max-h-[520px] overflow-y-auto overflow-x-hidden rounded-md bg-slate-950 p-4 text-xs leading-5 text-slate-100">
                {JSON.stringify(execution.finalResponse?.state || execution.rawState || selectedSample?.request || {}, null, 2)}
              </pre>
            </CardBody>
          </Card>
          <div className="space-y-5">
            <Card>
              <CardHeader title="Node Details" />
              <CardBody>
                <div className="text-sm font-semibold text-ink">{selectedNode?.label}</div>
                <div className="mt-2">
                  <StatusBadge status={execution.nodeStatuses[selectedNode?.id] || "PENDING"} />
                </div>
                <pre className="json-panel mt-4 max-h-64 overflow-y-auto overflow-x-hidden rounded-md bg-slate-50 p-3 text-xs text-slate-700">
                  {JSON.stringify(selectedNodeEvents.at(-1)?.payload || {}, null, 2)}
                </pre>
              </CardBody>
            </Card>
            <Card>
              <CardHeader title="Audit Timeline" />
              <CardBody>
                <div className="text-sm leading-6 text-slate-600">
                  {execution.finalResponse?.explainability?.narrative || "Explainability appears after the graph reaches the explanation node."}
                </div>
              </CardBody>
            </Card>
          </div>
        </div>
        <div className="grid min-w-0 gap-5 xl:grid-cols-[minmax(280px,0.38fr)_minmax(0,0.62fr)]">
          <Card>
            <CardHeader title="Execution Timeline" />
            <CardBody>
              <Timeline events={execution.events} />
            </CardBody>
          </Card>
          <Card>
            <CardHeader title="Execution Logs" />
            <CardBody>
              <div className="max-h-96 overflow-y-auto overflow-x-hidden rounded-lg border border-line">
                <table className="w-full table-fixed divide-y divide-line text-sm">
                  <thead className="sticky top-0 bg-slate-50">
                    <tr>
                      <th className="break-words px-3 py-2 text-left">Node</th>
                      <th className="break-words px-3 py-2 text-left">Status</th>
                      <th className="break-words px-3 py-2 text-left">Duration</th>
                      <th className="break-words px-3 py-2 text-left">Request</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-line bg-white">
                    {execution.events.map((event, index) => (
                      <tr key={`${event.timestamp}-${index}`}>
                        <td className="break-words px-3 py-2 align-top">{event.node}</td>
                        <td className="break-words px-3 py-2 align-top"><StatusBadge status={event.status} /></td>
                        <td className="break-words px-3 py-2 align-top">{event.duration_ms} ms</td>
                        <td className="break-words px-3 py-2 align-top">{event.request_id}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardBody>
          </Card>
        </div>
      </div>
    </div>
  );
}

function TracePanels({ response }) {
  const state = response?.state || {};
  const panels = [
    { title: "Policy Evaluation", payload: state.policy || {} },
    { title: "API Invocations", payload: state.execution || {} },
    { title: "Human Approvals", payload: state.approval || { status: "NOT_REQUIRED" } },
    { title: "Audit Events", payload: state.audit?.events || [] },
    { title: "Explainability Trace", payload: response?.explainability?.timeline || [] }
  ];
  return (
    <div className="grid gap-4 lg:grid-cols-5">
      {panels.map((panel) => (
        <Card key={panel.title}>
          <CardHeader title={panel.title} />
          <CardBody>
            <pre className="json-panel max-h-44 overflow-y-auto overflow-x-hidden rounded-md bg-slate-50 p-3 text-xs text-slate-700">{JSON.stringify(panel.payload, null, 2)}</pre>
          </CardBody>
        </Card>
      ))}
    </div>
  );
}

function GovernanceSummary({ response }) {
  const risk = response?.governance?.risk || {};
  const opa = response?.governance?.opa || {};
  const timeline = response?.explainability?.timeline || [];
  const cards = [
    { title: "Risk Summary", value: risk.level || risk.category || "Pending", detail: risk.score !== undefined ? `Score ${risk.score}` : "NIST RMF assessment pending" },
    { title: "OPA Decision", value: opa.decision || "Pending", detail: opa.opa_url || "OPA evaluation pending" },
    { title: "Matched Policy", value: opa.matched_policy || "Pending", detail: opa.reasons?.[0] || "No policy result yet" },
    { title: "Audit Timeline", value: timeline.length || 0, detail: "Splunk-compatible events" }
  ];
  return (
    <div className="grid min-w-0 gap-4 md:grid-cols-2 xl:grid-cols-4">
      {cards.map((card) => (
        <Card key={card.title}>
          <CardBody>
            <div className="text-sm font-medium text-slate-500">{card.title}</div>
            <div className="mt-3 text-xl font-semibold text-ink">{card.value}</div>
            <div className="mt-2 text-xs leading-5 text-slate-500">{card.detail}</div>
          </CardBody>
        </Card>
      ))}
    </div>
  );
}
