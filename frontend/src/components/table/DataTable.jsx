import { ChevronDown, ChevronUp, Search } from "lucide-react";
import { useMemo, useState } from "react";

export function DataTable({ columns, rows, loading, empty = "No records", onRowClick }) {
  const [query, setQuery] = useState("");
  const [sortKey, setSortKey] = useState(columns[0]?.key);
  const [direction, setDirection] = useState("asc");
  const [page, setPage] = useState(1);
  const pageSize = 8;

  const visibleRows = useMemo(() => {
    const filtered = rows.filter((row) => JSON.stringify(row).toLowerCase().includes(query.toLowerCase()));
    const sorted = [...filtered].sort((a, b) => {
      const first = String(a[sortKey] ?? "");
      const second = String(b[sortKey] ?? "");
      return direction === "asc" ? first.localeCompare(second) : second.localeCompare(first);
    });
    return sorted;
  }, [rows, query, sortKey, direction]);

  const pageRows = visibleRows.slice((page - 1) * pageSize, page * pageSize);
  const pageCount = Math.max(Math.ceil(visibleRows.length / pageSize), 1);

  function toggleSort(key) {
    if (sortKey === key) {
      setDirection(direction === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setDirection("asc");
    }
  }

  return (
    <div>
      <div className="mb-3 flex items-center gap-2 rounded-md border border-line bg-white px-3 py-2">
        <Search className="h-4 w-4 text-slate-400" />
        <input
          value={query}
          onChange={(event) => {
            setQuery(event.target.value);
            setPage(1);
          }}
          className="w-full bg-transparent text-sm outline-none"
          placeholder="Search"
        />
      </div>
      <div className="overflow-hidden rounded-lg border border-line bg-white">
        <table className="min-w-full divide-y divide-line text-sm">
          <thead className="bg-slate-50">
            <tr>
              {columns.map((column) => (
                <th key={column.key} className="px-4 py-3 text-left font-semibold text-slate-600">
                  <button className="inline-flex items-center gap-1" onClick={() => toggleSort(column.key)}>
                    {column.header}
                    {sortKey === column.key ? direction === "asc" ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" /> : null}
                  </button>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-line bg-white">
            {loading ? (
              <tr>
                <td className="px-4 py-8 text-center text-slate-500" colSpan={columns.length}>
                  Loading records
                </td>
              </tr>
            ) : pageRows.length ? (
              pageRows.map((row) => (
                <tr
                  key={row.id || row.request_id || row.approval_id || row.policy_id || JSON.stringify(row)}
                  onClick={() => onRowClick?.(row)}
                  className={onRowClick ? "cursor-pointer hover:bg-slate-50" : ""}
                >
                  {columns.map((column) => (
                    <td key={column.key} className="px-4 py-3 text-slate-700">
                      {column.render ? column.render(row) : row[column.key]}
                    </td>
                  ))}
                </tr>
              ))
            ) : (
              <tr>
                <td className="px-4 py-8 text-center text-slate-500" colSpan={columns.length}>
                  {empty}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <div className="mt-3 flex items-center justify-between text-sm text-slate-500">
        <span>
          Page {page} of {pageCount}
        </span>
        <div className="flex gap-2">
          <button className="rounded border border-line px-3 py-1 disabled:opacity-40" disabled={page === 1} onClick={() => setPage((value) => value - 1)}>
            Previous
          </button>
          <button className="rounded border border-line px-3 py-1 disabled:opacity-40" disabled={page === pageCount} onClick={() => setPage((value) => value + 1)}>
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
