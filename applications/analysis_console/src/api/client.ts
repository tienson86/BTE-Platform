import type {
  AnalysisData,
  ApiEnvelope,
  ChartData,
  CreateChartPayload,
  InterpretationData,
  ReportData,
} from "./types";

async function request<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(path, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });
  const payload = (await response.json()) as ApiEnvelope<T> & {
    details?: unknown;
    code?: string;
  };
  if (!response.ok || !payload.success) {
    throw new Error(payload.message || `Request failed (${response.status})`);
  }
  return payload.data;
}

export const api = {
  health: () =>
    fetch("/health").then(async (r) => {
      if (!r.ok) throw new Error("API unavailable");
      return r.json() as Promise<{ status: string; service: string; version: string }>;
    }),

  createChart: (body: CreateChartPayload) =>
    request<ChartData>("/api/v1/charts", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  getChart: (chartId: string) =>
    request<ChartData>(`/api/v1/charts/${chartId}`),

  runAnalysis: (chartId: string) =>
    request<AnalysisData>("/api/v1/analysis", {
      method: "POST",
      body: JSON.stringify({ chart_id: chartId }),
    }),

  getAnalysis: (analysisId: string) =>
    request<AnalysisData>(`/api/v1/analysis/${analysisId}`),

  runInterpretation: (analysisId: string) =>
    request<InterpretationData>("/api/v1/interpretation", {
      method: "POST",
      body: JSON.stringify({ analysis_id: analysisId }),
    }),

  getInterpretation: (interpretationId: string) =>
    request<InterpretationData>(`/api/v1/interpretation/${interpretationId}`),

  generateReport: (interpretationId: string, title = "BTE Analysis Report") =>
    request<ReportData>("/api/v1/report", {
      method: "POST",
      body: JSON.stringify({
        interpretation_id: interpretationId,
        formats: ["html", "markdown", "pdf", "json"],
        include_structured_data: true,
        title,
      }),
    }),
};

export function downloadPdfBase64(base64: string, filename: string) {
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i += 1) {
    bytes[i] = binary.charCodeAt(i);
  }
  const blob = new Blob([bytes], { type: "application/pdf" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}
