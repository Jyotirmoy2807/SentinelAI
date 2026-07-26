import { ArrowRight, ShieldCheck } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "../components/button/Button.jsx";
import { Card, CardBody } from "../components/card/Card.jsx";
import { StatusBadge } from "../components/badge/StatusBadge.jsx";

const checkpoints = [
  "Identity",
  "NIST RMF Risk",
  "OPA Policy",
  "Approval",
  "Execution",
  "Splunk Audit",
  "Explainability"
];

export function LandingPage() {
  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-lg border border-line bg-white shadow-sm">
        <div className="grid min-h-[520px] gap-8 p-8 lg:grid-cols-[0.9fr_1.1fr] lg:p-10">
          <div className="flex flex-col justify-center">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-md bg-brand text-white">
              <ShieldCheck className="h-6 w-6" />
            </div>
            <h1 className="max-w-2xl text-4xl font-semibold tracking-normal text-ink">SentinelAI</h1>
            <p className="mt-4 max-w-xl text-base leading-7 text-slate-600">
              Enterprise governance for autonomous AI agents, centered on deterministic checkpoints, auditability, and explainable execution.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link to="/dashboard">
                <Button>
                  Open Console
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Link to="/live">
                <Button tone="secondary">Watch Live Governance</Button>
              </Link>
            </div>
          </div>
          <div className="flex items-center">
            <div className="grid w-full grid-cols-2 gap-3 md:grid-cols-5">
              {checkpoints.map((checkpoint, index) => (
                <Card key={checkpoint} className="min-h-24">
                  <CardBody className="flex h-full flex-col justify-between">
                    <span className="text-xs font-semibold text-slate-400">0{index + 1}</span>
                    <span className="text-sm font-semibold text-ink">{checkpoint}</span>
                    <StatusBadge status={index < 6 ? "COMPLETED" : index === 6 ? "PENDING" : "ACTIVE"} />
                  </CardBody>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
