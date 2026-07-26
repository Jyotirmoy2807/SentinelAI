import { useEffect, useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Modal } from "../../../components/modal/Modal.jsx";

const defaults = {
  policies: {
    policy_id: "",
    name: "",
    description: "",
    priority: 100,
    status: "ACTIVE",
    version: "1.0",
    department: "Enterprise",
    policy_group: "default",
    conditions: "{}",
    actions: "{\"decision\":\"ALLOW\",\"reason\":\"Configured governance policy.\"}"
  },
  firewall: {
    rule_id: "",
    name: "",
    category: "Safety",
    severity: "MEDIUM",
    status: "ACTIVE",
    pattern: "",
    blocked_services: "[]",
    blocked_operations: "[]",
    updated_by: "governance.admin",
    version: "1.0"
  },
  compliance: {
    rule_id: "",
    name: "",
    framework: "Internal",
    status: "ACTIVE",
    version: "1.0",
    affected_departments: "[\"All\"]",
    conditions: "{}",
    require_approval: false
  },
  budget: {
    name: "",
    department: "Enterprise",
    daily_limit: 5000,
    monthly_limit: 100000,
    transaction_limit: 1000,
    approval_threshold: 500,
    spent_today: 0,
    spent_month: 0,
    status: "ACTIVE"
  }
};

export function ResourceFormModal({ kind, open, item, onClose, onSubmit }) {
  const [form, setForm] = useState(defaults[kind]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!open) return;
    const next = item ? serializeItem(kind, item) : defaults[kind];
    setForm(next);
    setError("");
  }, [item, kind, open]);

  function update(key, value) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  function submit(event) {
    event.preventDefault();
    try {
      onSubmit(parsePayload(kind, form));
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <Modal title={item ? "Edit Governance Configuration" : "Create Governance Configuration"} open={open} onClose={onClose}>
      <form className="grid gap-4 md:grid-cols-2" onSubmit={submit}>
        {Object.entries(form).map(([key, value]) => (
          <label key={key} className={`text-sm font-medium text-slate-600 ${isJsonField(key) ? "md:col-span-2" : ""}`}>
            {key.replaceAll("_", " ")}
            {isJsonField(key) ? (
              <textarea
                rows={4}
                className="mt-1 w-full rounded-md border border-line px-3 py-2 font-mono text-xs outline-none focus:border-brand"
                value={value}
                onChange={(event) => update(key, event.target.value)}
              />
            ) : typeof value === "boolean" ? (
              <select className="mt-1 w-full rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={String(value)} onChange={(event) => update(key, event.target.value === "true")}>
                <option value="true">true</option>
                <option value="false">false</option>
              </select>
            ) : (
              <input className="mt-1 w-full rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={value ?? ""} onChange={(event) => update(key, event.target.value)} />
            )}
          </label>
        ))}
        {error ? <div className="rounded-md bg-red-50 p-3 text-sm text-danger md:col-span-2">{error}</div> : null}
        <div className="flex justify-end gap-2 md:col-span-2">
          <Button type="button" tone="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit">Save</Button>
        </div>
      </form>
    </Modal>
  );
}

function isJsonField(key) {
  return ["conditions", "actions", "blocked_services", "blocked_operations", "affected_departments"].includes(key);
}

function serializeItem(kind, item) {
  const output = {};
  Object.keys(defaults[kind]).forEach((key) => {
    const value = item[key];
    output[key] = typeof defaults[kind][key] === "string" && isJsonField(key) ? JSON.stringify(value ?? JSON.parse(defaults[kind][key]), null, 2) : value ?? defaults[kind][key];
  });
  return output;
}

function parsePayload(kind, form) {
  const payload = { ...form };
  Object.keys(payload).forEach((key) => {
    if (isJsonField(key)) payload[key] = JSON.parse(payload[key] || (key.includes("departments") || key.includes("blocked") ? "[]" : "{}"));
    if (["priority", "daily_limit", "monthly_limit", "transaction_limit", "approval_threshold", "spent_today", "spent_month"].includes(key)) {
      payload[key] = Number(payload[key]);
    }
  });
  if (kind !== "budget" && !payload.rule_id && !payload.policy_id) {
    payload.rule_id = `RULE-${Date.now()}`;
  }
  return payload;
}
