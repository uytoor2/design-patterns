import { useCallback, useEffect, useState } from "react";

import {
  createSensor,
  fetchSensors,
  type SensorDto,
  type SensorType,
} from "../../services/api";

function formatConfig(config: Record<string, unknown>): string {
  return Object.entries(config)
    .map(([key, value]) => `${key}: ${String(value)}`)
    .join(" · ");
}

function friendlyType(deviceType: string): string {
  return deviceType.replaceAll("_", " ");
}

export function SensorList() {
  const [sensors, setSensors] = useState<SensorDto[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [creatingType, setCreatingType] = useState<SensorType | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadSensors = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await fetchSensors();
      setSensors(data);
    } catch (requestError) {
      const message =
        requestError instanceof Error
          ? requestError.message
          : "Could not load sensors.";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadSensors();
  }, [loadSensors]);

  async function handleCreate(type: SensorType) {
    setCreatingType(type);
    setError(null);

    try {
      const createdSensor = await createSensor(type);
      setSensors((currentSensors) => [createdSensor, ...currentSensors]);
    } catch (requestError) {
      const message =
        requestError instanceof Error
          ? requestError.message
          : "Could not create the sensor.";
      setError(message);
    } finally {
      setCreatingType(null);
    }
  }

  return (
    <section
      id="sensors"
      className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm"
    >
      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">Sensors</h2>
          <p className="text-sm text-slate-600">
            Create and review greenhouse monitoring devices.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => void handleCreate("moisture")}
            disabled={creatingType !== null}
            className="rounded-md bg-emerald-600 px-3 py-2 text-sm font-medium text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-slate-400"
          >
            {creatingType === "moisture"
              ? "Adding…"
              : "Add moisture sensor"}
          </button>

          <button
            type="button"
            onClick={() => void handleCreate("light")}
            disabled={creatingType !== null}
            className="rounded-md bg-amber-500 px-3 py-2 text-sm font-medium text-white transition hover:bg-amber-600 disabled:cursor-not-allowed disabled:bg-slate-400"
          >
            {creatingType === "light" ? "Adding…" : "Add light sensor"}
          </button>
        </div>
      </div>

      {error && (
        <div
          role="alert"
          className="mb-4 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
        >
          <div className="flex items-center justify-between gap-3">
            <span>{error}</span>
            <button
              type="button"
              onClick={() => void loadSensors()}
              className="font-medium underline"
            >
              Retry
            </button>
          </div>
        </div>
      )}

      {isLoading ? (
        <p className="text-sm text-slate-600">Loading sensors…</p>
      ) : sensors.length === 0 ? (
        <div className="rounded-md border border-dashed border-slate-300 p-4 text-sm text-slate-600">
          No sensors have been created yet. Add a moisture or light sensor to
          begin.
        </div>
      ) : (
        <ul className="space-y-3">
          {sensors.map((sensor) => (
            <li
              key={sensor.id}
              className="rounded-md border border-slate-200 bg-slate-50 p-3"
            >
              <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h3 className="font-medium text-slate-900">
                    {sensor.display_name || "Unnamed sensor"}
                  </h3>
                  <p className="text-sm capitalize text-slate-600">
                    {friendlyType(sensor.device_type)}
                  </p>
                </div>

                <span className="text-xs text-slate-500">{sensor.id}</span>
              </div>

              <p className="mt-2 text-xs text-slate-600">
                {formatConfig(sensor.default_config)}
              </p>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}