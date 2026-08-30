/**
 * Sticky mobile bar for primary jumps. Hidden on desktop.
 */

import type { ReactNode } from "react";

/**
 * Thumb-zone shortcuts to Action and Interpretation.
 */
export function MobileActionBar(): ReactNode {
  return (
    <nav className="bte-mobile-bar" data-mobile="action-bar" aria-label="Thao tác nhanh">
      <a className="bte-mobile-bar__btn" href="#bte-card-action-plan" data-thumb-zone="true">
        Kế hoạch
      </a>
      <a className="bte-mobile-bar__btn" href="#bte-card-interpretation" data-thumb-zone="true">
        Luận giải
      </a>
    </nav>
  );
}
