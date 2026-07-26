import { Plus, Trash2 } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Modal } from "../../../components/modal/Modal.jsx";

const EMPTY_LOOKUP_LIST = [];
const DEFAULT_NUMERIC_FIELDS = ["identity.trustScore", "normalizedExecution.amount", "risk.score"];

export function GovernancePolicyFormModal({ open, onClose, policy, lookups, onSubmit, pending }) {
  const decisions = lookups?.decisions ?? EMPTY_LOOKUP_LIST;
  const fields = lookups?.condition_fields ?? EMPTY_LOOKUP_LIST;
  const operators = lookups?.condition_operators ?? EMPTY_LOOKUP_LIST;
  const valueOptions = useMemo(() => buildConditionValueOptions(lookups), [lookups]);
  const numericFields = lookups?.numeric_condition_fields?.length ? lookups.numeric_condition_fields : DEFAULT_NUMERIC_FIELDS;
  const defaults = useMemo(
    () => ({
      policy_id: "",
      name: "",
      description: "",
      decision: decisions[0] || "",
      priority: 100,
      enabled: true,
      conditions: [],
      reason: ""
    }),
    [decisions]
  );
  const [form, setForm] = useState(defaults);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!open) return;
    setForm(policy ? { ...policy, conditions: policy.conditions || [] } : defaults);
    setError("");
  }, [defaults, open, policy]);

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function updateCondition(index, field, value) {
    setForm((current) => ({
      ...current,
      conditions: current.conditions.map((condition, currentIndex) => {
        if (currentIndex !== index) return condition;
        const next = { ...condition, [field]: value };
        if (field === "field") next.value = "";
        return next;
      })
    }));
  }

  function addCondition() {
    setForm((current) => ({
      ...current,
      conditions: [
        ...current.conditions,
        {
          field: fields[0]?.value || "",
          operator: operators[0]?.value || "",
          value: ""
        }
      ]
    }));
  }

  function removeCondition(index) {
    setForm((current) => ({ ...current, conditions: current.conditions.filter((_, currentIndex) => currentIndex !== index) }));
  }

  function submit(event) {
    event.preventDefault();
    if (!form.policy_id || !form.name || !form.decision || !form.reason) {
      setError("Policy ID, name, decision, and reason are required.");
      return;
    }
    if (form.conditions.some((condition) => !condition.field || !condition.operator || condition.value === "")) {
      setError("Every condition must include a field, operator, and value.");
      return;
    }
    setError("");
    onSubmit(
      {
        ...form,
        priority: Number(form.priority),
        conditions: form.conditions.map((condition) => ({ ...condition, value: coerceValue(condition.value) }))
      },
      setError
    );
  }

  return (
    <Modal title={policy ? "Edit Governance Policy" : "Create Governance Policy"} open={open} onClose={onClose}>
      <form className="grid gap-4" onSubmit={submit}>
        <div className="grid gap-4 md:grid-cols-2">
          <Field label="Policy ID" value={form.policy_id} onChange={(value) => update("policy_id", value)} disabled={Boolean(policy)} />
          <Field label="Name" value={form.name} onChange={(value) => update("name", value)} />
          <Select label="Decision" value={form.decision} options={decisions.map((value) => ({ value, label: value }))} onChange={(value) => update("decision", value)} />
          <Field label="Priority" type="number" value={form.priority} onChange={(value) => update("priority", value)} />
        </div>
        <label className="text-sm font-medium text-slate-600">
          Description
          <textarea rows={2} className="mt-1 w-full min-w-0 rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={form.description || ""} onChange={(event) => update("description", event.target.value)} />
        </label>
        <label className="inline-flex items-center gap-2 text-sm font-medium text-slate-600">
          <input type="checkbox" checked={Boolean(form.enabled)} onChange={(event) => update("enabled", event.target.checked)} />
          Enabled
        </label>
        <div className="rounded-md border border-line p-3">
          <div className="mb-3 flex items-center justify-between gap-3">
            <div className="text-sm font-semibold text-ink">Conditions</div>
            <Button type="button" tone="secondary" onClick={addCondition}>
              <Plus className="h-4 w-4" />
              Add Condition
            </Button>
          </div>
          <div className="grid gap-3">
            {form.conditions.length ? (
              form.conditions.map((condition, index) => (
                <div key={`${condition.field}-${index}`} className="grid min-w-0 gap-2 rounded-md bg-slate-50 p-2 md:grid-cols-[minmax(0,1fr)_minmax(0,1fr)_minmax(0,1fr)_auto]">
                  <Select value={condition.field} options={fields} onChange={(value) => updateCondition(index, "field", value)} />
                  <Select
                    value={condition.operator}
                    options={operatorsForCondition(condition, operators, numericFields, valueOptions)}
                    onChange={(value) => updateCondition(index, "operator", value)}
                  />
                  <ConditionValueControl
                    condition={condition}
                    options={valueOptions[condition.field] || EMPTY_LOOKUP_LIST}
                    numeric={numericFields.includes(condition.field)}
                    onChange={(value) => updateCondition(index, "value", value)}
                  />
                  <button type="button" title="Remove condition" className="rounded-md p-2 text-danger hover:bg-red-50" onClick={() => removeCondition(index)}>
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))
            ) : (
              <div className="rounded-md bg-slate-50 px-3 py-6 text-center text-sm text-slate-500">No conditions. The policy will match every request.</div>
            )}
          </div>
        </div>
        <Field label="Reason" value={form.reason} onChange={(value) => update("reason", value)} />
        {error ? <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-danger">{formatError(error)}</div> : null}
        <div className="flex justify-end gap-2">
          <Button type="button" tone="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" disabled={pending}>
            Save Policy
          </Button>
        </div>
      </form>
    </Modal>
  );
}

function Field({ label, type = "text", value, onChange, disabled }) {
  return (
    <label className="min-w-0 text-sm font-medium text-slate-600">
      {label}
      <input type={type} className="mt-1 w-full min-w-0 rounded-md border border-line px-3 py-2 outline-none focus:border-brand disabled:bg-slate-100" value={value ?? ""} onChange={(event) => onChange(event.target.value)} disabled={disabled} />
    </label>
  );
}

function Select({ label, value, options, onChange }) {
  const normalizedOptions = value && !options.some((option) => option.value === value) ? [{ value, label: value }, ...options] : options;
  const hasOptions = normalizedOptions.length > 0;
  const control = (
    <select className="w-full min-w-0 rounded-md border border-line px-3 py-2 text-sm outline-none focus:border-brand disabled:bg-slate-100 disabled:text-slate-400" value={value || ""} onChange={(event) => onChange(event.target.value)} disabled={!hasOptions}>
      <option value="" disabled>{hasOptions ? "Select" : "No values available"}</option>
      {normalizedOptions.map((option) => (
        <option key={option.value} value={option.value}>{option.label}</option>
      ))}
    </select>
  );
  if (!label) return control;
  return (
    <label className="min-w-0 text-sm font-medium text-slate-600">
      {label}
      <div className="mt-1">{control}</div>
    </label>
  );
}

function ConditionValueControl({ condition, options, numeric, onChange }) {
  if (numeric) {
    return (
      <input
        type="number"
        className="min-w-0 rounded-md border border-line px-3 py-2 text-sm outline-none focus:border-brand"
        value={condition.value ?? ""}
        onChange={(event) => onChange(event.target.value)}
      />
    );
  }
  if (options.length) {
    const normalizedOptions = condition.value && !options.some((option) => option.value === condition.value) ? [{ value: condition.value, label: condition.value }, ...options] : options;
    return <Select value={condition.value} options={normalizedOptions} onChange={onChange} />;
  }
  return (
    <input
      className="min-w-0 rounded-md border border-line px-3 py-2 text-sm outline-none focus:border-brand"
      value={condition.value ?? ""}
      onChange={(event) => onChange(event.target.value)}
    />
  );
}

function coerceValue(value) {
  if (value === "true") return true;
  if (value === "false") return false;
  const numberValue = Number(value);
  return Number.isNaN(numberValue) || value === "" ? value : numberValue;
}

function formatError(error) {
  if (Array.isArray(error)) return error.map((item) => item.msg || item).join(", ");
  return String(error);
}

function buildConditionValueOptions(lookups) {
  const provided = lookups?.condition_value_options || {};
  const apiOperations = lookups?.api_operations?.map((item) => item.operation) || [];
  const groupedOperations = lookups?.enterprise_apis?.flatMap((api) => api.supported_operations || []) || [];
  return {
    "identity.status": toOptions(provided["identity.status"], lookups?.agent_statuses),
    "identity.department": toOptions(provided["identity.department"], lookups?.departments),
    "identity.riskTier": toOptions(provided["identity.riskTier"], lookups?.risk_tiers),
    "normalizedExecution.service": toOptions(provided["normalizedExecution.service"], lookups?.services),
    "normalizedExecution.operation": toOptions(provided["normalizedExecution.operation"], [...apiOperations, ...groupedOperations]),
    "risk.level": toOptions(provided["risk.level"], lookups?.risk_tiers),
    "risk.category": toOptions(provided["risk.category"], lookups?.risk_tiers),
  };
}

function operatorsForCondition(condition, operators, numericFields, valueOptions) {
  const field = condition.field;
  if (numericFields.includes(field)) return operators.filter((operator) => ["equals", "not_equals", "greater_than", "greater_or_equal", "less_than", "less_or_equal"].includes(operator.value));
  if (valueOptions[field]?.length) return operators.filter((operator) => ["equals", "not_equals"].includes(operator.value));
  return operators.filter((operator) => ["equals", "not_equals", "contains"].includes(operator.value));
}

function toOptions(primary, fallback = []) {
  const values = primary?.length ? primary : fallback || [];
  const normalized = values.map((item) => (typeof item === "string" ? { value: item, label: item } : item));
  const seen = new Set();
  return normalized.filter((item) => {
    if (!item?.value || seen.has(item.value)) return false;
    seen.add(item.value);
    return true;
  });
}
