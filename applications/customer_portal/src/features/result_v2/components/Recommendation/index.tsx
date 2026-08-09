import { memo } from "react";
import type {
  ChromeModel,
  CtaModel,
  PageState,
  RecommendationModel,
} from "../../adapter/PortalResultModel";
import { groupRecommendations } from "../../utils/grouping";
import { EmptyState } from "../EmptyState";
import { RecommendationCard } from "../RecommendationCard";
import { Button } from "../Shared/Button";
import { SectionHeader } from "../Shared/SectionHeader";

export type RecommendationRegionProps = {
  title: string;
  items: RecommendationModel[];
  cta: CtaModel;
  chrome: ChromeModel;
  pageState: PageState;
  isExpanded: (id: string) => boolean;
  onToggleItem: (id: string) => void;
  onPrimaryCta?: () => void;
  onSecondaryCta?: () => void;
  onEmptyNext?: () => void;
};

export const Recommendation = memo(function Recommendation({
  title,
  items,
  cta,
  chrome,
  pageState,
  isExpanded,
  onToggleItem,
  onPrimaryCta,
  onSecondaryCta,
  onEmptyNext,
}: RecommendationRegionProps) {
  const groups = groupRecommendations(items);
  const loading = pageState === "loading" || pageState === "printing" || pageState === "exporting";
  const showPrimary = pageState !== "error" && pageState !== "empty" && pageState !== "offline";

  return (
    <section
      className="rv2-section"
      id="rv2-Recommendation"
      tabIndex={-1}
      aria-labelledby="rv2-rec-title"
    >
      <SectionHeader id="rv2-rec-title">{title}</SectionHeader>
      {items.length === 0 ? (
        <EmptyState
          title={title}
          body={chrome.empty_recommendations}
          nextLabel={chrome.section_summary}
          onNext={onEmptyNext}
        />
      ) : (
        <div className="rv2-rec-grid">
          {groups.map((group) =>
            group.items.length === 0 ? null : (
              <div key={group.domain} className="rv2-rec-group">
                <h3 className="rv2-rec-group__title">{group.domainLabel}</h3>
                {group.items.map((item) => (
                  <RecommendationCard
                    key={item.id}
                    model={item}
                    chrome={chrome}
                    expanded={isExpanded(`rec:${item.id}`)}
                    onToggle={() => onToggleItem(`rec:${item.id}`)}
                  />
                ))}
              </div>
            ),
          )}
        </div>
      )}
      {showPrimary ? (
        <div className="rv2-cta-row">
          <Button
            variant="primary"
            disabled={!cta.primary_enabled || loading}
            onClick={onPrimaryCta}
          >
            {loading ? chrome.cta_loading : cta.primary_label}
          </Button>
          {cta.secondary_label ? (
            <Button
              variant="secondary"
              disabled={!cta.secondary_enabled || loading}
              onClick={onSecondaryCta}
            >
              {cta.secondary_label}
            </Button>
          ) : null}
        </div>
      ) : null}
    </section>
  );
});
