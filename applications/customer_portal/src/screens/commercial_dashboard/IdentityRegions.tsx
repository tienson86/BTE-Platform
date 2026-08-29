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
 * Region C — compact foundation badges.
 */
export function IdentityFoundation({
  foundation,
}: {
  readonly foundation: IdentityFoundationView;
}): ReactNode {
  return (
    <section className="bte-id__region" data-region="foundation">
      <p className="bte-id__region-label">Nền tảng</p>
      <KvList
        rows={[
          { label: "Cung Phi", value: foundation.cungPhi },
          { label: "Mệnh Quái", value: foundation.menhQuai },
          { label: "Nhóm Trạch", value: foundation.nhomTrach },
          { label: "Tiết khí", value: foundation.tietKhi },
        ]}
      />
    </section>
  );
}

/**
 * Region D — analysis id and date only. Version / Engine / Confidence stay off the header.
 */
export function IdentityStatus({ status }: { readonly status: IdentityStatusView }): ReactNode {
  const rows: KvRow[] = [];
  if (status.analysisId) rows.push({ label: "Mã phân tích", value: status.analysisId });
  if (status.analyzedAt) rows.push({ label: "Ngày phân tích", value: status.analyzedAt });
  return (
    <section className="bte-id__region bte-id__region--status" data-region="status">
      <p className="bte-id__region-label">Trạng thái</p>
      {rows.length > 0 ? <KvList rows={rows} /> : <p className="bte-id__status-empty">—</p>}
    </section>
  );
}
