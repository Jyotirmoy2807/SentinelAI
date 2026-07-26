import { useEffect, useMemo, useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Modal } from "../../../components/modal/Modal.jsx";

const EMPTY_LOOKUP_LIST = [];

export function AgentFormModal({ open, onClose, agent, onSubmit, lookups }) {
  const enterpriseApis = lookups?.enterprise_apis ?? EMPTY_LOOKUP_LIST;
  const budgetPolicies = lookups?.budget_policies ?? EMPTY_LOOKUP_LIST;
  const governancePolicies = lookups?.governance_policies ?? EMPTY_LOOKUP_LIST;
  const departments = lookups?.departments ?? EMPTY_LOOKUP_LIST;
  const versions = lookups?.versions ?? EMPTY_LOOKUP_LIST;
  const agentStatuses = lookups?.agent_statuses ?? EMPTY_LOOKUP_LIST;
  const riskTiers = lookups?.risk_tiers ?? EMPTY_LOOKUP_LIST;
  const defaults = useMemo(
    () => ({
      passport_id: "",
      name: "",
      owner: "",
      department: departments[0] || "",
      version: versions[0] || "",
      status: agentStatuses[0] || "",
      trust_score: 80,
      risk_tier: riskTiers[0] || "",
      budget_profile: budgetPolicies[0]?.name || "",
      reputation: 90,
      allowed_apis: [],
      allowed_operations: [],
      policy_groups: []
    }),
    [agentStatuses, budgetPolicies, departments, riskTiers, versions]
  );
  const [form, setForm] = useState(defaults);
  const [error, setError] = useState("");

  const operationOptions = useMemo(() => {
    const selectedApis = enterpriseApis.filter((api) => form.allowed_apis.includes(api.service_name));
    const source = selectedApis.length ? selectedApis : enterpriseApis;
    return [...new Set(source.flatMap((api) => api.supported_operations || []))].sort();
  }, [enterpriseApis, form.allowed_apis]);

  useEffect(() => {
    if (!open) return;
    setForm(agent ? { ...agent } : defaults);
    setError("");
  }, [agent, defaults, open]);

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function toggle(field, value) {
    setForm((current) => {
      const values = current[field] || [];
      const next = values.includes(value) ? values.filter((item) => item !== value) : [...values, value];
      const patch = { [field]: next };
      if (field === "allowed_apis") {
        const selectedApis = enterpriseApis.filter((api) => next.includes(api.service_name));
        const validOperations = new Set(selectedApis.flatMap((api) => api.supported_operations || []));
        patch.allowed_operations = current.allowed_operations.filter((operation) => validOperations.has(operation));
      }
      return { ...current, ...patch };
    });
  }

  function submit(event) {
    event.preventDefault();
    if (!form.passport_id || !form.name || !form.owner || !form.department || !form.status || !form.risk_tier || !form.budget_profile) {
      setError("Passport ID, name, owner, department, status, risk tier, and budget profile are required.");
      return;
    }
    onSubmit({
      ...form,
      trust_score: Number(form.trust_score),
      reputation: Number(form.reputation)
    });
  }

  return (
    <Modal title={agent ? "Edit Agent" : "Register Agent"} open={open} onClose={onClose}>
      <form className="grid gap-4 md:grid-cols-2" onSubmit={submit}>
        <Field label="Passport ID" value={form.passport_id} onChange={(value) => update("passport_id", value)} disabled={Boolean(agent)} />
        <Field label="Agent Name" value={form.name} onChange={(value) => update("name", value)} />
        <Field label="Owner" value={form.owner} onChange={(value) => update("owner", value)} />
        <Select label="Department" value={form.department} options={departments} onChange={(value) => update("department", value)} />
        <Select label="Version" value={form.version} options={versions} onChange={(value) => update("version", value)} />
        <Select label="Budget Profile" value={form.budget_profile} options={budgetPolicies.map((policy) => policy.name)} onChange={(value) => update("budget_profile", value)} />
        <Select label="Status" value={form.status} options={agentStatuses} onChange={(value) => update("status", value)} />
        <Select label="Risk Tier" value={form.risk_tier} options={riskTiers} onChange={(value) => update("risk_tier", value)} />
        <NumberField label="Trust Score" value={form.trust_score} onChange={(value) => update("trust_score", value)} />
        <NumberField label="Reputation" value={form.reputation} onChange={(value) => update("reputation", value)} />
        <Checklist title="Allowed APIs" values={form.allowed_apis} options={enterpriseApis.map((api) => api.service_name)} onToggle={(value) => toggle("allowed_apis", value)} />
        <Checklist title="Allowed Operations" values={form.allowed_operations} options={operationOptions} onToggle={(value) => toggle("allowed_operations", value)} />
        <Checklist title="Policy Groups" values={form.policy_groups} options={governancePolicies.map((policy) => policy.policy_id)} labels={Object.fromEntries(governancePolicies.map((policy) => [policy.policy_id, policy.name]))} onToggle={(value) => toggle("policy_groups", value)} />
        {error ? <div className="rounded-md bg-red-50 p-3 text-sm text-danger md:col-span-2">{error}</div> : null}
        <div className="flex justify-end gap-2 md:col-span-2">
          <Button type="button" tone="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit">{agent ? "Save Agent" : "Register Agent"}</Button>
        </div>
      </form>
    </Modal>
  );
}

function Field({ label, value, onChange, disabled }) {
  return (
    <label className="min-w-0 text-sm font-medium text-slate-600">
      {label}
      <input className="mt-1 w-full min-w-0 rounded-md border border-line px-3 py-2 outline-none focus:border-brand disabled:bg-slate-100" value={value || ""} onChange={(event) => onChange(event.target.value)} disabled={disabled} />
    </label>
  );
}

function NumberField({ label, value, onChange }) {
  return (
    <label className="min-w-0 text-sm font-medium text-slate-600">
      {label}
      <input type="number" min="0" max="100" className="mt-1 w-full min-w-0 rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={value ?? 0} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}

function Select({ label, value, options, onChange }) {
  const normalizedOptions = value && !options.includes(value) ? [value, ...options] : options;
  const hasOptions = normalizedOptions.length > 0;

  return (
    <label className="min-w-0 text-sm font-medium text-slate-600">
      {label}
      <select className="mt-1 w-full min-w-0 rounded-md border border-line px-3 py-2 outline-none focus:border-brand disabled:bg-slate-100 disabled:text-slate-400" value={value || ""} onChange={(event) => onChange(event.target.value)} disabled={!hasOptions}>
        <option value="" disabled>{hasOptions ? "Select" : "No values available"}</option>
        {normalizedOptions.map((option) => (
          <option key={option} value={option}>{option}</option>
        ))}
      </select>
    </label>
  );
}

function Checklist({ title, values = [], options = [], labels = {}, onToggle }) {
  return (
    <div className="min-w-0 md:col-span-2">
      <div className="mb-2 text-sm font-medium text-slate-600">{title}</div>
      <div className="grid gap-2 rounded-md border border-line p-3 sm:grid-cols-2">
        {options.length ? (
          options.map((option) => (
            <label key={option} className="flex min-w-0 items-center gap-2 text-sm text-slate-600">
              <input type="checkbox" checked={values.includes(option)} onChange={() => onToggle(option)} />
              <span className="min-w-0 break-words">{labels[option] || option}</span>
            </label>
          ))
        ) : (
          <div className="text-sm text-slate-400 sm:col-span-2">No options available</div>
        )}
      </div>
    </div>
  );
}
