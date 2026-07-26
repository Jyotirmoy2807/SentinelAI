import { useEffect, useMemo, useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Modal } from "../../../components/modal/Modal.jsx";

const EMPTY_LOOKUP_LIST = [];
const DEFAULT_VERSION_OPTIONS = ["1.0"];
const NEW_SERVICE = "__new_service__";
const NEW_VERSION = "__new_version__";

export function EnterpriseFormModal({ open, onClose, item, onSubmit, lookups = {}, policies = [], versions = [], statuses = [] }) {
  const services = lookups.services ?? EMPTY_LOOKUP_LIST;
  const methods = lookups.methods ?? EMPTY_LOOKUP_LIST;
  const authTypes = lookups.authentication_types ?? EMPTY_LOOKUP_LIST;
  const statusOptions = statuses.length ? statuses : lookups.statuses ?? EMPTY_LOOKUP_LIST;
  const versionOptions = versions.length ? versions : DEFAULT_VERSION_OPTIONS;

  const defaults = useMemo(
    () => ({
      service_name: services[0] || NEW_SERVICE,
      new_service_name: "",
      operation: "",
      method: methods.includes("POST") ? "POST" : methods[0] || "POST",
      base_url: "mock://enterprise",
      path: "/",
      authentication_type: authTypes.includes("NONE") ? "NONE" : authTypes[0] || "NONE",
      authentication_config: "{}",
      timeout_seconds: 30,
      retry_count: 0,
      version: versionOptions[0] || "1.0",
      new_version: "",
      status: statusOptions[0] || "ACTIVE",
      required_policies: [],
      endpoint_metadata: "{\"owner\":\"Platform\",\"sla\":\"250ms mock\"}"
    }),
    [authTypes, methods, services, statusOptions, versionOptions]
  );

  const [form, setForm] = useState(defaults);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!open) return;
    setForm(
      item
        ? {
            ...item,
            new_service_name: "",
            authentication_config: JSON.stringify(item.authentication_config || {}, null, 2),
            required_policies: item.required_policies || [],
            endpoint_metadata: JSON.stringify(item.endpoint_metadata || {}, null, 2),
            new_version: ""
          }
        : defaults
    );
    setError("");
  }, [defaults, item, open]);

  function update(key, value) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  function togglePolicy(value) {
    setForm((current) => {
      const currentValues = current.required_policies || [];
      const required_policies = currentValues.includes(value) ? currentValues.filter((item) => item !== value) : [...currentValues, value];
      return { ...current, required_policies };
    });
  }

  function submit(event) {
    event.preventDefault();
    try {
      const serviceName = form.service_name === NEW_SERVICE ? form.new_service_name.trim() : form.service_name;
      const version = form.version === NEW_VERSION ? form.new_version.trim() : form.version;
      if (!serviceName) throw new Error("Service name is required.");
      if (!version) throw new Error("Version is required.");
      onSubmit({
        service_name: serviceName,
        operation: form.operation.trim(),
        method: form.method,
        base_url: form.base_url.trim(),
        path: form.path.trim(),
        authentication_type: form.authentication_type,
        authentication_config: JSON.parse(form.authentication_config || "{}"),
        timeout_seconds: Number(form.timeout_seconds || 30),
        retry_count: Number(form.retry_count || 0),
        version,
        status: form.status,
        required_policies: form.required_policies || [],
        endpoint_metadata: JSON.parse(form.endpoint_metadata || "{}")
      });
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <Modal title={item ? "Edit Enterprise API" : "Register Enterprise API"} open={open} onClose={onClose}>
      <form className="grid gap-4 md:grid-cols-2" onSubmit={submit}>
        <ServiceSelect value={form.service_name} services={services} onChange={(value) => update("service_name", value)} />
        {form.service_name === NEW_SERVICE ? <Field label="New Service Name" value={form.new_service_name} onChange={(value) => update("new_service_name", value)} /> : null}
        <Field label="Operation" value={form.operation} onChange={(value) => update("operation", value)} />
        <Select label="HTTP Method" value={form.method} options={methods} onChange={(value) => update("method", value)} />
        <Field label="Base URL" value={form.base_url} onChange={(value) => update("base_url", value)} />
        <Field label="Path" value={form.path} onChange={(value) => update("path", value)} />
        <Select label="Authentication Type" value={form.authentication_type} options={authTypes} onChange={(value) => update("authentication_type", value)} />
        <Select label="Version" value={form.version} options={versionOptions} extraOption={{ value: NEW_VERSION, label: "Add New Version" }} onChange={(value) => update("version", value)} />
        {form.version === NEW_VERSION ? <Field label="New Version" value={form.new_version} onChange={(value) => update("new_version", value)} /> : null}
        <Select label="Status" value={form.status} options={statusOptions} onChange={(value) => update("status", value)} />
        <NumberField label="Timeout Seconds" value={form.timeout_seconds} min={1} max={120} onChange={(value) => update("timeout_seconds", value)} />
        <NumberField label="Retry Count" value={form.retry_count} min={0} max={5} onChange={(value) => update("retry_count", value)} />
        <Checklist title="Required Policies" values={form.required_policies} options={policies.map((policy) => policy.policy_id)} labels={Object.fromEntries(policies.map((policy) => [policy.policy_id, policy.name]))} onToggle={togglePolicy} />
        <JsonArea label="Authentication Config" value={form.authentication_config} onChange={(value) => update("authentication_config", value)} />
        <JsonArea label="Endpoint Metadata" value={form.endpoint_metadata} onChange={(value) => update("endpoint_metadata", value)} />
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

function NumberField({ label, value, min, max, onChange }) {
  return (
    <label className="min-w-0 text-sm font-medium text-slate-600">
      {label}
      <input type="number" min={min} max={max} className="mt-1 w-full min-w-0 rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={value ?? ""} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}

function ServiceSelect({ value, services, onChange }) {
  const options = value && value !== NEW_SERVICE && !services.includes(value) ? [value, ...services] : services;
  return (
    <label className="min-w-0 text-sm font-medium text-slate-600">
      Service
      <select className="mt-1 w-full min-w-0 rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={value || ""} onChange={(event) => onChange(event.target.value)}>
        {options.map((service) => (
          <option key={service} value={service}>
            {service}
          </option>
        ))}
        <option value={NEW_SERVICE}>Add New Service</option>
      </select>
    </label>
  );
}

function Select({ label, value, options, extraOption, onChange }) {
  const normalizedOptions = value && !options.includes(value) && value !== extraOption?.value ? [value, ...options] : options;
  const hasOptions = normalizedOptions.length > 0 || extraOption;

  return (
    <label className="min-w-0 text-sm font-medium text-slate-600">
      {label}
      <select className="mt-1 w-full min-w-0 rounded-md border border-line px-3 py-2 outline-none focus:border-brand disabled:bg-slate-100 disabled:text-slate-400" value={value || ""} onChange={(event) => onChange(event.target.value)} disabled={!hasOptions}>
        <option value="" disabled>{hasOptions ? "Select" : "No values available"}</option>
        {normalizedOptions.map((option) => (
          <option key={option} value={option}>{option}</option>
        ))}
        {extraOption ? <option value={extraOption.value}>{extraOption.label}</option> : null}
      </select>
    </label>
  );
}

function JsonArea({ label, value, onChange }) {
  return (
    <label className="text-sm font-medium text-slate-600 md:col-span-2">
      {label}
      <textarea rows={4} className="mt-1 w-full min-w-0 rounded-md border border-line px-3 py-2 font-mono text-xs outline-none focus:border-brand" value={value || ""} onChange={(event) => onChange(event.target.value)} />
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
