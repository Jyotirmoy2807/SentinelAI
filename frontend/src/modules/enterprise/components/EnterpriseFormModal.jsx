import { useEffect, useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Modal } from "../../../components/modal/Modal.jsx";

const defaults = {
  service_name: "",
  adapter: "RefundAdapter",
  version: "1.0",
  status: "ACTIVE",
  permissions: "",
  required_policies: "",
  allowed_agents: "",
  endpoint_metadata: "{\"owner\":\"Platform\",\"sla\":\"250ms mock\"}"
};

export function EnterpriseFormModal({ open, onClose, item, onSubmit }) {
  const [form, setForm] = useState(defaults);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!open) return;
    setForm(
      item
        ? {
            ...item,
            permissions: item.permissions?.join(", ") || "",
            required_policies: item.required_policies?.join(", ") || "",
            allowed_agents: item.allowed_agents?.join(", ") || "",
            endpoint_metadata: JSON.stringify(item.endpoint_metadata || {}, null, 2)
          }
        : defaults
    );
    setError("");
  }, [item, open]);

  function update(key, value) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  function submit(event) {
    event.preventDefault();
    try {
      onSubmit({
        ...form,
        permissions: split(form.permissions),
        required_policies: split(form.required_policies),
        allowed_agents: split(form.allowed_agents),
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
        <label className="text-sm font-medium text-slate-600">
          Adapter
          <select className="mt-1 w-full rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={form.adapter} onChange={(event) => update("adapter", event.target.value)}>
            <option>RefundAdapter</option>
            <option>MerchantAdapter</option>
            <option>PaymentAdapter</option>
            <option>BookingAdapter</option>
            <option>InvoiceAdapter</option>
          </select>
        </label>
        <Field label="Version" value={form.version} onChange={(value) => update("version", value)} />
        <label className="text-sm font-medium text-slate-600">
          Status
          <select className="mt-1 w-full rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={form.status} onChange={(event) => update("status", event.target.value)}>
            <option>ACTIVE</option>
            <option>INACTIVE</option>
            <option>MAINTENANCE</option>
          </select>
        </label>
        <Field label="Permissions" value={form.permissions} onChange={(value) => update("permissions", value)} wide />
        <Field label="Required Policies" value={form.required_policies} onChange={(value) => update("required_policies", value)} wide />
        <Field label="Allowed Agents" value={form.allowed_agents} onChange={(value) => update("allowed_agents", value)} wide />
        <label className="text-sm font-medium text-slate-600 md:col-span-2">
          Endpoint Metadata
          <textarea rows={4} className="mt-1 w-full rounded-md border border-line px-3 py-2 font-mono text-xs outline-none focus:border-brand" value={form.endpoint_metadata} onChange={(event) => update("endpoint_metadata", event.target.value)} />
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

function Field({ label, value, onChange, wide }) {
  return (
    <label className={`text-sm font-medium text-slate-600 ${wide ? "md:col-span-2" : ""}`}>
      {label}
      <input className="mt-1 w-full rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={value || ""} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}

function split(value) {
  return String(value || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}
