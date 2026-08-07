/**
 * Sprint B stubs — zone shells only (Phase 01 architecture extraction).
 */

import type { ReactNode } from "react";
import { ResultGrid, ResultGridCell, ResultRow } from "../layout";

/**
 * RecommendationZone — Row 05 shell (LP-005 deferred to Sprint B).
 */
export function RecommendationZone(): ReactNode {
  return (
    <ResultRow
      rowId="05"
      zone="recommendation"
      heightClass="L"
      pattern="LP-005"
      aria-label="Recommendation Zone"
      data-sprint="B"
    >
      <ResultGrid>
        <ResultGridCell span={12}>
          <article className="rp-card rp-card--stub" data-card="recommendation">
            <h2 className="rp-card__title">KHUYẾN NGHỊ</h2>
            <p className="rp-card__summary">Sprint B — LP-005</p>
          </article>
        </ResultGridCell>
      </ResultGrid>
    </ResultRow>
  );
}

/**
 * InterpretationZone — Row 06 shell (LP-006 deferred to Sprint B).
 */
export function InterpretationZone(): ReactNode {
  return (
    <ResultRow
      rowId="06"
      zone="interpretation"
      heightClass="AUTO"
      pattern="LP-006"
      aria-label="Interpretation Zone"
      data-sprint="B"
    >
      <ResultGrid>
        <ResultGridCell span={12}>
          <article className="rp-card rp-card--stub rp-card--auto" data-card="interpretation">
            <h2 className="rp-card__title">LUẬN GIẢI</h2>
            <p className="rp-card__summary">Sprint B — LP-006</p>
          </article>
        </ResultGridCell>
      </ResultGrid>
    </ResultRow>
  );
}

/**
 * KnowledgeZone — Row 07 shell (LP-007 deferred to Sprint B).
 */
export function KnowledgeZone(): ReactNode {
  return (
    <ResultRow
      rowId="07"
      zone="knowledge"
      heightClass="AUTO"
      pattern="LP-007"
      aria-label="Knowledge Zone"
      data-sprint="B"
    >
      <ResultGrid>
        <ResultGridCell span={12}>
          <article className="rp-card rp-card--stub rp-card--auto" data-card="knowledge">
            <h2 className="rp-card__title">KIẾN THỨC</h2>
            <p className="rp-card__summary">Sprint B — LP-007</p>
          </article>
        </ResultGridCell>
      </ResultGrid>
    </ResultRow>
  );
}
