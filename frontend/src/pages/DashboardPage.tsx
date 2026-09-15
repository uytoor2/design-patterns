import { SensorList } from "../features/sensors/SensorList";

export function DashboardPage() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <SensorList />

      <section id="config" className="rounded-lg border bg-white p-4">
        <h2 className="mb-2 text-lg font-semibold">Configuration</h2>
        <p className="text-sm text-slate-600">
          Placeholder for configuration UI.
        </p>
      </section>

      <section id="automation" className="rounded-lg border bg-white p-4">
        <h2 className="mb-2 text-lg font-semibold">Automation</h2>
        <p className="text-sm text-slate-600">
          Placeholder for automation rules.
        </p>
      </section>

      <section id="overview" className="rounded-lg border bg-white p-4">
        <h2 className="mb-2 text-lg font-semibold">Overview</h2>
        <p className="text-sm text-slate-600">
          Placeholder for overview data.
        </p>
      </section>

      <section id="controls" className="rounded-lg border bg-white p-4">
        <h2 className="mb-2 text-lg font-semibold">Controls</h2>
        <p className="text-sm text-slate-600">
          Placeholder for device controls.
        </p>
      </section>

      <section id="events" className="rounded-lg border bg-white p-4">
        <h2 className="mb-2 text-lg font-semibold">Events</h2>
        <p className="text-sm text-slate-600">
          Placeholder for event feed.
        </p>
      </section>
    </div>
  );
}