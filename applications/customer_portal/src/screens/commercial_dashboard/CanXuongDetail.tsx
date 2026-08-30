/**
 * Detailed Cân Xương section — same canonical object as the header summary.
 */

import type { ReactNode } from "react";
import { CAN_XUONG_EMPTY_COPY } from "./canXuongAdapter";
import type { IdentityFoundationView } from "./types";

type CanXuongDetailProps = {
  readonly foundation: IdentityFoundationView;
};

/**
 * S10-equivalent detail target for Commercial Dashboard `/result`.
 */
export function CanXuongDetail({ foundation }: CanXuongDetailProps): ReactNode {
  return (
    <section
      id="sec-can-xuong"
      className="bte-id__cx-detail"
      data-module="bone-weight-detail"
    >
      <p className="bte-id__cx-detail-title">Cân Xương Đoán Mệnh</p>
      {foundation.available ? (
        <>
          <p className="bte-id__cx-detail-weight">{foundation.displayWeight}</p>
          {foundation.classification ? (
            <p className="bte-id__cx-badge">{foundation.classification}</p>
          ) : null}
          <p className="bte-id__cx-detail-body">
            {foundation.interpretation || foundation.summary}
          </p>
        </>
      ) : (
        <p className="bte-id__cx-empty">{CAN_XUONG_EMPTY_COPY}</p>
      )}
    </section>
  );
}
