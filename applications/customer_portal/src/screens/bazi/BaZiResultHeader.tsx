import { memo, type ReactNode } from "react";
import { Avatar } from "../../components/base/Avatar";
import { Badge } from "../../components/base/Badge";
import { Button } from "../../components/base/Button";
import { Card } from "../../components/base/Card";
import { Divider } from "../../components/base/Divider";
import { BaseText } from "../../components/base/BaseText";
import { Stack } from "../../components/layout/Stack";
import { Grid } from "../../components/layout/Grid";
import type {
  BaZiChartMetadata,
  BaZiProfile,
  BaZiQuickAction,
  BaZiResultLabels,
  PresentationStatus,
} from "./mockData";
import { SectionGate } from "./SectionGate";

export type BaZiResultHeaderProps = {
  status: PresentationStatus;
  labels: BaZiResultLabels;
  profile: BaZiProfile;
  metadata: BaZiChartMetadata;
  actions: readonly BaZiQuickAction[];
  errorMessage?: string;
};

function initialsFromName(name: string): string {
  const parts = name.trim().split(/\s+/);
  const last = parts[parts.length - 1] ?? "";
  return (last.charAt(0) || "B").toUpperCase();
}

/** WP05 — BaZi Result Header (presentation only). */
export const BaZiResultHeader = memo(function BaZiResultHeader({
  status,
  labels,
  profile,
  metadata,
  actions,
  errorMessage,
}: BaZiResultHeaderProps): ReactNode {
  return (
    <Card className="cui-bazi-header" aria-label={labels.pageTitle}>
      <SectionGate
        status={status}
        loadingLabel="Đang tải header kết quả"
        emptyTitle="Chưa có thông tin lá số"
        emptyDescription="Lập lá số mới để xem kết quả."
        errorTitle="Không tải được header kết quả"
        errorDescription={errorMessage}
      >
        <Stack gap="paragraph">
          <div className="cui-bazi-header__title-row">
            <div>
              <BaseText variant="pageTitle" className="cui-bazi-header__title">
                {labels.pageTitle}
              </BaseText>
              <Badge tone="info">
                {labels.fieldChartId}: {metadata.chartId}
              </Badge>
            </div>
            <Badge tone="success">{metadata.analysisStatus}</Badge>
          </div>

          <Divider />

          <section aria-labelledby="bazi-profile-heading">
            <BaseText id="bazi-profile-heading" variant="section">
              {labels.profileHeading}
            </BaseText>
            <div className="cui-bazi-header__profile">
              <Avatar
                size="lg"
                initials={initialsFromName(profile.fullName)}
                alt={profile.fullName}
              />
              <Grid columns={3} className="cui-bazi-header__profile-grid">
                <ProfileField label={labels.fieldFullName} value={profile.fullName} />
                <ProfileField label={labels.fieldGender} value={profile.gender} />
                <ProfileField label={labels.fieldSolar} value={profile.solarBirthDate} />
                <ProfileField label={labels.fieldLunar} value={profile.lunarBirthDate} />
                <ProfileField label={labels.fieldBirthTime} value={profile.birthTime} />
                <ProfileField label={labels.fieldBirthPlace} value={profile.birthPlace} />
              </Grid>
            </div>
          </section>

          <Divider />

          <section aria-labelledby="bazi-meta-heading">
            <BaseText id="bazi-meta-heading" variant="section">
              {labels.metadataHeading}
            </BaseText>
            <Grid columns={2} className="cui-bazi-header__meta-grid">
              <ProfileField label={labels.fieldCreatedAt} value={metadata.createdAt} />
              <ProfileField label={labels.fieldEngine} value={metadata.engineVersion} />
              <ProfileField
                label={labels.fieldRules}
                value={metadata.ruleDatabaseVersion}
              />
              <ProfileField
                label={labels.fieldInterpretation}
                value={metadata.interpretationVersion}
              />
            </Grid>
          </section>

          <Divider />

          <section aria-labelledby="bazi-actions-heading">
            <BaseText id="bazi-actions-heading" variant="section">
              {labels.actionsHeading}
            </BaseText>
            <div className="cui-bazi-header__actions" role="group" aria-label={labels.actionsHeading}>
              {actions.map((action) => (
                <Button
                  key={action.id}
                  variant="secondary"
                  disabled={!action.enabled}
                  aria-label={action.ariaLabel}
                  title={action.enabled ? action.label : `${action.label} (chưa khả dụng)`}
                >
                  {action.label}
                </Button>
              ))}
            </div>
          </section>
        </Stack>
      </SectionGate>
    </Card>
  );
});

function ProfileField({ label, value }: { label: string; value: string }): ReactNode {
  return (
    <div className="cui-bazi-field">
      <BaseText variant="caption" tone="muted">
        {label}
      </BaseText>
      <BaseText variant="body">{value}</BaseText>
    </div>
  );
}
