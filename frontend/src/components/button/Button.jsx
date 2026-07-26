export function Button({ children, tone = "primary", className = "", type = "button", ...props }) {
  const tones = {
    primary: "bg-brand text-white hover:bg-blue-700 border-brand",
    secondary: "bg-white text-ink hover:bg-slate-50 border-line",
    danger: "bg-danger text-white hover:bg-red-800 border-danger",
    ghost: "bg-transparent text-slate-700 hover:bg-slate-100 border-transparent"
  };
  return (
    <button
      type={type}
      className={`inline-flex h-10 items-center justify-center gap-2 rounded-md border px-3 text-sm font-medium transition disabled:cursor-not-allowed disabled:opacity-50 ${tones[tone]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
