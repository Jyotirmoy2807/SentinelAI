import {
  Activity,
  Bot,
  ClipboardCheck,
  Database,
  FlaskConical,
  Gauge,
  Home,
  LandPlot,
  Settings,
  ShieldCheck
} from "lucide-react";

export const navigationItems = [
  { label: "Landing", path: "/", icon: LandPlot },
  { label: "Dashboard", path: "/dashboard", icon: Gauge },
  { label: "Agent Management", path: "/agents", icon: Bot },
  { label: "Governance Management", path: "/governance", icon: ShieldCheck },
  { label: "Enterprise API Registry", path: "/enterprise", icon: Database },
  { label: "Live Governance", path: "/live", icon: Activity },
  { label: "Human Approval", path: "/approvals", icon: ClipboardCheck },
  { label: "Audit & Explainability", path: "/audit", icon: Home },
  { label: "Simulation Lab", path: "/simulation", icon: FlaskConical },
  { label: "Settings", path: "/settings", icon: Settings }
];
