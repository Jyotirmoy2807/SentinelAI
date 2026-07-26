import { StatusBadge } from "../badge/StatusBadge.jsx";
import { formatDate } from "../../utils/format.js";

export function Timeline({ events }) {
  return (
    <ol className="space-y-3">
      {events?.length ? (
        events.map((event, index) => (
          <li key={`${event.node}-${event.timestamp}-${index}`} className="rounded-lg border border-line bg-white p-3">
            <div className="flex items-center justify-between gap-3">
              <span className="text-sm font-semibold text-ink">{event.node?.replaceAll("_", " ")}</span>
              <StatusBadge status={event.status} />
            </div>
            <div className="mt-2 flex items-center justify-between text-xs text-slate-500">
              <span>{formatDate(event.timestamp)}</span>
              <span>{event.duration_ms || 0} ms</span>
            </div>
          </li>
        ))
      ) : (
        <li className="rounded-lg border border-dashed border-line bg-white p-4 text-sm text-slate-500">No execution events yet</li>
      )}
    </ol>
  );
}
