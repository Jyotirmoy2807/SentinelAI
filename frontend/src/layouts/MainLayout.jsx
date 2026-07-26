import { Bell, Menu, Search, ShieldCheck } from "lucide-react";
import { NavLink, Outlet, useLocation } from "react-router-dom";
import { navigationItems } from "../constants/navigation.js";
import { useUiStore } from "../store/uiStore.js";

const componentScrollRoutes = ["/agents", "/governance", "/enterprise", "/approvals", "/audit"];

export function MainLayout() {
  const sidebarOpen = useUiStore((state) => state.sidebarOpen);
  const toggleSidebar = useUiStore((state) => state.toggleSidebar);
  const location = useLocation();
  const componentScroll = componentScrollRoutes.some((path) => location.pathname.startsWith(path));

  return (
    <div className="h-screen min-w-0 overflow-hidden bg-surface text-ink">
      <aside
        className={`fixed inset-y-0 left-0 z-30 border-r border-line bg-white transition-all duration-200 ${
          sidebarOpen ? "w-72 translate-x-0" : "w-72 -translate-x-full lg:w-20 lg:translate-x-0"
        }`}
      >
        <div className="flex h-16 items-center gap-3 border-b border-line px-5">
          <div className="flex h-10 w-10 items-center justify-center rounded-md bg-brand text-white">
            <ShieldCheck className="h-5 w-5" />
          </div>
          {sidebarOpen ? (
            <div>
              <div className="text-sm font-bold tracking-wide text-ink">SentinelAI</div>
              <div className="text-xs text-slate-500">Governance Console</div>
            </div>
          ) : null}
        </div>
        <nav className="space-y-1 p-3">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition ${
                    isActive ? "bg-blue-50 text-brand" : "text-slate-600 hover:bg-slate-100 hover:text-ink"
                  }`
                }
              >
                <Icon className="h-4 w-4 shrink-0" />
                {sidebarOpen ? <span>{item.label}</span> : null}
              </NavLink>
            );
          })}
        </nav>
      </aside>
      {sidebarOpen ? <button aria-label="Close sidebar overlay" className="fixed inset-0 z-20 bg-ink/20 lg:hidden" onClick={toggleSidebar} /> : null}
      <div className={`flex h-screen min-w-0 flex-col overflow-hidden transition-all ${sidebarOpen ? "lg:pl-72" : "lg:pl-20"}`}>
        <header className="z-20 flex h-16 shrink-0 min-w-0 items-center justify-between gap-3 border-b border-line bg-white/95 px-4 backdrop-blur sm:px-6">
          <div className="flex min-w-0 flex-1 items-center gap-3">
            <button aria-label="Toggle sidebar" className="rounded-md p-2 hover:bg-slate-100" onClick={toggleSidebar}>
              <Menu className="h-5 w-5" />
            </button>
            <div className="hidden min-w-0 max-w-md flex-1 items-center gap-2 rounded-md border border-line bg-slate-50 px-3 py-2 md:flex">
              <Search className="h-4 w-4 text-slate-400" />
              <input className="w-full bg-transparent text-sm outline-none" placeholder="Search governance records" />
            </div>
          </div>
          <div className="flex shrink-0 items-center gap-2 sm:gap-3">
            <span className="hidden rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700 sm:inline-flex">Development</span>
            <button aria-label="Notifications" className="rounded-md p-2 hover:bg-slate-100">
              <Bell className="h-5 w-5" />
            </button>
            <div className="h-9 w-9 rounded-full bg-slate-900 text-center text-sm font-semibold leading-9 text-white">GA</div>
          </div>
        </header>
        <main className={`min-h-0 flex-1 overflow-x-hidden ${componentScroll ? "overflow-hidden" : "overflow-y-auto"}`}>
          <div className={`mx-auto box-border min-w-0 max-w-[1500px] px-3 py-4 sm:px-6 sm:py-6 ${componentScroll ? "h-full" : ""}`}>
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
