import type { ReactNode } from "react";

export function ExpertDetails(): ReactNode {
  return (
    <section
      className="bte-card ne-expert"
      data-section="P-S11"
      data-testid="expert-details"
      data-expert-seam="static-placeholder"
      hidden
      aria-hidden="true"
      inert
    >
      <h2>Chi tiết chuyên gia</h2>
      <p data-testid="expert-seam-note">
        Khe kiểm tra cho bước sau. Đây chưa phải liên kết với kết quả vận hành thực.
      </p>
    </section>
  );
}
