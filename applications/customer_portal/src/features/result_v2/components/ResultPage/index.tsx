import { lazy, memo, Suspense, useMemo } from "react";
import type { DomainKey, PageState, PortalResultModel } from "../../adapter/PortalResultModel";
import { DOMAIN_ORDER } from "../../adapter/PortalResultModel";
import {
  showAppendix,
  showCharts,
  showDomain,
  showKnowledge,
  showTechnical,
  showWarnings,
} from "../../utils/visibility";
import { Appendix } from "../Appendix";
import { DomainSection } from "../DomainSection";
import { EmptyState } from "../EmptyState";
import { ErrorState } from "../ErrorState";
import { ExecutiveSummary } from "../ExecutiveSummary";
import { Footer } from "../Footer";
import { Hero } from "../Hero";
import { ImportantWarnings } from "../ImportantWarnings";
import { Knowledge } from "../Knowledge";
import { LoadingState } from "../LoadingState";
import { Recommendation } from "../Recommendation";
import { TechnicalInfo } from "../TechnicalInfo";

// Charts stay lazy; Knowledge + Technical are eager for readable narrative / fundamentals.
const ChartsLazy = lazy(async () => {
  const mod = await import("../Charts");
  return { default: mod.Charts };
});

export type ResultPageProps = {
  model: PortalResultModel;
  pageState: PageState;
  isExpanded: (id: string) => boolean;
  onToggle: (id: string) => void;
  onNavigate: (targetUiId: string) => void;
  onRetry?: () => void;
  onPrimaryCta?: () => void;
  onSecondaryCta?: () => void;
};

export const ResultPage = memo(function ResultPage({
  model,
  pageState,
  isExpanded,
  onToggle,
  onNavigate,
  onRetry,
  onPrimaryCta,
  onSecondaryCta,
}: ResultPageProps) {
  const { chrome, cta } = model;
  const recById = useMemo(() => {
    const map = new Map(model.recommendations.map((item) => [item.id, item]));
    return map;
  }, [model.recommendations]);

  if (pageState === "loading") {
    return (
      <div className="rv2-page" data-page="result-v2" data-state={pageState}>
        <LoadingState label={chrome.page_loading} />
      </div>
    );
  }

  if (pageState === "offline") {
    return (
      <div className="rv2-page" data-page="result-v2" data-state={pageState}>
        <ErrorState
          title={chrome.page_offline}
          body={chrome.page_offline}
          retryLabel={chrome.error_retry}
          onRetry={onRetry}
        />
      </div>
    );
  }

  if (pageState === "error") {
    return (
      <div className="rv2-page" data-page="result-v2" data-state={pageState}>
        <ErrorState
          title={chrome.error_page}
          body={model.page.error_message ?? chrome.error_page}
          retryLabel={chrome.error_retry}
          onRetry={onRetry}
        />
      </div>
    );
  }

  if (pageState === "empty") {
    return (
      <div className="rv2-page" data-page="result-v2" data-state={pageState}>
        <EmptyState
          title={chrome.empty_page}
          body={chrome.empty_page}
          nextLabel={chrome.error_retry}
          onNext={onRetry}
        />
      </div>
    );
  }

  // Narrative open by default; Technical remains available but secondary (collapsed).
  const technicalCollapsed = !isExpanded("section:technical");
  const knowledgeCollapsed = !isExpanded("section:knowledge");

  return (
    <div className="rv2-page" data-page="result-v2" data-polish="px4" data-state={pageState} data-contract={model.contract_id}>
      <a className="rv2-skip" href="#rv2-main">
        {chrome.skip}
      </a>
      <nav className="rv2-nav">
        {model.nav.items
          .filter((item) => item.visible)
          .map((item) => (
            <button
              key={item.target_ui_id}
              type="button"
              className="rv2-nav__link"
              onClick={() => onNavigate(item.target_ui_id)}
            >
              {item.label}
            </button>
          ))}
      </nav>
      <main className="rv2-main" id="rv2-main">
        {model.hero ? <Hero model={model.hero} /> : null}
        {model.summary ? (
          <ExecutiveSummary
            model={model.summary}
            chrome={chrome}
            onJumpToRecommendations={() => onNavigate("Recommendation")}
          />
        ) : null}
        <Recommendation
          title={chrome.section_recommendation}
          items={model.recommendations}
          cta={cta}
          chrome={chrome}
          pageState={pageState}
          isExpanded={isExpanded}
          onToggleItem={onToggle}
          onPrimaryCta={onPrimaryCta}
          onSecondaryCta={onSecondaryCta}
          onEmptyNext={() => onNavigate("Summary")}
        />
        {showWarnings(model.warnings) ? (
          <ImportantWarnings
            title={chrome.section_warnings}
            items={model.warnings}
            chrome={chrome}
            isExpanded={isExpanded}
            onToggleItem={onToggle}
          />
        ) : null}
        {showKnowledge(model.knowledge) ? (
          <Knowledge
            title={chrome.section_knowledge}
            items={model.knowledge}
            chrome={chrome}
            sectionCollapsed={knowledgeCollapsed}
            isItemExpanded={(index) => isExpanded(`know:${index}`)}
            onToggleSection={() => onToggle("section:knowledge")}
            onToggleItem={(index) => onToggle(`know:${index}`)}
          />
        ) : null}
        {DOMAIN_ORDER.map((key: DomainKey) => {
          const domain = model.domains[key];
          if (!showDomain(domain)) return null;
          const recs = domain.recommendation_ids
            .map((id) => recById.get(id))
            .filter((item): item is NonNullable<typeof item> => Boolean(item));
          return (
            <DomainSection
              key={key}
              domain={domain}
              recommendations={recs}
              chrome={chrome}
              isExpanded={isExpanded}
              onToggleRecommendation={onToggle}
              onToggleAnalysis={(domainKey) => onToggle(`analysis:${domainKey}`)}
              onEmptyNext={() => onNavigate("Recommendation")}
            />
          );
        })}
        {showCharts(model.charts) ? (
          <Suspense fallback={null}>
            <ChartsLazy
              title={chrome.section_charts}
              items={model.charts}
              chrome={chrome}
              isExpanded={(id) => isExpanded(id)}
              onToggleTable={(index) => onToggle(`chart:${index}`)}
            />
          </Suspense>
        ) : null}
        {showTechnical(model.technical) ? (
          <TechnicalInfo
            title={chrome.section_technical}
            model={model.technical}
            chrome={chrome}
            collapsed={technicalCollapsed}
            onToggle={() => onToggle("section:technical")}
          />
        ) : null}
        {showAppendix(model.appendix) ? (
          <Appendix title={chrome.section_appendix} model={model.appendix} />
        ) : null}
      </main>
      <Footer />
    </div>
  );
});
