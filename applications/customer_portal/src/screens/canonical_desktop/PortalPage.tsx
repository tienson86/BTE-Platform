/**
 * PortalPage — Desktop Canonical UI root.
 * Built from scratch against CANONICAL_PORTAL_UI_DESKTOP_V1.png.
 * Does not reuse legacy Portal layout or BaZiResultScreen.
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
 * Canonical Desktop Portal page.
 */
export function PortalPage(): ReactNode {
  return (
    <div className="cd-root" data-canonical="desktop-v1">
      <PortalSidebar />
      <PortalHeader />
      <main className="cd-content">
        <S00ContextHeader />

        <div className="cd-row cd-row--3">
          <S01IdentityDecision />
          <S02OverviewActions />
          <S09CungPhi />
        </div>

        <div className="cd-row cd-row--4">
          <S03FourPillars />
          <S04ElementBalance />
          <S05Strength />
          <S10CanXuong />
        </div>

        <div className="cd-row cd-row--bottom">
          <S06TenGods />
          <S07ShenSha />
          <S08Interpretation />
          <S11LearningPanel />
        </div>
      </main>
      <PortalFooter />
    </div>
  );
}
