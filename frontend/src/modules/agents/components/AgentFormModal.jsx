import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "../../../components/button/Button.jsx";
import { Modal } from "../../../components/modal/Modal.jsx";

const schema = z.object({
  passport_id: z.string().min(3),
  name: z.string().min(2),
  owner: z.string().min(2),
  department: z.string().min(2),
  version: z.string().min(1),
  status: z.string().min(1),
  trust_score: z.coerce.number().min(0).max(100),
  risk_tier: z.string().min(1),
  budget_profile: z.string().min(1),
  reputation: z.coerce.number().min(0).max(100),
  allowed_apis: z.string(),
  allowed_operations: z.string(),
  policy_groups: z.string()
});

const defaults = {
  passport_id: "",
  name: "",
  owner: "",
  department: "Finance",
  version: "1.0.0",
  status: "ACTIVE",
  trust_score: 80,
  risk_tier: "LOW",
  budget_profile: "Finance-Controlled",
  reputation: 90,
  allowed_apis: "Invoice Service",
  allowed_operations: "create_invoice",
  policy_groups: "default"
};

export function AgentFormModal({ open, onClose, agent, onSubmit }) {
  const { register, handleSubmit, reset, setError, formState } = useForm({ defaultValues: defaults });

  useEffect(() => {
    reset(
      agent
        ? {
            ...agent,
            allowed_apis: agent.allowed_apis?.join(", ") || "",
            allowed_operations: agent.allowed_operations?.join(", ") || "",
            policy_groups: agent.policy_groups?.join(", ") || ""
          }
        : defaults
    );
  }, [agent, reset, open]);

  function submit(values) {
    const result = schema.safeParse(values);
    if (!result.success) {
      result.error.issues.forEach((issue) => setError(issue.path[0], { message: issue.message }));
      return;
    }
    const payload = {
      ...result.data,
      allowed_apis: splitList(result.data.allowed_apis),
      allowed_operations: splitList(result.data.allowed_operations),
      policy_groups: splitList(result.data.policy_groups)
    };
    onSubmit(payload);
  }

  return (
    <Modal title={agent ? "Edit Agent" : "Register Agent"} open={open} onClose={onClose}>
      <form className="grid gap-4 md:grid-cols-2" onSubmit={handleSubmit(submit)}>
        {[
          ["passport_id", "Passport ID"],
          ["name", "Agent Name"],
          ["owner", "Owner"],
          ["department", "Department"],
          ["version", "Version"],
          ["budget_profile", "Budget Profile"]
        ].map(([name, label]) => (
          <label key={name} className="text-sm font-medium text-slate-600">
            {label}
            <input className="mt-1 w-full rounded-md border border-line px-3 py-2 outline-none focus:border-brand" {...register(name)} disabled={agent && name === "passport_id"} />
            {formState.errors[name] ? <span className="text-xs text-danger">{formState.errors[name].message}</span> : null}
          </label>
        ))}
        <label className="text-sm font-medium text-slate-600">
          Status
          <select className="mt-1 w-full rounded-md border border-line px-3 py-2 outline-none focus:border-brand" {...register("status")}>
            <option>ACTIVE</option>
            <option>SUSPENDED</option>
            <option>BLOCKED</option>
          </select>
        </label>
        <label className="text-sm font-medium text-slate-600">
          Risk Tier
          <select className="mt-1 w-full rounded-md border border-line px-3 py-2 outline-none focus:border-brand" {...register("risk_tier")}>
            <option>LOW</option>
            <option>MEDIUM</option>
            <option>HIGH</option>
          </select>
        </label>
        <label className="text-sm font-medium text-slate-600">
          Trust Score
          <input type="number" className="mt-1 w-full rounded-md border border-line px-3 py-2 outline-none focus:border-brand" {...register("trust_score")} />
        </label>
        <label className="text-sm font-medium text-slate-600">
          Reputation
          <input type="number" className="mt-1 w-full rounded-md border border-line px-3 py-2 outline-none focus:border-brand" {...register("reputation")} />
        </label>
        {[
          ["allowed_apis", "Allowed APIs"],
          ["allowed_operations", "Allowed Operations"],
          ["policy_groups", "Policy Groups"]
        ].map(([name, label]) => (
          <label key={name} className="text-sm font-medium text-slate-600 md:col-span-2">
            {label}
            <input className="mt-1 w-full rounded-md border border-line px-3 py-2 outline-none focus:border-brand" {...register(name)} />
          </label>
        ))}
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

function splitList(value) {
  return String(value || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}
