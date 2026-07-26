export function formatDate(value) {
  if (!value) return "Never";
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  }).format(new Date(value));
}

export function formatNumber(value, suffix = "") {
  if (value === undefined || value === null) return "0";
  return `${new Intl.NumberFormat().format(value)}${suffix}`;
}

export function titleize(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (character) => character.toUpperCase());
}
