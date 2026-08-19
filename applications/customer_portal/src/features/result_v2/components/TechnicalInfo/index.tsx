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

const METADATA_LABELS: Record<string, string> = {
  year_pillar: "Năm",
  month_pillar: "Tháng",
  day_pillar: "Ngày",
  hour_pillar: "Giờ",
  day_master: "Nhật chủ",
  pattern: "Cách cục",
  climate_state: "Trạng thái khí hậu",
  balancing_need: "Nhu cầu điều hòa",
  climate_evidence: "Căn cứ khí hậu",
  temperature_score: "Điểm khí hậu (kỹ thuật)",
  strength: "Thân vượng/nhược",
  strength_score: "Điểm thân",
  score_grade: "Hạng điểm",
  score_total: "Điểm tổng",
  birth_place: "Nơi sinh",
  gender: "Giới tính",
};

function metadataLabel(key: string): string {
  return METADATA_LABELS[key] ?? key;
}

/** Prefer chart-fundamental keys first in the technical list. */
const METADATA_ORDER = [
  "year_pillar",
  "month_pillar",
  "day_pillar",
  "hour_pillar",
  "day_master",
  "pattern",
  "pattern_evidence",
  "climate_state",
  "balancing_need",
  "climate_evidence",
  "temperature_score",
  "strength",
  "strength_score",
  "score_grade",
  "score_total",
  "birth_place",
  "gender",
] as const;

export function TechnicalInfo({
  title,
  model,
  chrome,
  collapsed,
  onToggle,
}: TechnicalInfoProps) {
  if (!model.available) return null;
  const panelId = "rv2-technical-panel";
  const metaEntries = Object.entries(model.metadata ?? {}).sort(([a], [b]) => {
    const ia = (METADATA_ORDER as readonly string[]).indexOf(a);
    const ib = (METADATA_ORDER as readonly string[]).indexOf(b);
    const ra = ia === -1 ? 1000 : ia;
    const rb = ib === -1 ? 1000 : ib;
    return ra - rb || a.localeCompare(b);
  });

  return (
    <section
      className="rv2-section rv2-section--reference"
      id="rv2-Technical"
      tabIndex={-1}
      aria-labelledby="rv2-tech-title"
      data-chart-fundamentals="true"
    >
      <SectionHeader id="rv2-tech-title" icon="technical">
        {title}
      </SectionHeader>
      <Expand
        expanded={!collapsed}
        expandLabel={chrome.expand_technical}
        collapseLabel={chrome.expand_technical_less}
        controlsId={panelId}
        onToggle={onToggle}
      />
      {!collapsed ? (
        <div id={panelId} className="rv2-card rv2-technical-card rv2-expand-panel">
          <dl className="rv2-dl">
            {model.pillars ? (
              <div data-field="pillars">
                <dt>{chrome.technical_pillars}</dt>
                <dd>{model.pillars}</dd>
              </div>
            ) : null}
            {metaEntries.map(([key, value]) => (
              <div key={key} data-field={key}>
                <dt>{metadataLabel(key)}</dt>
                <dd>{value}</dd>
              </div>
            ))}
            {model.calendar ? (
              <div>
                <dt>{chrome.technical_calendar}</dt>
                <dd>{model.calendar}</dd>
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
