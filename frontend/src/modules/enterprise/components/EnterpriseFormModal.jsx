import { useEffect, useMemo, useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Modal } from "../../../components/modal/Modal.jsx";

const EMPTY_LOOKUP_LIST = [];

export function EnterpriseFormModal({ open, onClose, item, onSubmit, adapters = [], policies = [], versions = [], statuses = [] }) {
  const defaultAdapter = adapters[0]?.name || "";
  const defaultOperations = adapters[0]?.supported_operations ?? EMPTY_LOOKUP_LIST;
  const defaults = useMemo(
    () => ({
      service_name: "",
      adapter: defaultAdapter,
      version: versions[0] || "",
      status: statuses[0] || "",
      supported_operations: defaultOperations,
      required_policies: [],
      endpoint_metadata: "{\"owner\":\"Platform\",\"sla\":\"250ms mock\"}"
    }),
    [defaultAdapter, defaultOperations, statuses, versions]
  );
  const [form, setForm] = useState(defaults);
  const [error, setError] = useState("");

  const selectedAdapter = adapters.find((adapter) => adapter.name === form.adapter);
  const operationOptions = selectedAdapter?.supported_operations ?? EMPTY_LOOKUP_LIST;

  useEffect(() => {
    if (!open) return;
    setForm(
      item
        ? {
            ...item,
            supported_operations: item.supported_operations || [],
            required_policies: item.required_policies || [],
            endpoint_metadata: JSON.stringify(item.endpoint_metadata || {}, null, 2)
          }
        : defaults
    );
    setError("");
  }, [defaults, item, open]);

  function update(key, value) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  function updateAdapter(value) {
    const adapter = adapters.find((item) => item.name === value);
    setForm((current) => ({ ...current, adapter: value, supported_operations: adapter?.supported_operations ?? EMPTY_LOOKUP_LIST }));
  }

  function toggleList(field, value) {
    setForm((current) => {
      const currentValues = current[field] || [];
      const nextValues = currentValues.includes(value) ? currentValues.filter((item) => item !== value) : [...currentValues, value];
      return { ...current, [field]: nextValues };
    });
  }

  function submit(event) {
    event.preventDefault();
    try {
      onSubmit({
        ...form,
        endpoint_metadata: JSON.parse(form.endpoint_metadata || "{}")
      });
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <Modal title={item ? "Edit Enterprise API" : "Register Enterprise API"} open={open} onClose={onClose}>
      <form className="grid gap-4 md:grid-cols-2" onSubmit={submit}>
        <Field label="Service Name" value={form.service_name} onChange={(value) => update("service_name", value)} />
        <Select label="Adapter" value={form.adapter} options={adapters.map((adapter) => adapter.name)} onChange={updateAdapter} />
        <Select label="Version" value={form.version} options={versions} onChange={(value) => update("version", value)} />
        <Select label="Status" value={form.status} options={statuses} onChange={(value) => update("status", value)} />
        <Checklist title="Supported Operations" values={form.supported_operations} options={operationOptions} onToggle={(value) => toggleList("supported_operations", value)} />
        <Checklist title="Required Policies" values={form.required_policies} options={policies.map((policy) => policy.policy_id)} labels={Object.fromEntries(policies.map((policy) => [policy.policy_id, policy.name]))} onToggle={(value) => toggleList("required_policies", value)} />
        <label className="text-sm font-medium text-slate-600 md:col-span-2">
          Endpoint Metadata
          <textarea rows={4} className="mt-1 w-full min-w-0 rounded-md border border-line px-3 py-2 font-mono text-xs outline-none focus:border-brand" value={form.endpoint_metadata} onChange={(event) => update("endpoint_metadata", event.target.value)} />
        </label>
        {error ? <div className="rounded-md bg-red-50 p-3 text-sm text-danger md:col-span-2">{error}</div> : null}
        <div className="flex justify-end gap-2 md:col-span-2">
          <Button type="button" tone="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit">Save API</Button>
        </div>
      </form>
    </Modal>
  );
}

function Field({ label, value, onChange }) {
  return (
    <label className="min-w-0 text-sm font-medium text-slate-600">
      {label}
      <input className="mt-1 w-full min-w-0 rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={value || ""} onChange={(event) => onChange(event.target.value)} />
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
