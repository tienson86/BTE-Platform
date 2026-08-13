/**
 * Four Pillars detail + Shen Sha cards — presentation only.
 */

import type { ReactNode } from "react";
import { PresentationText } from "../../../components/shared/PresentationText";
import type { ChartDetailViewModel, ShenShaViewModel } from "../viewModels";
import { ResultCardShell } from "./ResultCardShell";

export function ChartDetailCard({ model }: { model: ChartDetailViewModel }): ReactNode {
  if (!model.visible || model.pillars.length === 0) return null;

  return (
    <ResultCardShell
      title={model.title}
      titleId="rp-chart-detail-title"
      data-card="four-pillars"
      data-priority="2"
      className="rp-card--auto"
    >
      <div className="rp-table-wrap">
        <table className="rp-chart-table">
          <thead>
            <tr>
              <th scope="col" />
              {model.pillars.map((pillar) => (
                <th key={pillar.label} scope="col">
                  {pillar.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            <DetailRow label="Thiên can" values={model.pillars.map((pillar) => pillar.stem)} />
            <DetailRow label="Địa chi" values={model.pillars.map((pillar) => pillar.branch)} />
            <DetailRow label="Nạp âm" values={model.pillars.map((pillar) => pillar.napAm)} />
            <DetailRow label="Tàng can" values={model.pillars.map((pillar) => pillar.hiddenStems)} />
            <DetailRow label="Thập thần" values={model.pillars.map((pillar) => pillar.tenGod)} />
            <DetailRow label="Trường sinh" values={model.pillars.map((pillar) => pillar.growthStage)} />
          </tbody>
        </table>
      </div>
    </ResultCardShell>
  );
}

export function ShenShaCard({ model }: { model: ShenShaViewModel }): ReactNode {
  if (!model.visible || model.items.length === 0) return null;

  return (
    <ResultCardShell
      title={model.title}
      titleId="rp-shensha-title"
      data-card="shen-sha"
      data-priority="3"
      className="rp-card--auto"
    >
      <ul className="rp-shensha">
        {model.items.map((item) => (
          <li key={item}>
            <PresentationText typeRole="body" clamp="subtitle" as="span">
              {item}
            </PresentationText>
          </li>
        ))}
      </ul>
    </ResultCardShell>
  );
}

function DetailRow({ label, values }: { label: string; values: readonly string[] }): ReactNode {
  return (
    <tr>
      <th scope="row">{label}</th>
      {values.map((value, index) => (
        <td key={`${label}-${index}`}>{value || "—"}</td>
      ))}
    </tr>
  );
}
