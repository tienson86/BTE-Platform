/**
 * Full-width Identity Header (not a Card).
 */

import type { ReactNode } from "react";
import { FourPillars } from "./FourPillars";
import { IdentityFoundation, IdentityPerson, IdentityStatus } from "./IdentityRegions";
import type { IdentityHeaderView } from "./types";

type IdentityHeaderProps = {
  readonly model: IdentityHeaderView;
};

/**
 * Canonical Identity Header with regions A / B / C / D.
 */
export function IdentityHeader({ model }: IdentityHeaderProps): ReactNode {
  return (
    <header className="bte-id" data-identity-header="true">
      <IdentityPerson person={model.person} />
      <FourPillars pillars={model.pillars} dayMaster={model.dayMaster} />
      <IdentityFoundation foundation={model.foundation} />
      <IdentityStatus status={model.status} />
    </header>
  );
}
