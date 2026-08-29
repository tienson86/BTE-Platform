/**
 * Identity Header region B — canonical Tứ Trụ summary via shared TuTruPanel.
 */

import type { ReactNode } from "react";
import { TuTruPanel } from "../../components/canonical";
import type { IdentityHeaderView } from "./types";

type FourPillarsProps = {
  readonly pillars: IdentityHeaderView["pillars"];
};

function toTuTruPillar(pillar: IdentityHeaderView["pillars"]["year"]) {
  return {
    canChi: pillar.canChi,
    napAm: pillar.napAm,
    cungPhi: pillar.cungPhi,
  };
}

/**
 * Tứ Trụ summary: Trụ / Can Chi / Nạp âm / Cung Phi. Not the Bát Tự detail table.
 */
export function FourPillars({ pillars }: FourPillarsProps): ReactNode {
  return (
    <div className="bte-id__pillars" data-region="pillars">
      <TuTruPanel
        className="bte-id__tu-tru"
        year={toTuTruPillar(pillars.year)}
        month={toTuTruPillar(pillars.month)}
        day={toTuTruPillar(pillars.day)}
        hour={toTuTruPillar(pillars.hour)}
      />
    </div>
  );
}
