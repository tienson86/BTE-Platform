export type AssetType = "rule" | "sentence" | "phrase" | "terminology";
export type AssetStatus =
  | "draft"
  | "review"
  | "approved"
  | "released"
  | "rejected";
export type WorkflowAction = "submit" | "approve" | "reject" | "release";

export interface ApiEnvelope<T> {
  success: boolean;
  message: string;
  data: T;
  request_id?: string | null;
}

export interface HistoryEntry {
  event_id: string;
  action: string;
  actor: string;
  at: string;
  message: string;
  details?: Record<string, unknown>;
}

export interface VersionSnapshot {
  version: string;
  created_at: string;
  created_by: string;
  status: AssetStatus;
  content: Record<string, unknown>;
  title: string;
  note?: string;
}

export interface KnowledgeAsset {
  asset_id: string;
  asset_type: AssetType;
  title: string;
  content: Record<string, unknown>;
  status: AssetStatus;
  version: string;
  created_at: string;
  updated_at: string;
  created_by: string;
  updated_by: string;
  history: HistoryEntry[];
  versions: VersionSnapshot[];
  metadata: Record<string, unknown>;
}

export interface ValidationIssue {
  code: string;
  severity: "error" | "warning" | "info";
  message: string;
  path?: string;
}

export interface ValidationResult {
  asset_id: string;
  valid: boolean;
  issues: ValidationIssue[];
}

export interface PreviewResult {
  asset_id: string;
  asset_type: AssetType;
  title: string;
  version: string;
  status: AssetStatus;
  preview_text: string;
  content: Record<string, unknown>;
}

export interface DiffLine {
  kind: "equal" | "add" | "remove";
  text: string;
}

export interface DiffResult {
  asset_id: string;
  from_version: string;
  to_version: string;
  lines: DiffLine[];
}

export interface CreateAssetPayload {
  asset_type: AssetType;
  title: string;
  content: Record<string, unknown>;
  actor?: string;
}

export interface UpdateAssetPayload {
  title?: string;
  content?: Record<string, unknown>;
  actor?: string;
  note?: string;
}
