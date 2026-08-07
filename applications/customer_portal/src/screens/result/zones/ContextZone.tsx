/**
 * ContextZone — Row 01 (PACK_07). Height S.
 */

import type { ReactNode } from "react";
import { PresentationText } from "../../../components/shared/PresentationText";
import { ResultGrid, ResultGridCell, ResultRow } from "../layout";
import { useResultPageViewModel } from "../ResultPageContext";

/**
 * Context information strip — who / birth / chart / status.
 */
export function ContextZone(): ReactNode {
  const { context } = useResultPageViewModel();

  return (
    <ResultRow
      rowId="01"
      zone="context"
      heightClass="S"
      aria-label="Context Zone"
    >
      <ResultGrid>
        <ResultGridCell span={12}>
          <article className="rp-card rp-card--context" data-card="context" aria-labelledby="rp-context-title">
            <PresentationText
              as="h2"
              id="rp-context-title"
              typeRole="title"
              clamp="title"
              className="rp-card__title"
            >
              {context.title}
            </PresentationText>
            <div className="rp-context">
              <div className="rp-context__col">
                <PresentationText typeRole="caption" as="div">
                  Hồ sơ
                </PresentationText>
                <PresentationText typeRole="subtitle" clamp="subtitle" as="div">
                  {context.profileName}
                </PresentationText>
                <PresentationText typeRole="summary" clamp="summary" as="div">
                  {context.profileMeta}
                </PresentationText>
              </div>
              <div className="rp-context__col">
                <PresentationText typeRole="caption" as="div">
                  Ngày giờ sinh
                </PresentationText>
                <PresentationText typeRole="subtitle" clamp="subtitle" as="div">
                  {context.birthDate}
                </PresentationText>
                <PresentationText typeRole="summary" clamp="summary" as="div">
                  {context.birthLunar} · {context.birthTime}
                </PresentationText>
              </div>
              <div className="rp-context__col">
                <PresentationText typeRole="caption" as="div">
                  Mã lá số
                </PresentationText>
                <PresentationText typeRole="subtitle" clamp="subtitle" as="div">
                  {context.chartId}
                </PresentationText>
              </div>
              <div className="rp-context__col">
                <PresentationText typeRole="caption" as="div">
                  Trạng thái
                </PresentationText>
                <PresentationText typeRole="subtitle" clamp="subtitle" as="div">
                  {context.status}
                </PresentationText>
                <PresentationText typeRole="summary" clamp="summary" as="div">
                  {context.analyzedAt}
                </PresentationText>
              </div>
            </div>
          </article>
        </ResultGridCell>
      </ResultGrid>
    </ResultRow>
  );
}
