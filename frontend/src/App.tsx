import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppLayout } from "./components/AppLayout";
import { DashboardPage } from "./pages/DashboardPage";

function HomePage() {
  return (
    <div className="rounded-lg border bg-white p-6">
      <h2 className="mb-2 text-xl font-bold text-emerald-600">
        Smart Greenhouse Dashboard
      </h2>
      <p className="text-slate-700">
        Welcome to the greenhouse control system. Use the navigation to open the
        dashboard.
      </p>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<HomePage />} />
          <Route path="dashboard" element={<DashboardPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}