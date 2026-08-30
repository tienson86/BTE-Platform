import { useId, type ReactNode } from "react";

import { cx } from "../../utils";
import { cungPhiBadgeToken, napAmBadgeToken } from "./tokens";
import {
  TU_TRU_COLUMNS,
  TU_TRU_ROWS,
  TU_TRU_TITLE,
  type TuTruPanelProps,
  type TuTruPillar,
  type TuTruRowKey,
} from "./types";

const EMPTY = "—";

/**
 * Colored badge for a supplied Nạp âm or Cung Phi label.
 */
function TuTruBadge({
  value,
  kind,
}: {
  value: string;
  kind: "nap-am" | "cung-phi";
}): ReactNode {
  const label = value.trim();
  if (!label) {
    return <span className="bte-tu-tru__empty">{EMPTY}</span>;
  }
  const token = kind === "nap-am" ? napAmBadgeToken(label) : cungPhiBadgeToken(label);
  return (
    <span
      className={cx("bte-tu-tru__badge", token ? `bte-tu-tru__badge--${token}` : "bte-tu-tru__badge--neutral")}
      data-kind={kind}
    >
      {label}
    </span>
  );
}

/**
 * One Tứ Trụ data row. Renders supplied labels only.
 */
function TuTruRow({
  label,
  pillar,
  rowKey,
}: {
  label: string;
  pillar: TuTruPillar;
  rowKey: TuTruRowKey;
}): ReactNode {
  const canChi = pillar.canChi.trim() || EMPTY;
  return (
    <tr data-pillar={rowKey}>
      <th scope="row">{label}</th>
      <td className="bte-tu-tru__can-chi">{canChi}</td>
      <td>
        <TuTruBadge value={pillar.napAm} kind="nap-am" />
      </td>
      <td>
        <TuTruBadge value={pillar.cungPhi} kind="cung-phi" />
      </td>
    </tr>
  );
}

/**
 * Canonical Tứ Trụ panel for the BTE Platform.
 *
 * Renders Năm / Tháng / Ngày / Giờ with Can Chi, Nạp âm, and Cung Phi.
 * The component does not calculate or transform identity fields.
 */
export function TuTruPanel({
  year,
  month,
  day,
  hour,
  className,
}: TuTruPanelProps): ReactNode {
  const titleId = useId();
  const pillars: Record<TuTruRowKey, TuTruPillar> = { year, month, day, hour };
  return (
    <section
      className={cx("bte-tu-tru", className)}
      data-canonical="tu-tru-panel"
      data-testid="tu-tru-panel"
      aria-labelledby={titleId}
    >
      <h3 id={titleId} className="bte-tu-tru__title">
        {TU_TRU_TITLE}
      </h3>
      <table className="bte-tu-tru__table">
        <thead>
          <tr>
            <th className="bte-tu-tru__corner" scope="col">
              Trụ
            </th>
            {TU_TRU_COLUMNS.map((column) => (
              <th key={column} scope="col">
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {TU_TRU_ROWS.map((row) => (
            <TuTruRow key={row.key} label={row.label} rowKey={row.key} pillar={pillars[row.key]} />
          ))}
        </tbody>
      </table>
    </section>
  );
}
