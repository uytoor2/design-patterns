import { useEffect, useState } from "react";
import { fetchHealth } from "../services/api";
import type { HealthResponse } from "../services/api";
type Status = "ok" | "degraded" | "error";

export function HealthStatus() {
  const [status, setStatus] = useState<Status>("error");
  const [db, setDb] = useState<"ok" | "fail">("fail");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const data: HealthResponse = await fetchHealth();
        if (cancelled) return;
        setStatus(data.status === "ok" ? "ok" : "degraded");
        setDb(data.db);
      } catch {
        if (cancelled) return;
        setStatus("error");
        setDb("fail");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();

    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return (
      <span className="rounded-full bg-slate-200 px-3 py-1 text-sm text-slate-600">
        Checking…
      </span>
    );
  }

  const ring =
    status === "ok"
      ? "ring-emerald-500 text-emerald-700 bg-emerald-50"
      : status === "degraded"
      ? "ring-amber-500 text-amber-700 bg-amber-50"
      : "ring-red-500 text-red-700 bg-red-50";

  return (
    <span
      className={`rounded-full px-3 py-1 text-sm ring-2 ${ring}`}
      title={`API: ${status} · DB: ${db}`}
    >
      API: {status} · DB: {db}
    </span>
  );
}