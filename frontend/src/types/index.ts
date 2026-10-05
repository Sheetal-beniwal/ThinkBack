// Shared TypeScript interfaces for all API request/response types.
// Add new types here as the application grows.

export interface SearchRequest {
  query: string;
  top_k?: number;
  difficulty?: "Easy" | "Medium" | "Hard" | null;
  pattern?: string | null;
}

export interface Problem {
  score: number;
  title: string;
  difficulty: "Easy" | "Medium" | "Hard";
  description?: string;
  primary_pattern: string;
  url: string;
  acceptanceRate?: string;
  submissionCount?: string;
}

export interface SearchResponse {
  results: Problem[];
}

export interface AskRequest {
  query: string;
}

export interface AskResponse {
  query: string;
  answer: string;
}

// Difficulty filter options – keeps UI and API in sync
export type DifficultyFilter = "All" | "Easy" | "Medium" | "Hard";
