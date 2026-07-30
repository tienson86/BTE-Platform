/** Domain types for Analysis Console project library. */

import type { ChartData, CreateChartPayload } from "../api/types";

export type LibraryChart = {
  id: string;
  chart_id: string | null;
  name: string;
  customer_name: string;
  day_master: string;
  gender: string;
  year: number | null;
  month: number | null;
  day: number | null;
  favorite: boolean;
  pinned: boolean;
  created_at: string;
  updated_at: string;
  last_opened_at: string;
  tags: string[];
  payload: CreateChartPayload;
  remote?: ChartData | null;
};

export type TimelineEventType =
  | "chart_created"
  | "chart_opened"
  | "analysis_run"
  | "interpretation"
  | "report"
  | "export"
  | "import"
  | "favorite"
  | "pin";

export type TimelineEvent = {
  id: string;
  type: TimelineEventType;
  title: string;
  detail: string;
  at: string;
  chart_id: string | null;
  library_id: string | null;
};

export type CustomerRecord = {
  id: string;
  name: string;
  chart_count: number;
  library_ids: string[];
  last_seen: string;
  notes: string;
};

export type UserProfile = {
  display_name: string;
  email: string;
  role: string;
  organization: string;
  locale: string;
  bio: string;
};

export type AppSettings = {
  theme_preference: "light" | "dark" | "system";
  density: "comfortable" | "compact";
  auto_save_charts: boolean;
  show_api_status: boolean;
  reduce_motion: boolean;
  default_timezone: string;
};

export type LibraryExportBundle = {
  version: "1.0.0";
  exported_at: string;
  charts: LibraryChart[];
  timeline: TimelineEvent[];
  customers: CustomerRecord[];
  profile: UserProfile;
  settings: AppSettings;
};

export const DEFAULT_PROFILE: UserProfile = {
  display_name: "Analyst",
  email: "analyst@bte.local",
  role: "Senior Analyst",
  organization: "BTE Platform",
  locale: "vi-VN",
  bio: "BaZi analysis workspace user.",
};

export const DEFAULT_SETTINGS: AppSettings = {
  theme_preference: "system",
  density: "comfortable",
  auto_save_charts: true,
  show_api_status: true,
  reduce_motion: false,
  default_timezone: "Asia/Ho_Chi_Minh",
};
