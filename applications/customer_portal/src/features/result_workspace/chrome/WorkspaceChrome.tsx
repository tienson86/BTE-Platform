import type { ReactNode } from "react";

import {
  IconBell,
  IconMenu,
  IconStarLogo,
  IconSun,
} from "../../../screens/canonical_desktop/icons";
import { WORKSPACE_PANELS, WORKSPACE_TOP_NAV } from "../layout";

/**
 * Product top navigation — chrome only, no result data.
 */
export function WorkspaceTopNav(): ReactNode {
  return (
    <header className="bte-rw__topnav" role="banner" data-chrome="top-nav">
      <button type="button" className="bte-rw__icon-btn bte-rw__menu-toggle" aria-label="Menu">
        <IconMenu size={20} />
      </button>
      <nav className="bte-rw__nav" aria-label="Điều hướng chính">
        {WORKSPACE_TOP_NAV.map((item) => (
          <a
            key={item.id}
            href={item.href}
            className={item.active ? "bte-rw__nav-link bte-rw__nav-link--active" : "bte-rw__nav-link"}
            data-nav={item.id}
          >
            {item.label}
          </a>
        ))}
      </nav>
      <div className="bte-rw__utils">
        <button type="button" className="bte-rw__icon-btn" aria-label="Chế độ sáng">
          <IconSun size={18} />
        </button>
        <button type="button" className="bte-rw__icon-btn" aria-label="Thông báo">
          <IconBell size={18} />
        </button>
        <div className="bte-rw__user" data-slot="user">
          <div className="bte-rw__avatar" aria-hidden="true">
            BT
          </div>
          <div className="bte-rw__user-meta">
            <span className="bte-rw__user-name">Tài khoản</span>
            <span className="bte-rw__user-role">BTE Portal</span>
          </div>
        </div>
      </div>
    </header>
  );
}

/**
 * Left sidebar — panel map, not a data surface.
 */
export function WorkspaceSidebar(): ReactNode {
  return (
    <aside className="bte-rw__sidebar" aria-label="Thanh bên" data-chrome="sidebar">
      <div className="bte-rw__brand">
        <IconStarLogo className="bte-rw__logo" />
        <span className="bte-rw__brand-text">BTE Portal</span>
      </div>
      <div className="bte-rw__sidebar-group">
        <div className="bte-rw__sidebar-title">Lá số</div>
        <ul className="bte-rw__sidebar-nav">
          {WORKSPACE_PANELS.map((panel) => (
            <li key={panel.id}>
              <a className="bte-rw__sidebar-link" href={`#panel-${panel.id}`}>
                {panel.title}
              </a>
            </li>
          ))}
        </ul>
      </div>
      <div className="bte-rw__sidebar-foot">
        <div>BTE Platform v1.0.0</div>
        <div>Result Workspace V2</div>
      </div>
    </aside>
  );
}

/**
 * Workspace page header — reserved context slots, no bound chart values.
 */
export function WorkspaceHeader(): ReactNode {
  return (
    <div className="bte-rw__page-header" data-chrome="header">
      <div>
        <p className="bte-rw__eyebrow">BaZi Result Workspace V2</p>
        <h1 className="bte-rw__page-title">Kết quả Bát Tự</h1>
      </div>
      <dl className="bte-rw__context">
        <div className="bte-rw__context-item" data-slot="profile">
          <dt>Hồ sơ</dt>
          <dd data-placeholder="true">Chờ dữ liệu</dd>
        </div>
        <div className="bte-rw__context-item" data-slot="chart-id">
          <dt>Mã lá số</dt>
          <dd data-placeholder="true">Chờ dữ liệu</dd>
        </div>
        <div className="bte-rw__context-item" data-slot="status">
          <dt>Trạng thái</dt>
          <dd data-placeholder="true">Chờ dữ liệu</dd>
        </div>
      </dl>
    </div>
  );
}
