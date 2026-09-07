export type HealthResponse = { status: string; db: "ok" | "fail" };

const API_BASE = "/api";

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  return response.json();
}