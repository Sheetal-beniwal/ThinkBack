/**
 * API utility layer — all backend communication lives here.
 * Components should import these functions; never fetch() directly from UI.
 *
 * Requests go to /api/* which Next.js proxies to the FastAPI backend
 * (configured in next.config.ts). This avoids CORS entirely since
 * the browser always talks to the same origin (localhost:3000).
 */

import type {
  AskRequest,
  AskResponse,
  SearchRequest,
  SearchResponse,
} from "@/types";

// Use relative /api path so requests go through the Next.js proxy.
// The proxy rewrites /api/* → NEXT_PUBLIC_API_URL/* (see next.config.ts).
const API_BASE_URL = "/api";

// ─── Generic fetch wrapper ────────────────────────────────────────────────────

async function apiFetch<T>(
  endpoint: string,
  body: unknown,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const text = await response.text().catch(() => "Unknown error");
    throw new Error(
      `API error ${response.status}: ${text}`,
    );
  }

  return response.json() as Promise<T>;
}

// ─── Public API functions ─────────────────────────────────────────────────────

/**
 * Semantic search across solved LeetCode problems.
 */
export async function searchProblems(
  request: SearchRequest,
): Promise<SearchResponse> {
  return apiFetch<SearchResponse>("/search", request);
}

/**
 * Ask the RAG-powered AI assistant a question about solved problems.
 */
export async function askAI(request: AskRequest): Promise<AskResponse> {
  return apiFetch<AskResponse>("/ask", request);
}
