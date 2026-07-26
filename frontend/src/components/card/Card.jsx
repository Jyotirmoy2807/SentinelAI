export function Card({ children, className = "" }) {
  return <section className={`rounded-lg border border-line bg-white shadow-sm ${className}`}>{children}</section>;
}

export function CardHeader({ title, action, children }) {
  return (
    <div className="flex items-start justify-between gap-4 border-b border-line px-5 py-4">
      <div>
        <h2 className="text-base font-semibold text-ink">{title}</h2>
        {children ? <p className="mt-1 text-sm text-slate-500">{children}</p> : null}
      </div>
      {action}
    </div>
  );
}

export function CardBody({ children, className = "" }) {
  return <div className={`p-5 ${className}`}>{children}</div>;
}
