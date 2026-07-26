import { Bot, ClipboardCheck, Database, FlaskConical, Gauge, Home, Settings, ShieldCheck } from "lucide-react";

export const navigationItems = [
  { label: "Dashboard", path: "/dashboard", icon: Gauge },
  { label: "Agent Management", path: "/agents", icon: Bot },
  { label: "Governance Management", path: "/governance", icon: ShieldCheck },
  { label: "Enterprise API Registry", path: "/enterprise", icon: Database },
  { label: "Human Approval", path: "/approvals", icon: ClipboardCheck },
  { label: "Audit & Explainability", path: "/audit", icon: Home },
  { label: "Simulation Lab", path: "/simulation", icon: FlaskConical },
  { label: "Settings", path: "/settings", icon: Settings }
];
