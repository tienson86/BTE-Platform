/**
 * Identity Header regions A, C, and D.
 */

import type { ReactNode } from "react";
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
 * Region C — Cân Xương Đoán Mệnh (replaces the former Foundation summary).
 */
export function IdentityFoundation({
  foundation,
}: {
  readonly foundation: IdentityFoundationView;
}): ReactNode {
  return (
    <section className="bte-id__region" data-region="foundation" data-module="bone-weight">
      <p className="bte-id__region-label">Cân Xương Đoán Mệnh</p>
      <KvList
        rows={[
          { label: "Cân lượng", value: foundation.weight },
          { label: "Phân loại", value: foundation.classification },
          { label: "Đánh giá", value: foundation.rating },
          { label: "Tóm tắt", value: foundation.summary },
        ]}
      />
    </section>
  );
}

/**
 * Region D — analysis id plus technical calendar / Cung Phi metadata.
 */
export function IdentityStatus({ status }: { readonly status: IdentityStatusView }): ReactNode {
  const rows: KvRow[] = [];
  if (status.analysisId) rows.push({ label: "Mã phân tích", value: status.analysisId });
  if (status.analyzedAt) rows.push({ label: "Ngày phân tích", value: status.analyzedAt });
  if (status.tamNguyen) rows.push({ label: "Tam Nguyên", value: status.tamNguyen });
  if (status.cuuVan) rows.push({ label: "Cửu Vận", value: status.cuuVan });
  if (status.cungPhi) rows.push({ label: "Cung Phi", value: status.cungPhi });
  if (status.menhQuai) rows.push({ label: "Mệnh Quái", value: status.menhQuai });
  if (status.nhomTrach) rows.push({ label: "Nhóm Trạch", value: status.nhomTrach });
  if (status.tietKhi) rows.push({ label: "Tiết khí", value: status.tietKhi });
  return (
    <section className="bte-id__region bte-id__region--status" data-region="status">
      <p className="bte-id__region-label">Thông tin kỹ thuật</p>
      {rows.length > 0 ? <KvList rows={rows} /> : <p className="bte-id__status-empty">—</p>}
    </section>
  );
}
