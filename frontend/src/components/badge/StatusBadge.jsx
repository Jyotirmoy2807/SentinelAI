export function StatusBadge({ status }) {
  const normalized = String(status || "UNKNOWN").toUpperCase();
  const tones = {
    ACTIVE: "bg-emerald-50 text-emerald-700 ring-emerald-200",
    HEALTHY: "bg-emerald-50 text-emerald-700 ring-emerald-200",
    DEPLOYED: "bg-emerald-50 text-emerald-700 ring-emerald-200",
    PASSED: "bg-emerald-50 text-emerald-700 ring-emerald-200",
    ALLOW: "bg-emerald-50 text-emerald-700 ring-emerald-200",
    APPROVED: "bg-emerald-50 text-emerald-700 ring-emerald-200",
    SUCCESS: "bg-emerald-50 text-emerald-700 ring-emerald-200",
    COMPLETED: "bg-emerald-50 text-emerald-700 ring-emerald-200",
    RUNNING: "bg-blue-50 text-blue-700 ring-blue-200",
    PENDING: "bg-amber-50 text-amber-700 ring-amber-200",
    PENDING_APPROVAL: "bg-amber-50 text-amber-700 ring-amber-200",
    REQUIRE_APPROVAL: "bg-amber-50 text-amber-700 ring-amber-200",
    WAITING_APPROVAL: "bg-amber-50 text-amber-700 ring-amber-200",
    DENY: "bg-red-50 text-red-700 ring-red-200",
    DENIED: "bg-red-50 text-red-700 ring-red-200",
    REJECTED: "bg-red-50 text-red-700 ring-red-200",
    BLOCKED: "bg-red-50 text-red-700 ring-red-200",
    SUSPENDED: "bg-slate-100 text-slate-600 ring-slate-200",
    INACTIVE: "bg-slate-100 text-slate-600 ring-slate-200",
    MAINTENANCE: "bg-purple-50 text-purple-700 ring-purple-200",
    FAILED: "bg-red-50 text-red-700 ring-red-200",
    ERROR: "bg-red-50 text-red-700 ring-red-200",
    SIMULATED: "bg-cyan-50 text-cyan-700 ring-cyan-200"
  };
  return (
    <span className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-semibold ring-1 ${tones[normalized] || "bg-slate-100 text-slate-600 ring-slate-200"}`}>
      {normalized.replaceAll("_", " ")}
    </span>
  );
}
