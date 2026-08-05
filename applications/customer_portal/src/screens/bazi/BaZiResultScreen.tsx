import type { ReactNode } from "react";
import type { BaZiResultViewModel } from "../../adapters";
import { AppProviders } from "../../app/AppProviders";
import { Stack } from "../../components/layout/Stack";
import { AppLayout } from "../../layouts/AppLayout";
import { RESULT_TOC_ITEMS } from "../../layouts/Navigation/navItems";
import { PageWrapper } from "../../layouts/PageWrapper";
import { BaZiResultHeader } from "./BaZiResultHeader";
import { ExecutiveSummaryCard } from "./ExecutiveSummaryCard";
import { FiveElementsCard } from "./FiveElementsCard";
import { FourPillarsCard } from "./FourPillarsCard";
import { InterpretationCard } from "./InterpretationCard";
import { KnowledgeCard } from "./KnowledgeCard";
import { ShenShaCard } from "./ShenShaCard";
import { SpiritGodsRow } from "./SpiritGodsRow";
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
  data?: BaZiResultMockBundle | BaZiResultViewModel;
  status?: PresentationStatus;
};

/**
 * Canonical BaZi Result — expected information flow (PO):
 * Executive Summary → BaZi Overview → Four Pillars → Five Elements →
 * Strength → Ten Gods → ShenSha → Interpretation → Knowledge
 */
export function BaZiResultScreen({
  pathname = "/result",
  userName,
  data = BAZI_RESULT_MOCK,
  status,
}: BaZiResultScreenProps): ReactNode {
  const bundle = data;
  const resolvedStatus = status ?? bundle.status;
  const labels = bundle.labels;
  const displayName = userName ?? bundle.profile.fullName;

  return (
    <AppProviders>
      <AppLayout
        pathname={pathname}
        userLabel={displayName}
        tocItems={RESULT_TOC_ITEMS}
        tocTitle="MỤC LỤC"
        tocActiveId="summary"
      >
        <PageWrapper
          title={labels.pageTitle}
          description={`${bundle.metadata.chartId} · ${bundle.profile.fullName}`}
          className="cui-bazi-page"
        >
          <Stack gap="section" className="cui-bazi-result cui-bazi-result--canonical">
            {/* 1. Executive Summary */}
            <ExecutiveSummaryCard
              status={resolvedStatus}
              labels={labels}
              executive={bundle.executive}
              errorMessage={bundle.errorMessage}
            />

            {/* 2. BaZi Overview */}
            <section id="tong-quan" className="cui-bazi-level">
              <BaZiResultHeader
                status={resolvedStatus}
                labels={labels}
                profile={bundle.profile}
                metadata={bundle.metadata}
                actions={bundle.actions}
                errorMessage={bundle.errorMessage}
              />
            </section>

            {/* 3. Four Pillars */}
            <FourPillarsCard
              status={resolvedStatus}
              labels={labels}
              pillars={bundle.pillars}
              errorMessage={bundle.errorMessage}
            />

            {/* 4. Five Elements */}
            <section id="ngu-hanh" className="cui-bazi-level">
              <FiveElementsCard
                status={resolvedStatus}
                labels={labels}
                elements={bundle.fiveElements}
                errorMessage={bundle.errorMessage}
              />
            </section>

            {/* 5. Strength (+ Dụng/Kỵ glance) */}
            <section id="than-vuong" className="cui-bazi-level">
              <div className="cui-bazi-strength-row">
                <StrengthCard
                  status={resolvedStatus}
                  labels={labels}
                  strength={bundle.strength}
                  errorMessage={bundle.errorMessage}
                />
                <SpiritGodsRow gods={bundle.spiritGods} />
              </div>
            </section>

            {/* 6. Ten Gods */}
            <section id="thap-than" className="cui-bazi-level">
              <TenGodsCard
                status={resolvedStatus}
                labels={labels}
                gods={bundle.tenGods}
                errorMessage={bundle.errorMessage}
              />
            </section>

            {/* 7. ShenSha */}
            <section id="than-sat" className="cui-bazi-level">
              <ShenShaCard
                status={resolvedStatus}
                labels={labels}
                items={bundle.shenSha}
                errorMessage={bundle.errorMessage}
              />
            </section>

            {/* 8. Interpretation */}
            <section id="luan-giai" className="cui-bazi-level">
              <InterpretationCard
                status={resolvedStatus}
                labels={labels}
                interpretation={bundle.interpretation}
                errorMessage={bundle.errorMessage}
              />
            </section>

            {/* 9. Knowledge */}
            <section id="tri-thuc" className="cui-bazi-level">
              <KnowledgeCard
                status={resolvedStatus}
                labels={labels}
                items={bundle.knowledge}
                errorMessage={bundle.errorMessage}
              />
            </section>
          </Stack>
        </PageWrapper>
      </AppLayout>
    </AppProviders>
  );
}
