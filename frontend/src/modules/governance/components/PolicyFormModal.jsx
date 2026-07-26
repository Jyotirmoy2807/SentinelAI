import { useEffect, useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Modal } from "../../../components/modal/Modal.jsx";

const starterPolicy = `package sentinelai.custom

default decision := {
  "decision": "ALLOW",
  "matched_policy": "sentinelai.custom/default_allow",
  "reasons": ["Custom policy evaluated"],
}

decision := {
  "decision": "REQUIRE_APPROVAL",
  "matched_policy": "sentinelai.custom/high_risk_approval",
  "reasons": ["High risk requests require human approval"],
} if {
  input.risk.score >= 70
}
`;

const defaults = {
  policy_id: "",
  name: "",
  content: starterPolicy
};

export function PolicyFormModal({ open, onClose, onSubmit, pending }) {
  const [form, setForm] = useState(defaults);
  const [error, setError] = useState("");

  useEffect(() => {
    if (open) {
      setForm(defaults);
      setError("");
    }
  }, [open]);

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function submit(event) {
    event.preventDefault();
    if (!/^[a-zA-Z0-9_-]{3,80}$/.test(form.policy_id)) {
      setError("Policy ID must be 3-80 characters and use only letters, numbers, dashes, or underscores.");
      return;
    }
    if (form.name.trim().length < 2) {
      setError("Display name is required.");
      return;
    }
    if (!form.content.includes("package ")) {
      setError("Rego content must include a package declaration.");
      return;
    }
    setError("");
    onSubmit({ ...form, name: form.name.trim(), content: form.content.trim() }, setError);
  }

  return (
    <Modal title="Add OPA Policy" open={open} onClose={onClose}>
      <form className="grid gap-4" onSubmit={submit}>
        <div className="grid gap-4 md:grid-cols-2">
          <label className="text-sm font-medium text-slate-600">
            Policy ID
            <input className="mt-1 w-full rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={form.policy_id} onChange={(event) => update("policy_id", event.target.value)} placeholder="high_risk_approval" />
          </label>
          <label className="text-sm font-medium text-slate-600">
            Display Name
            <input className="mt-1 w-full rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={form.name} onChange={(event) => update("name", event.target.value)} placeholder="High Risk Approval" />
          </label>
        </div>
        <label className="text-sm font-medium text-slate-600">
          Rego Policy
          <textarea rows={16} className="mt-1 w-full rounded-md border border-line px-3 py-2 font-mono text-xs leading-5 outline-none focus:border-brand" value={form.content} onChange={(event) => update("content", event.target.value)} />
        </label>
        {error ? <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-danger">{error}</div> : null}
        <div className="flex justify-end gap-2">
          <Button type="button" tone="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" disabled={pending}>
            Add Policy
          </Button>
        </div>
      </form>
    </Modal>
  );
}
