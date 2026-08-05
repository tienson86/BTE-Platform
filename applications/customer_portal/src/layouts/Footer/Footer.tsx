import type { ReactNode } from "react";
import { cx } from "../../utils";

/** Portal product version shown in footer (presentation only). */
const PORTAL_VERSION = "1.0.0";

export type FooterProps = {
  version?: string;
  className?: string;
};

/** Application footer — version, copyright, support placeholder (WP03). */
export function Footer({
  version = PORTAL_VERSION,
  className,
}: FooterProps): ReactNode {
  const year = new Date().getFullYear();
  return (
    <footer className={cx("cui-app-footer", className)} role="contentinfo">
      <p className="cui-app-footer__meta">
        BTE Platform v{version} · © {year} BTE
      </p>
      <a className="cui-app-footer__support" href="/support">
        Hỗ trợ
      </a>
    </footer>
  );
}
