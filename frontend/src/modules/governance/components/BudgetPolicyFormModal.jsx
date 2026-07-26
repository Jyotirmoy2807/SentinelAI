import { useEffect, useMemo, useState } from "react";
import { Button } from "../../../components/button/Button.jsx";
import { Modal } from "../../../components/modal/Modal.jsx";

const EMPTY_LOOKUP_LIST = [];

export function BudgetPolicyFormModal({ open, onClose, policy, lookups, onSubmit, pending }) {
  const departments = lookups?.departments ?? EMPTY_LOOKUP_LIST;
  const statuses = lookups?.budget_statuses ?? EMPTY_LOOKUP_LIST;
  const defaults = useMemo(
    () => ({
      name: "",
      department: departments[0] || "",
      daily_limit: 0,
      monthly_limit: 0,
      transaction_limit: 0,
      approval_threshold: 0,
      spent_today: 0,
      spent_month: 0,
      status: statuses[0] || ""
    }),
    [departments, statuses]
  );
  const [form, setForm] = useState(defaults);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!open) return;
    setForm(policy || defaults);
    setError("");
  }, [defaults, open, policy]);

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function submit(event) {
    event.preventDefault();
    if (!form.name || !form.department || !form.status) {
      setError("Name, department, and status are required.");
      return;
    }
    const payload = {
      ...form,
      daily_limit: Number(form.daily_limit),
      monthly_limit: Number(form.monthly_limit),
      transaction_limit: Number(form.transaction_limit),
      approval_threshold: Number(form.approval_threshold),
      spent_today: Number(form.spent_today),
      spent_month: Number(form.spent_month)
    };
    if (payload.approval_threshold > payload.transaction_limit) {
      setError("Approval threshold cannot exceed transaction limit.");
      return;
    }
    setError("");
    onSubmit(payload, setError);
  }

  return (
    <Modal title={policy ? "Edit Budget Policy" : "Create Budget Policy"} open={open} onClose={onClose}>
      <form className="grid gap-4 md:grid-cols-2" onSubmit={submit}>
        <Field label="Name" value={form.name} onChange={(value) => update("name", value)} />
        <Select label="Department" value={form.department} options={departments} onChange={(value) => update("department", value)} />
        <NumberField label="Daily Limit" value={form.daily_limit} onChange={(value) => update("daily_limit", value)} />
        <NumberField label="Monthly Limit" value={form.monthly_limit} onChange={(value) => update("monthly_limit", value)} />
        <NumberField label="Transaction Limit" value={form.transaction_limit} onChange={(value) => update("transaction_limit", value)} />
        <NumberField label="Approval Threshold" value={form.approval_threshold} onChange={(value) => update("approval_threshold", value)} />
        <NumberField label="Spent Today" value={form.spent_today} onChange={(value) => update("spent_today", value)} />
        <NumberField label="Spent Month" value={form.spent_month} onChange={(value) => update("spent_month", value)} />
        <Select label="Status" value={form.status} options={statuses} onChange={(value) => update("status", value)} />
        {error ? <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-danger md:col-span-2">{formatError(error)}</div> : null}
        <div className="flex justify-end gap-2 md:col-span-2">
          <Button type="button" tone="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" disabled={pending}>
            Save Budget Policy
          </Button>
        </div>
      </form>
    </Modal>
  );
}

function Field({ label, value, onChange }) {
  return (
    <label className="min-w-0 text-sm font-medium text-slate-600">
      {label}
      <input className="mt-1 w-full min-w-0 rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={value ?? ""} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}

function NumberField(props) {
  return (
    <label className="min-w-0 text-sm font-medium text-slate-600">
      {props.label}
      <input type="number" min="0" className="mt-1 w-full min-w-0 rounded-md border border-line px-3 py-2 outline-none focus:border-brand" value={props.value ?? 0} onChange={(event) => props.onChange(event.target.value)} />
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

function formatError(error) {
  if (Array.isArray(error)) return error.map((item) => item.msg || item).join(", ");
  return String(error);
}
