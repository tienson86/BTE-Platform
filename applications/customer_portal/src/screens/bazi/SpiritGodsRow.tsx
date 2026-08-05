import { memo, type ReactNode } from "react";
import { Card } from "../../components/base/Card";
import { BaseText } from "../../components/base/BaseText";
import type { BaZiSpiritGod } from "./mockData";

export type SpiritGodsRowProps = {
  gods: readonly BaZiSpiritGod[];
};

/** Glance cards for Dụng / Kỵ Thần beside Strength (Canonical L3 accent). */
export const SpiritGodsRow = memo(function SpiritGodsRow({
  gods,
}: SpiritGodsRowProps): ReactNode {
  if (gods.length === 0) {
    return null;
  }

  return (
    <div className="cui-bazi-spirits" aria-label="Dụng Thần · Kỵ Thần">
      {gods.map((god) => (
        <Card
          key={god.id}
          className="cui-bazi-spirit"
          data-role={god.role}
          data-element={god.element}
        >
          <BaseText variant="caption" tone="muted">
            {god.roleLabel}
          </BaseText>
          <BaseText variant="section">{god.name}</BaseText>
        </Card>
      ))}
    </div>
  );
});
