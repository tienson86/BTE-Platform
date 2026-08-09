import { memo } from "react";
import type { ChromeModel, RecommendationModel } from "../../adapter/PortalResultModel";
import { Card } from "../Shared/Card";
import { Expand } from "../Shared/Expand";
import { ResultIcon } from "../Shared/Icon";
import { Tag } from "../Shared/Tag";

export type RecommendationCardProps = {
  model: RecommendationModel;
  chrome: ChromeModel;
  expanded: boolean;
  onToggle: () => void;
  disabled?: boolean;
};

export const RecommendationCard = memo(function RecommendationCard({
  model,
  chrome,
  expanded,
  onToggle,
  disabled = false,
}: RecommendationCardProps) {
  const detailId = `rv2-rec-detail-${model.id}`;
  return (
    <Card
      className="rv2-rec-card"
      domain={model.domain}
      priority={model.priority}
      disabled={disabled}
      title={
        <>
          <div className="rv2-rec-card__meta">
            <ResultIcon name={model.domain} />
            <Tag>{model.domain_label}</Tag>
          </div>
          <h3 className="rv2-card__title">{model.title}</h3>
        </>
      }
    >
      <div className="rv2-field">
        <span className="rv2-field__label">{chrome.field_why}</span>
        <p className="rv2-field__value">{model.reason}</p>
      </div>
      <div className="rv2-field">
        <span className="rv2-field__label">{chrome.field_expected_result}</span>
        <p className="rv2-field__value rv2-field__value--result">{model.expected_result}</p>
      </div>
      <div className="rv2-field">
        <span className="rv2-field__label">{chrome.field_action}</span>
        <p className="rv2-field__value">{model.action}</p>
      </div>
      {model.detail ? (
        <div className="rv2-card__footer">
          <Expand
            expanded={expanded}
            expandLabel={chrome.expand_more}
            collapseLabel={chrome.expand_less}
            controlsId={detailId}
            onToggle={onToggle}
          />
          {expanded ? (
            <div id={detailId} className="rv2-prose rv2-expand-panel">
              <p>{model.detail}</p>
            </div>
          ) : (
            <div id={detailId} hidden />
          )}
        </div>
      ) : null}
    </Card>
  );
});
