import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { MainLayout } from "../layouts/MainLayout.jsx";
import { LandingPage } from "../pages/LandingPage.jsx";
import { DashboardPage } from "../modules/dashboard/pages/DashboardPage.jsx";
import { AgentsPage } from "../modules/agents/pages/AgentsPage.jsx";
import { GovernanceManagementPage } from "../modules/governance/pages/GovernanceManagementPage.jsx";
import { EnterpriseRegistryPage } from "../modules/enterprise/pages/EnterpriseRegistryPage.jsx";
import { LiveExecutionPage } from "../modules/execution/pages/LiveExecutionPage.jsx";
import { ApprovalCenterPage } from "../modules/approvals/pages/ApprovalCenterPage.jsx";
import { AuditPage } from "../modules/audit/pages/AuditPage.jsx";
import { SettingsPage } from "../modules/settings/pages/SettingsPage.jsx";
import { SimulationLabPage } from "../modules/simulation/pages/SimulationLabPage.jsx";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1
    }
  }
});

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<MainLayout />}>
            <Route path="/" element={<LandingPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/agents" element={<AgentsPage />} />
            <Route path="/governance" element={<GovernanceManagementPage />} />
            <Route path="/enterprise" element={<EnterpriseRegistryPage />} />
            <Route path="/live" element={<LiveExecutionPage />} />
            <Route path="/approvals" element={<ApprovalCenterPage />} />
            <Route path="/audit" element={<AuditPage />} />
            <Route path="/simulation" element={<SimulationLabPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
