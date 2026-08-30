/**
 * ContextZone — Row 01 Identity hero (Product Polish V1).
 * Metadata demoted to secondary expandable details.
 */

import { useId, useState, type ReactNode } from "react";
import { PresentationText } from "../../../components/shared/PresentationText";
import { ResultGrid, ResultGridCell, ResultRow } from "../layout";
import { useResultPageViewModel } from "../ResultPageContext";

/**
 * Identity-first context — who is this consultation for.
 */
export function ContextZone(): ReactNode {
  const { context } = useResultPageViewModel();
  const [metaOpen, setMetaOpen] = useState(false);
  const metaId = useId();

  return (
    <ResultRow
      rowId="01"
      zone="context"
      heightClass="AUTO"
      aria-label="Identity Zone"
      data-priority="1"
    >
      <ResultGrid>
        <ResultGridCell span={12}>
          <article
            className="rp-card rp-card--context rp-card--identity-hero"
            data-card="context"
            data-question="who-am-i"
            aria-labelledby="rp-context-title"
          >
            <PresentationText
              as="p"
              typeRole="caption"
              className="rp-identity__eyebrow"
            >
              {context.identityLabel}
            </PresentationText>
            <PresentationText
              as="h2"
              id="rp-context-title"
              typeRole="title"
              clamp="title"
              className="rp-card__title rp-identity__title"
            >
              {context.title}
            </PresentationText>
            <PresentationText
              typeRole="metric"
              as="p"
              className="rp-identity__name"
            >
              {context.profileName}
            </PresentationText>
            {context.profileMeta ? (
              <PresentationText
                typeRole="body"
                clamp="summary"
                as="p"
                className="rp-identity__meta"
              >
                {context.profileMeta}
              </PresentationText>
            ) : null}
            <div className="rp-identity__birth">
              <PresentationText typeRole="subtitle" clamp="subtitle" as="span">
                {context.birthDate}
              </PresentationText>
              <PresentationText typeRole="summary" clamp="summary" as="span">
                {context.birthLunar} · {context.birthTime}
              </PresentationText>
            </div>

            <button
              type="button"
              className="rp-expand-btn rp-identity__meta-toggle"
              aria-expanded={metaOpen}
              aria-controls={metaId}
              onClick={() => setMetaOpen((value) => !value)}
            >
              {metaOpen ? "Ẩn thông tin kỹ thuật" : "Thông tin kỹ thuật"}
            </button>
            {metaOpen ? (
              <dl id={metaId} className="rp-identity__tech">
                <div>
                  <dt>Mã lá số</dt>
                  <dd>{context.chartId}</dd>
                </div>
                <div>
                  <dt>Trạng thái</dt>
                  <dd>{context.status}</dd>
                </div>
                <div>
                  <dt>Thời điểm phân tích</dt>
                  <dd>{context.analyzedAt}</dd>
                </div>
                {context.tamNguyen ? (
                  <div>
                    <dt>Tam Nguyên</dt>
                    <dd>{context.tamNguyen}</dd>
                  </div>
                ) : null}
                {context.cuuVan ? (
                  <div>
                    <dt>Cửu Vận</dt>
                    <dd>{context.cuuVan}</dd>
                  </div>
                ) : null}
                {context.cungPhi ? (
                  <div>
                    <dt>Cung Phi</dt>
                    <dd>{context.cungPhi}</dd>
                  </div>
                ) : null}
                {context.menhQuai ? (
                  <div>
                    <dt>Mệnh Quái</dt>
                    <dd>{context.menhQuai}</dd>
                  </div>
                ) : null}
                {context.nhomTrach ? (
                  <div>
                    <dt>Nhóm Trạch</dt>
                    <dd>{context.nhomTrach}</dd>
                  </div>
                ) : null}
              </dl>
            ) : null}
          </article>
        </ResultGridCell>
      </ResultGrid>
    </ResultRow>
  );
}
