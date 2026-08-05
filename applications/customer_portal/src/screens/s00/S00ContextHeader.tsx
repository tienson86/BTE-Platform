/**
 * S00 Context Header — Canonical Desktop (from scratch).
 * Visual source of truth: knowledge/ui_reference/CANONICAL_PORTAL_UI.png
 * Does not use or modify the legacy portal AppLayout / BaZiResultScreen.
 */

import type { ReactNode } from "react";

const NAV_ITEMS = [
  "Trang chủ",
  "Luận giải",
  "Kết quả",
  "Báo cáo",
  "Lịch sử",
  "Tài khoản",
  "Đăng nhập",
] as const;

/**
 * S00 — Context Header
 * Left: Brand + menu · Center: Primary nav · Right: Theme + avatar
 */
export function S00ContextHeader(): ReactNode {
  return (
    <header className="s00-header" data-section="s00-context" aria-label="S00 Context Header">
      <div className="s00-header__left">
        <div className="s00-header__brand">
          <span className="s00-header__brand-bte">BTE</span>
          <span className="s00-header__brand-portal"> Portal</span>
        </div>
        <button type="button" className="s00-header__menu" aria-label="Menu" tabIndex={0}>
          <span className="s00-header__menu-bar" />
          <span className="s00-header__menu-bar" />
          <span className="s00-header__menu-bar" />
        </button>
      </div>

      <nav className="s00-header__center" aria-label="Primary">
        {NAV_ITEMS.map((label) => {
          const active = label === "Kết quả";
          return (
            <a
              key={label}
              href="#"
              className={
                active ? "s00-header__nav-link s00-header__nav-link--active" : "s00-header__nav-link"
              }
              aria-current={active ? "page" : undefined}
            >
              {label}
            </a>
          );
        })}
      </nav>

      <div className="s00-header__right">
        <button type="button" className="s00-header__theme" aria-label="Chế độ sáng">
          <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
            <circle cx="12" cy="12" r="4" fill="currentColor" />
            <g stroke="currentColor" strokeWidth="1.6" strokeLinecap="round">
              <line x1="12" y1="2" x2="12" y2="5" />
              <line x1="12" y1="19" x2="12" y2="22" />
              <line x1="2" y1="12" x2="5" y2="12" />
              <line x1="19" y1="12" x2="22" y2="12" />
              <line x1="4.2" y1="4.2" x2="6.3" y2="6.3" />
              <line x1="17.7" y1="17.7" x2="19.8" y2="19.8" />
              <line x1="4.2" y1="19.8" x2="6.3" y2="17.7" />
              <line x1="17.7" y1="6.3" x2="19.8" y2="4.2" />
            </g>
          </svg>
        </button>
        <div className="s00-header__avatar" aria-label="NV">
          NV
        </div>
      </div>
    </header>
  );
}
