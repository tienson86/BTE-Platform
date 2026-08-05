import { memo, type ReactNode } from "react";
import { Avatar } from "../../components/base/Avatar";
import { Badge } from "../../components/base/Badge";
import { BaseText } from "../../components/base/BaseText";
import type { BaseTone } from "../../components/base/types";
import type {
  BaZiChartMetadata,
  BaZiProfile,
  BaZiResultLabels,
  PresentationStatus,
} from "./mockData";
import { SectionGate } from "./SectionGate";

export type ContextHeaderProps = {
  status: PresentationStatus;
  labels: BaZiResultLabels;
  profile: BaZiProfile;
  metadata: BaZiChartMetadata;
  errorMessage?: string;
};

function initialsFromName(name: string): string {
  const parts = name.trim().split(/\s+/);
  const last = parts[parts.length - 1] ?? "";
  return (last.charAt(0) || "B").toUpperCase();
}

function buildBirthSummary(profile: BaZiProfile): string {
  const date = profile.solarBirthDate.trim();
  const time = profile.birthTime.trim();
  if (date && time && date !== "—" && time !== "—") {
    return `${date} · ${time}`;
  }
  return date || time || "—";
}

function statusTone(analysisStatus: string): BaseTone {
  const normalized = analysisStatus.toLowerCase();
  if (normalized.includes("lỗi") || normalized.includes("error")) {
    return "danger";
  }
  if (
    normalized.includes("đang") ||
    normalized.includes("loading") ||
    normalized.includes("xử lý")
  ) {
    return "warning";
  }
  if (normalized.includes("hoàn") || normalized.includes("xong") || normalized.includes("ready")) {
    return "success";
  }
  return "info";
}

/**
 * S00 — Context Header (context strip).
 * Confirms which profile/chart/analysis the user is viewing.
 * Not Navigation, not Hero, not Identity / Decision Support.
 */
export const ContextHeader = memo(function ContextHeader({
  status,
  labels,
  profile,
  metadata,
  errorMessage,
}: ContextHeaderProps): ReactNode {
  const birthSummary = buildBirthSummary(profile);
  const analysisVersion = metadata.interpretationVersion;

  return (
    <section
      id="ngu-canh"
      className="cui-bazi-context"
      aria-label={labels.contextTitle}
      data-section="s00-context"
    >
      <SectionGate
        status={status}
        loadingLabel="Đang tải ngữ cảnh lá số"
        emptyTitle="Chưa có ngữ cảnh lá số"
        emptyDescription="Lập lá số mới để xác nhận hồ sơ đang xem."
        errorTitle="Không tải được ngữ cảnh lá số"
        errorDescription={errorMessage}
      >
        <div className="cui-bazi-context__strip">
          <div className="cui-bazi-context__identity">
            <Avatar
              size="sm"
              initials={initialsFromName(profile.fullName)}
              alt={profile.fullName}
              className="cui-bazi-context__avatar"
            />
            <div className="cui-bazi-context__identity-text">
              <BaseText as="div" variant="body" className="cui-bazi-context__name">
                {profile.fullName}
              </BaseText>
              <BaseText as="div" variant="caption" tone="muted">
                {labels.fieldGender}: {profile.gender}
              </BaseText>
            </div>
          </div>

          <div className="cui-bazi-context__fields" role="list">
            <ContextField
              label={labels.fieldChartId}
              value={metadata.chartId}
              emphasize
            />
            <ContextField label={labels.fieldBirthSummary} value={birthSummary} />
            <ContextField label={labels.fieldAnalysisVersion} value={analysisVersion} />
            <ContextField label={labels.fieldAnalyzedAt} value={metadata.analyzedAt} />
          </div>

          <div className="cui-bazi-context__status">
            <Badge tone={statusTone(metadata.analysisStatus)}>
              {metadata.analysisStatus}
            </Badge>
            <a className="cui-bazi-context__detail-link" href="#tong-quan">
              {labels.contextDetailLink}
            </a>
          </div>
        </div>
      </SectionGate>
    </section>
  );
});

function ContextField({
  label,
  value,
  emphasize = false,
}: {
  label: string;
  value: string;
  emphasize?: boolean;
}): ReactNode {
  return (
    <div
      className={
        emphasize
          ? "cui-bazi-context__field cui-bazi-context__field--emphasize"
          : "cui-bazi-context__field"
      }
      role="listitem"
    >
      <BaseText as="span" variant="caption" tone="muted">
        {label}
      </BaseText>
      <BaseText as="span" variant="body">
        {value}
      </BaseText>
    </div>
  );
}
