import type { ReactNode } from "react";
import type { BaZiResultViewModel } from "../../adapters";
import { AppProviders } from "../../app/AppProviders";
import { Stack } from "../../components/layout/Stack";
import { isMockDataSource } from "../../config/api";
import { useBaZiResult } from "../../hooks/useBaZiResult";
import { AppLayout } from "../../layouts/AppLayout";
import { PageWrapper } from "../../layouts/PageWrapper";
import type { AnalyzeChartRequest } from "../../models";
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
  /**
   * Injected ViewModel (tests / story).
   * When omitted, loads via AnalyzeService → Adapter.
   */
  data?: BaZiResultMockBundle | BaZiResultViewModel;
  /** Force section status without replacing payload. */
  status?: PresentationStatus;
  /** Birth payload for API analyze when `data` is not injected. */
  analyzeRequest?: AnalyzeChartRequest;
};

/**
 * BaZi Result screen — Wave 3 (WP05–WP09) + TASK_003A integration.
 * Uses AppLayout only. Component section APIs unchanged.
 */
export function BaZiResultScreen({
  pathname = "/result",
  userName,
  data,
  status,
  analyzeRequest,
}: BaZiResultScreenProps): ReactNode {
  const useMockDefault = isMockDataSource() && !analyzeRequest && data === undefined;

  const remote = useBaZiResult({
    request: analyzeRequest,
    enabled: data === undefined,
    initialData: data ?? (useMockDefault ? BAZI_RESULT_MOCK : undefined),
  });

  const bundle = data ?? remote.viewModel;
  const resolvedStatus = status ?? bundle.status;
  const labels = bundle.labels;
  const displayName = userName ?? bundle.profile.fullName;

  return (
    <AppProviders>
      <AppLayout pathname={pathname} userLabel={displayName}>
        <PageWrapper
          title={labels.pageTitle}
          description={bundle.metadata.chartId}
          breadcrumb={[
            { id: "home", label: "Portal", href: "/dashboard" },
            { id: "result", label: labels.pageTitle },
          ]}
        >
          <Stack gap="section" className="cui-bazi-result">
            <BaZiResultHeader
              status={resolvedStatus}
              labels={labels}
              profile={bundle.profile}
              metadata={bundle.metadata}
              actions={bundle.actions}
              errorMessage={bundle.errorMessage}
            />
            <FourPillarsCard
              status={resolvedStatus}
              labels={labels}
              pillars={bundle.pillars}
              errorMessage={bundle.errorMessage}
            />
            <div className="cui-bazi-result__split">
              <FiveElementsCard
                status={resolvedStatus}
                labels={labels}
                elements={bundle.fiveElements}
                errorMessage={bundle.errorMessage}
              />
              <StrengthCard
                status={resolvedStatus}
                labels={labels}
                strength={bundle.strength}
                errorMessage={bundle.errorMessage}
              />
            </div>
            <TenGodsCard
              status={resolvedStatus}
              labels={labels}
              gods={bundle.tenGods}
              errorMessage={bundle.errorMessage}
            />
          </Stack>
        </PageWrapper>
      </AppLayout>
    </AppProviders>
  );
}
