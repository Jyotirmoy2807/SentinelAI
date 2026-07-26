export function Tabs({ tabs, active, onChange }) {
  return (
    <div className="flex flex-wrap gap-2 border-b border-line">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className={`border-b-2 px-3 py-2 text-sm font-medium ${active === tab.id ? "border-brand text-brand" : "border-transparent text-slate-500 hover:text-ink"}`}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
