/**
 * Four Pillars table for Identity Header region B.
 */

import type { ReactNode } from "react";
import type { IdentityDayMasterView, IdentityHeaderView } from "./types";

const PILLAR_KEYS = ["year", "month", "day", "hour"] as const;
const PILLAR_LABELS = ["Năm", "Tháng", "Ngày", "Giờ"] as const;

type FourPillarsProps = {
  readonly pillars: IdentityHeaderView["pillars"];
  readonly dayMaster: IdentityDayMasterView;
};

function display(value: string): string {
  return value || "—";
}

function dayMasterCaption(dayMaster: IdentityDayMasterView): string {
  return [dayMaster.stem, dayMaster.element, dayMaster.yinYang].filter(Boolean).join(" · ");
}

/**
 * Traditional 4-column Thiên Can / Địa Chi / Nạp Âm table.
 */
export function FourPillars({ pillars, dayMaster }: FourPillarsProps): ReactNode {
  return (
    <div className="bte-id__pillars" data-region="pillars">
      <p className="bte-id__region-label">Tứ trụ</p>
      <table className="bte-id__table">
        <thead>
          <tr>
            <th scope="col" className="bte-id__corner" />
            {PILLAR_LABELS.map((label, index) => {
              const key = PILLAR_KEYS[index]!;
              return (
                <th
                  key={key}
                  scope="col"
                  data-pillar={key}
                  data-day-master={key === "day" ? "true" : undefined}
                >
                  {label}
                </th>
              );
            })}
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">Thiên Can</th>
            {PILLAR_KEYS.map((key) => (
              <td
                key={`stem-${key}`}
                data-pillar={key}
                data-row="stem"
                data-day-master={key === "day" ? "true" : undefined}
              >
                {display(pillars[key].stem)}
              </td>
            ))}
          </tr>
          <tr>
            <th scope="row">Địa Chi</th>
            {PILLAR_KEYS.map((key) => (
              <td key={`branch-${key}`} data-pillar={key} data-row="branch">
                {display(pillars[key].branch)}
              </td>
            ))}
          </tr>
          <tr>
            <th scope="row">Nạp Âm</th>
            {PILLAR_KEYS.map((key) => (
              <td key={`nap-${key}`} data-pillar={key} data-row="nap-am" data-nap-am="">
                {display(pillars[key].napAm)}
              </td>
            ))}
          </tr>
          <tr className="bte-id__dm-row">
            <th scope="row" />
            {PILLAR_KEYS.map((key) => (
              <td
                key={`dm-${key}`}
                data-pillar={key}
                data-day-master={key === "day" ? "true" : undefined}
              >
                {key === "day" ? "NHẬT CHỦ" : ""}
              </td>
            ))}
          </tr>
        </tbody>
      </table>
      {dayMaster.stem ? (
        <p className="bte-id__day-master" data-day-master-summary="">
          Nhật chủ {dayMasterCaption(dayMaster)}
        </p>
      ) : null}
    </div>
  );
}
