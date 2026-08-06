/**
 * PortalPage — Desktop Canonical UI root.
 * Assembled against CANONICAL_PORTAL_UI_DESKTOP_V2.
 * Reuses approved S00–S11 modules. Does not redesign section internals.
 */

import type { ReactNode } from "react";
import { PortalFooter, PortalHeader, PortalSidebar } from "./shell/PortalChrome";
import {
  S00ContextHeader,
  S01IdentityDecision,
  S02OverviewActions,
  S03FourPillars,
  S04ElementBalance,
  S05Strength,
  S06TenGods,
  S07ShenSha,
  S08Interpretation,
  S09CungPhi,
  S10CanXuong,
  S11LearningPanel,
} from "./sections/Sections";
import "../../styles/canonical-desktop.css";

/**
 * Canonical Desktop Portal page (V2 layout shell).
 */
export function PortalPage(): ReactNode {
  return (
    <div className="cd-root" data-canonical="desktop-v2">
      <PortalSidebar />
      <PortalHeader />
      <main className="cd-content">
        <div className="cd-content__inner">
          {/* Row 1 — S00 full width */}
          <div className="cd-row cd-row--1">
            <S00ContextHeader />
          </div>

          {/* Row 2 — S01 | S02 | S09 — equal */}
          <div className="cd-row cd-row--3">
            <S01IdentityDecision />
            <S02OverviewActions />
            <S09CungPhi />
          </div>

          {/* Row 3 — S03(4) | S04(4) | S05(2) | S10(2) */}
          <div className="cd-row cd-row--4">
            <S03FourPillars />
            <S04ElementBalance />
            <S05Strength />
            <S10CanXuong />
          </div>

          {/* Row 4 — S06(4) | S07(2) | S08(3) | S11(3) */}
          <div className="cd-row cd-row--bottom">
            <S06TenGods />
            <S07ShenSha />
            <S08Interpretation />
            <S11LearningPanel />
          </div>
        </div>
      </main>
      <PortalFooter />
    </div>
  );
}
