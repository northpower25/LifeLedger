import { invoke, isTauri } from "@tauri-apps/api/core";

export type FhirResource = {
  resourceType: string;
  id: string;
  [key: string]: unknown;
};

const API = "http://127.0.0.1:8765/api/v1";

export async function api<T>(
  path: string,
  options: RequestInit = {},
  token?: string,
): Promise<T> {
  const headers = new Headers(options.headers);
  if (options.body) headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (isTauri()) {
    const reply = await invoke<{ status: number; body: string }>("api_request", {
      request: {
        method: options.method ?? "GET",
        path: `/api/v1${path}`,
        body: typeof options.body === "string" ? options.body : undefined,
        authorization: headers.get("Authorization") ?? undefined,
      },
    });
    if (reply.status < 200 || reply.status >= 300) {
      const body = JSON.parse(reply.body || "{}");
      throw new Error(body?.detail ?? `request_failed_${reply.status}`);
    }
    if (reply.status === 204) return undefined as T;
    return JSON.parse(reply.body) as T;
  }

  const response = await fetch(`${API}${path}`, { ...options, headers });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? `request_failed_${response.status}`);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}
