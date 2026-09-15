export type HealthResponse = {
  status: string;
  db: "ok" | "fail";
};

export type SensorDto = {
  id: string;
  device_type: string;
  display_name: string | null;
  default_config: Record<string, unknown>;
};

export type SensorType = "moisture" | "light";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, options);

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function fetchHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/api/health");
}

export function fetchSensors(): Promise<SensorDto[]> {
  return request<SensorDto[]>("/api/sensors");
}

export function createSensor(
  type: SensorType,
  displayName?: string,
): Promise<SensorDto> {
  return request<SensorDto>("/api/sensors", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      type,
      display_name: displayName || null,
    }),
  });
}