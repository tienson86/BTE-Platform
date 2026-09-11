import type { ReactNode } from "react";

import {
  ENERGY_COUNT_SCALE,
  ENERGY_ROLE_LABEL,
  GOLDEN_ENERGY_DISTRIBUTION,
} from "../goldenDistribution";

export function EnergyDistribution(): ReactNode {
  return (
    <section className="bte-card ne-distribution" data-section="P-S05" data-testid="energy-distribution">
      <h2>Cấu trúc trường khí</h2>
      <p className="muted">Tám trường khí xuất hiện trong dãy và mức độ lặp lại. Số lần xuất hiện không phải điểm số.</p>
      <ol className="ne-dist-list" data-testid="energy-distribution-list">
        {GOLDEN_ENERGY_DISTRIBUTION.map((energy, index) => {
          const roleLabel = ENERGY_ROLE_LABEL[energy.role];
          return (
            <li
              key={energy.label}
              className="ne-dist-row"
              data-testid={`dist-row-${index}`}
              data-energy-label={energy.label}
              data-energy-role={energy.role}
            >
              <span className="ne-dist-name" data-testid={`dist-name-${index}`}>
                {energy.label}
              </span>
              <span className="ne-dist-bar" aria-hidden="true">
                {Array.from({ length: ENERGY_COUNT_SCALE }, (_, tick) => (
                  <span
                    key={`${energy.label}-tick-${tick}`}
                    className="ne-dist-tick"
                    data-filled={tick < energy.count ? "true" : "false"}
                  />
                ))}
              </span>
              <span className="ne-dist-count" data-testid={`dist-count-${index}`}>
                {energy.count}
              </span>
              {roleLabel ? (
                <span className="ne-dist-role" data-testid={`dist-role-${index}`}>
                  {roleLabel}
                </span>
              ) : (
                <span className="ne-dist-role ne-dist-role--empty" />
              )}
            </li>
          );
        })}
      </ol>
      <p className="muted ne-dist-note">
        Ý nghĩa cuối cùng còn phụ thuộc vào vị trí và cách các trường khí kết hợp.
      </p>
    </section>
  );
}
