/**
 * Identity Header regions A, C, and D.
 */

import type { ReactNode } from "react";
import { CAN_XUONG_EMPTY_COPY } from "./canXuongAdapter";
import type { IdentityFoundationView, IdentityPersonView, IdentityStatusView } from "./types";

type KvRow = { readonly label: string; readonly value: string };

function KvList({ rows }: { readonly rows: readonly KvRow[] }): ReactNode {
  return (
    <dl className="bte-id__kv">
      {rows.map((row) => (
        <div key={row.label} className="bte-id__kv-row">
          <dt>{row.label}</dt>
          <dd>{row.value || "—"}</dd>
        </div>
      ))}
    </dl>
  );
}

/**
 * Region A — personal identity, no analysis conclusions.
 */
export function IdentityPerson({ person }: { readonly person: IdentityPersonView }): ReactNode {
  return (
    <section className="bte-id__region" data-region="identity">
      <p className="bte-id__region-label">Định danh</p>
      <p className="bte-id__name">{person.fullName || "—"}</p>
      <KvList
        rows={[
          { label: "Giới tính", value: person.gender },
          { label: "Dương lịch", value: person.solarBirth },
          { label: "Âm lịch", value: person.lunarBirth },
          { label: "Giờ sinh", value: person.birthTime },
          { label: "Nơi sinh", value: person.birthPlace },
        ]}
      />
    </section>
  );
}

/**
 * Region C — Cân Xương Đoán Mệnh summary card.
 */
export function IdentityFoundation({
  foundation,
}: {
  readonly foundation: IdentityFoundationView;
}): ReactNode {
  if (!foundation.available) {
    return (
      <section
        className="bte-id__region bte-id__region--cx"
        data-region="foundation"
        data-module="bone-weight"
        data-can-xuong="empty"
      >
        <p className="bte-id__region-label">Cân Xương Đoán Mệnh</p>
        <p className="bte-id__cx-empty">{CAN_XUONG_EMPTY_COPY}</p>
      </section>
    );
  }
  return (
    <section
      className="bte-id__region bte-id__region--cx"
      data-region="foundation"
      data-module="bone-weight"
      data-can-xuong="summary"
    >
      <p className="bte-id__region-label">Cân Xương Đoán Mệnh</p>
      <p className="bte-id__cx-weight" data-slot="can-xuong-weight">
        {foundation.displayWeight}
      </p>
      {foundation.classification ? (
        <p className="bte-id__cx-badge" data-slot="can-xuong-class">
          {foundation.classification}
        </p>
      ) : null}
      {foundation.summary ? (
        <p className="bte-id__cx-summary" data-slot="can-xuong-summary">
          {foundation.summary}
        </p>
      ) : null}
      <a className="bte-id__cx-link" href={foundation.detailHref}>
        Xem chi tiết
      </a>
    </section>
  );
}

type TechRow = { readonly label: string; readonly value: string };

/**
 * Region D — compact technical metadata. UUID stays on one ellipsized line.
 */
export function IdentityStatus({ status }: { readonly status: IdentityStatusView }): ReactNode {
  const primary: TechRow[] = [
    { label: "Tam Nguyên", value: status.tamNguyen },
    { label: "Cửu Vận", value: status.cuuVan },
    { label: "Cung Phi", value: status.cungPhi },
    { label: "Mệnh Quái", value: status.menhQuai },
    { label: "Nhóm Trạch", value: status.nhomTrach },
    { label: "Tiết khí", value: status.tietKhi },
  ].filter((row) => row.value);
  return (
    <section className="bte-id__region bte-id__region--status" data-region="status">
      <p className="bte-id__region-label">Thông tin kỹ thuật</p>
      {primary.length > 0 ? (
        <dl className="bte-id__tech">
          {primary.map((row) => (
            <div key={row.label} className="bte-id__tech-row">
              <dt>{row.label}</dt>
              <dd>{row.value}</dd>
            </div>
          ))}
        </dl>
      ) : (
        <p className="bte-id__status-empty">—</p>
      )}
      <div className="bte-id__tech-meta">
        {status.analysisId ? (
          <p className="bte-id__tech-id" title={status.analysisId}>
            <span>Mã phân tích</span>
            <span data-slot="analysis-id">{status.analysisId}</span>
          </p>
        ) : null}
        {status.analyzedAt ? (
          <p className="bte-id__tech-when">
            <span>Ngày phân tích</span>
            <span>{status.analyzedAt}</span>
          </p>
        ) : null}
      </div>
    </section>
  );
}
