import { Outlet, Link } from "react-router-dom";
import { HealthStatus } from "./HealthStatus";

export function AppLayout() {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
          <div className="flex items-center gap-4">
            <h1 className="text-lg font-bold text-emerald-600">
              Smart Greenhouse
            </h1>
            <nav className="flex items-center gap-3 text-sm">
              <Link className="text-slate-600 hover:text-slate-900" to="/">
                Home
              </Link>
              <Link className="text-slate-600 hover:text-slate-900" to="/dashboard">
                Dashboard
              </Link>
            </nav>
          </div>
          <HealthStatus />
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-6">
        <Outlet />
      </main>
    </div>
  );
}