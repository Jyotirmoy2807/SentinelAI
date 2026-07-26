import { ChevronDown, ChevronUp, Search } from "lucide-react";
import { useMemo, useState } from "react";

export function DataTable({ columns, rows, loading, empty = "No records", onRowClick, initialSortKey, initialDirection }) {
  const [query, setQuery] = useState("");
  const [sortKey, setSortKey] = useState(initialSortKey !== undefined ? initialSortKey : columns[0]?.key);
  const [direction, setDirection] = useState(initialDirection || "asc");
  const [page, setPage] = useState(1);
  const pageSize = 8;

  const visibleRows = useMemo(() => {
    const filtered = rows.filter((row) => JSON.stringify(row).toLowerCase().includes(query.toLowerCase()));
    if (!sortKey) return filtered;
    const sorted = [...filtered].sort((a, b) => {
      const valA = a[sortKey];
      const valB = b[sortKey];
      
      // Compare dates if valid date inputs or strings
      const timeA = typeof valA === "string" && !isNaN(Date.parse(valA)) ? new Date(valA).getTime() : null;
      const timeB = typeof valB === "string" && !isNaN(Date.parse(valB)) ? new Date(valB).getTime() : null;

      if (timeA !== null && timeB !== null) {
        return direction === "asc" ? timeA - timeB : timeB - timeA;
      }

      const first = String(valA ?? "");
      const second = String(valB ?? "");
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
    <div className="min-w-0 overflow-x-hidden">
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
      <div className="rounded-lg border border-line bg-white md:hidden">
        {loading ? (
          <div className="px-4 py-8 text-center text-sm text-slate-500">Loading records</div>
        ) : pageRows.length ? (
          <div className="divide-y divide-line">
            {pageRows.map((row) => (
              <div
                key={row.id || row.request_id || row.approval_id || row.policy_id || JSON.stringify(row)}
                onClick={() => onRowClick?.(row)}
                className={`block w-full min-w-0 px-4 py-3 text-left ${onRowClick ? "cursor-pointer hover:bg-slate-50" : ""}`}
              >
                <div className="grid gap-2">
                  {columns.map((column) => (
                    <div key={column.key} className="min-w-0">
                      <div className="text-[11px] font-semibold uppercase tracking-wide text-slate-400">{column.header}</div>
                      <div className="mt-1 break-words text-sm text-slate-700">{column.render ? column.render(row) : row[column.key]}</div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="px-4 py-8 text-center text-sm text-slate-500">{empty}</div>
        )}
      </div>
      <div className="hidden overflow-x-hidden rounded-lg border border-line bg-white md:block">
        <table className="w-full table-fixed divide-y divide-line text-sm">
          <colgroup>
            {columns.map((column) => (
              <col key={column.key} style={column.width ? { width: column.width } : undefined} />
            ))}
          </colgroup>
          <thead className="bg-slate-50">
            <tr>
              {columns.map((column) => (
                <th key={column.key} className={`break-words px-3 py-3 text-left font-semibold text-slate-600 ${column.headerClassName || ""}`}>
                  <button className="inline-flex max-w-full items-center gap-1 text-left" onClick={() => toggleSort(column.key)}>
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
                    <td key={column.key} className={`break-words px-3 py-3 align-top text-slate-700 ${column.cellClassName || ""}`}>
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
        <div className="flex shrink-0 gap-2">
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
