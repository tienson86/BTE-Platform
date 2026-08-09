import { memo } from "react";
import type { ChromeModel, TechnicalModel } from "../../adapter/PortalResultModel";
import { Expand } from "../Shared/Expand";
import { SectionHeader } from "../Shared/SectionHeader";

export type TechnicalInfoProps = {
  title: string;
  model: TechnicalModel;
  chrome: ChromeModel;
  collapsed: boolean;
  onToggle: () => void;
};

export function TechnicalInfo({
  title,
  model,
  chrome,
  collapsed,
  onToggle,
}: TechnicalInfoProps) {
  if (!model.available) return null;
  const panelId = "rv2-technical-panel";
  return (
    <section
      className="rv2-section"
      id="rv2-Technical"
      tabIndex={-1}
      aria-labelledby="rv2-tech-title"
    >
      <SectionHeader id="rv2-tech-title">{title}</SectionHeader>
      <Expand
        expanded={!collapsed}
        expandLabel={chrome.expand_technical}
        collapseLabel={chrome.expand_technical_less}
        controlsId={panelId}
        onToggle={onToggle}
      />
      {!collapsed ? (
        <div id={panelId} className="rv2-card">
          <dl className="rv2-dl">
            {model.calendar ? (
              <div>
                <dt>{chrome.technical_calendar}</dt>
                <dd>{model.calendar}</dd>
              </div>
            ) : null}
            {model.pillars ? (
              <div>
                <dt>{chrome.technical_pillars}</dt>
                <dd>{model.pillars}</dd>
              </div>
            ) : null}
            {model.timezone ? (
              <div>
                <dt>{chrome.technical_timezone}</dt>
                <dd>{model.timezone}</dd>
              </div>
            ) : null}
            {model.schema ? (
              <div>
                <dt>{chrome.technical_schema}</dt>
                <dd>{model.schema}</dd>
              </div>
            ) : null}
            {model.ids ? (
              <div>
                <dt>{chrome.technical_ids}</dt>
                <dd>{model.ids}</dd>
              </div>
            ) : null}
          </dl>
        </div>
      ) : (
        <div id={panelId} hidden />
      )}
    </section>
  );
}

export default memo(TechnicalInfo);
