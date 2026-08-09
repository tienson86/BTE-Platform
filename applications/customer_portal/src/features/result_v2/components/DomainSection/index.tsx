import { memo } from "react";
import type {
  ChromeModel,
  DomainKey,
  DomainModel,
  RecommendationModel,
} from "../../adapter/PortalResultModel";
import { interpolateDomain } from "../../formatters/labels";
import { EmptyState } from "../EmptyState";
import { RecommendationCard } from "../RecommendationCard";
import { Expand } from "../Shared/Expand";
import { SectionHeader } from "../Shared/SectionHeader";

const TARGET: Record<DomainKey, string> = {
  career: "DomainCareer",
  wealth: "DomainWealth",
  relationship: "DomainRelationship",
  health: "DomainHealth",
  luck: "DomainLuck",
};

export type DomainSectionProps = {
  domain: DomainModel;
  recommendations: RecommendationModel[];
  chrome: ChromeModel;
  isExpanded: (id: string) => boolean;
  onToggleRecommendation: (id: string) => void;
  onToggleAnalysis: (key: DomainKey) => void;
  onEmptyNext?: () => void;
};

export const DomainSection = memo(function DomainSection({
  domain,
  recommendations,
  chrome,
  isExpanded,
  onToggleRecommendation,
  onToggleAnalysis,
  onEmptyNext,
}: DomainSectionProps) {
  const sectionId = `rv2-${TARGET[domain.key]}`;
  const analysisId = `rv2-analysis-${domain.key}`;
  const analysisExpanded = isExpanded(`analysis:${domain.key}`);
  const hasContent =
    domain.available &&
    Boolean(domain.intro || recommendations.length || domain.analysis_preview);

  return (
    <section
      className="rv2-section rv2-section--domain"
      id={sectionId}
      tabIndex={-1}
      aria-labelledby={`${sectionId}-title`}
      data-domain={domain.key}
    >
      <SectionHeader id={`${sectionId}-title`} icon={domain.key}>
        {domain.title}
      </SectionHeader>
      {!hasContent ? (
        <EmptyState
          title={domain.title}
          body={interpolateDomain(chrome.empty_domain, domain.key)}
          nextLabel={chrome.section_recommendation}
          onNext={onEmptyNext}
        />
      ) : (
        <>
          {domain.intro ? <p className="rv2-domain__intro">{domain.intro}</p> : null}
          {recommendations.map((item) => (
            <RecommendationCard
              key={item.id}
              model={item}
              chrome={chrome}
              expanded={isExpanded(`rec:${item.id}`)}
              onToggle={() => onToggleRecommendation(`rec:${item.id}`)}
            />
          ))}
          {domain.analysis_preview ? (
            <div className="rv2-card rv2-analysis-card">
              <p className="rv2-prose">{domain.analysis_preview}</p>
              {domain.analysis_detail ? (
                <>
                  <Expand
                    expanded={analysisExpanded}
                    expandLabel={chrome.expand_analysis}
                    collapseLabel={chrome.expand_analysis_less}
                    controlsId={analysisId}
                    onToggle={() => onToggleAnalysis(domain.key)}
                  />
                  {analysisExpanded ? (
                    <p id={analysisId} className="rv2-prose rv2-expand-panel">
                      {domain.analysis_detail}
                    </p>
                  ) : (
                    <div id={analysisId} hidden />
                  )}
                </>
              ) : null}
            </div>
          ) : null}
        </>
      )}
    </section>
  );
});
