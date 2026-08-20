/**
 * Canonical REST paths under the API base URL (TASK_003A).
 * Base URL already includes `/api/v1` (or `/backend/api/v1`).
 */

export const API_ENDPOINTS = {
  health: "/health",
  analyze: "/analyze",
  bazi: "/bazi",
  calendar: "/calendar",
  pattern: "/pattern",
  score: "/score",
  interpretation: "/interpretation",
  report: "/report",
  exportPdf: "/export/pdf",
  exportDocx: "/export/docx",
  narrative: "/narrative",
  discussion: "/discussion",
  cases: "/cases",
  customers: "/customers",
} as const;

export type ApiEndpointKey = keyof typeof API_ENDPOINTS;
