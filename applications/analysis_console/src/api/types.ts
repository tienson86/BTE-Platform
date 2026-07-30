export type ApiEnvelope<T = Record<string, unknown>> = {
  success: boolean;
  message: string;
  data: T;
  request_id?: string | null;
};

export type ChartData = {
  chart_id: string;
  chart: {
    day_master: string;
    gender?: string | null;
    luck?: Record<string, unknown>;
    stems?: Record<string, string>;
    branches?: Record<string, string>;
  };
  calendar: {
    year?: number | null;
    month?: number | null;
    day?: number | null;
    hour?: number | null;
    minute?: number | null;
    timezone?: string;
  };
  metadata: Record<string, unknown>;
};

export type AnalysisData = {
  analysis_id: string;
  chart_id: string;
  request_id: string;
  stage_ids: string[];
  summary: Record<string, unknown> | null;
  confidence?: { score?: number | null; level?: string | null } | null;
};

export type InterpretationSection = {
  section_id: string;
  title: string;
  body: string;
};

export type InterpretationData = {
  interpretation_id: string;
  analysis_id: string;
  chart_id: string;
  overview: string;
  sections: InterpretationSection[];
  summary?: Record<string, unknown>;
};

export type ReportData = {
  report_id: string;
  interpretation_id: string;
  analysis_id: string;
  chart_id: string;
  html?: string | null;
  markdown?: string | null;
  pdf_base64?: string | null;
  pdf_size?: number | null;
  structured_report?: {
    sections?: InterpretationSection[];
    overview?: string;
  };
};

export type CreateChartPayload = {
  day_master: string;
  year?: number;
  month?: number;
  day?: number;
  hour?: number;
  minute?: number;
  gender?: string;
  timezone?: string;
  full_name?: string;
};
