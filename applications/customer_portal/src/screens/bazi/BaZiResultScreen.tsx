import type { ReactNode } from "react";
import { AppProviders } from "../../app/AppProviders";
import { Stack } from "../../components/layout/Stack";
import { AppLayout } from "../../layouts/AppLayout";
import { PageWrapper } from "../../layouts/PageWrapper";
import { BaZiResultHeader } from "./BaZiResultHeader";
import { FiveElementsCard } from "./FiveElementsCard";
import { FourPillarsCard } from "./FourPillarsCard";
import { StrengthCard } from "./StrengthCard";
import { TenGodsCard } from "./TenGodsCard";
import {
  BAZI_RESULT_MOCK,
  type BaZiResultMockBundle,
  type PresentationStatus,
} from "./mockData";

export type BaZiResultScreenProps = {
  pathname?: string;
  userName?: string;
  /** Override mock bundle (tests / future bindings). */
  data?: BaZiResultMockBundle;
  /** Force section status without replacing mock payload. */
  status?: PresentationStatus;
};

/**
 * BaZi Result screen — Wave 3 (WP05–WP09).
 * Uses AppLayout only. Presentation + mock data. No Engine calls.
 */
export function BaZiResultScreen({
  pathname = "/result",
  userName,
  data = BAZI_RESULT_MOCK,
  status,
}: BaZiResultScreenProps): ReactNode {
  const resolvedStatus = status ?? data.status;
  const labels = data.labels;
  const displayName = userName ?? data.profile.fullName;

  return (
    <AppProviders>
      <AppLayout pathname={pathname} userLabel={displayName}>
        <PageWrapper
          title={labels.pageTitle}
          description={data.metadata.chartId}
          breadcrumb={[
            { id: "home", label: "Portal", href: "/dashboard" },
            { id: "result", label: labels.pageTitle },
          ]}
        >
          <Stack gap="section" className="cui-bazi-result">
            <BaZiResultHeader
              status={resolvedStatus}
              labels={labels}
              profile={data.profile}
              metadata={data.metadata}
              actions={data.actions}
              errorMessage={data.errorMessage}
            />
            <FourPillarsCard
              status={resolvedStatus}
              labels={labels}
              pillars={data.pillars}
              errorMessage={data.errorMessage}
            />
            <div className="cui-bazi-result__split">
              <FiveElementsCard
                status={resolvedStatus}
                labels={labels}
                elements={data.fiveElements}
                errorMessage={data.errorMessage}
              />
              <StrengthCard
                status={resolvedStatus}
                labels={labels}
                strength={data.strength}
                errorMessage={data.errorMessage}
              />
            </div>
            <TenGodsCard
              status={resolvedStatus}
              labels={labels}
              gods={data.tenGods}
              errorMessage={data.errorMessage}
            />
          </Stack>
        </PageWrapper>
      </AppLayout>
    </AppProviders>
  );
}
