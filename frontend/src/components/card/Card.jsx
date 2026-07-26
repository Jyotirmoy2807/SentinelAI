export function Card({ children, className = "" }) {
  return <section className={`min-w-0 overflow-hidden rounded-lg border border-line bg-white shadow-sm ${className}`}>{children}</section>;
}

export function CardHeader({ title, action, children }) {
  return (
    <div className="flex flex-wrap items-start justify-between gap-3 border-b border-line px-4 py-4 sm:px-5">
      <div className="min-w-0">
        <h2 className="break-words text-base font-semibold text-ink">{title}</h2>
        {children ? <p className="mt-1 text-sm text-slate-500">{children}</p> : null}
      </div>
      {action ? <div className="shrink-0">{action}</div> : null}
    </div>
  );
}

export function CardBody({ children, className = "" }) {
  return <div className={`min-w-0 p-4 sm:p-5 ${className}`}>{children}</div>;
}
