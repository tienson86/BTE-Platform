import type { ReactNode } from "react";

import {
  IconBell,
  IconMenu,
  IconStarLogo,
  IconSun,
} from "../../../screens/canonical_desktop/icons";
import type { WorkspacePersonView } from "../adapter/types";
import { EMPTY_COPY, NO_RESULT_COPY } from "../catalog";
import { WORKSPACE_PANELS, WORKSPACE_TOP_NAV } from "../layout";

/**
 * Product top navigation — chrome only, no result data.
 */
export function WorkspaceTopNav(): ReactNode {
  return (
    <header className="bte-rw__topnav" role="banner" data-chrome="top-nav">
      <button type="button" className="bte-rw__icon-btn bte-rw__menu-toggle" aria-label="Menu" data-rw-toggle="sidebar">
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

function HeaderValue({
  slot,
  label,
  value,
  preview,
}: {
  slot: string;
  label: string;
  value?: string | null;
  preview?: boolean;
}): ReactNode {
  const ready = Boolean(value);
  return (
    <div className="bte-rw__context-item" data-slot={slot}>
      <dt>{label}</dt>
      <dd data-placeholder={ready ? "false" : "true"} data-preview={preview ? "fixture" : undefined}>
        {ready ? value : EMPTY_COPY}
      </dd>
    </div>
  );
}

/**
 * Workspace page header — customer identity first, analysis id secondary.
 */
export function WorkspaceHeader({
  person,
  preview = false,
  noResult = false,
}: {
  person?: WorkspacePersonView;
  preview?: boolean;
  noResult?: boolean;
}): ReactNode {
  const hasResult = Boolean(
    !noResult && (person?.name.value || person?.analysisId.value || person?.solarDate.value),
  );
  const status = preview ? "Bản xem trước" : hasResult ? "Đã phân tích" : "";
  return (
    <div className="bte-rw__page-header" data-chrome="header">
      <div className="bte-rw__hero">
        <h1 className="bte-rw__page-title">Kết quả luận giải Bát Tự</h1>
        {noResult ? (
          <p className="bte-rw__no-result" data-empty-page="true">
            {NO_RESULT_COPY}
          </p>
        ) : null}
        <dl className="bte-rw__hero-id">
          <HeaderValue
            slot="profile"
            label="Khách hàng"
            preview={preview}
            value={preview ? "Bản xem trước" : person?.name.value}
          />
          <div className="bte-rw__birthline">
            <HeaderValue
              slot="gender"
              label="Giới tính"
              preview={preview}
              value={preview ? "" : person?.gender.value}
            />
            <HeaderValue
              slot="solar-date"
              label="Ngày sinh"
              preview={preview}
              value={preview ? "" : person?.solarDate.value}
            />
            <HeaderValue
              slot="birth-time"
              label="Giờ sinh"
              preview={preview}
              value={preview ? "" : person?.birthTime.value}
            />
          </div>
          <HeaderValue
            slot="lunar-date"
            label="Âm lịch"
            preview={preview}
            value={preview ? "" : person?.lunarDate.value}
          />
        </dl>
      </div>
      <dl className="bte-rw__context">
        <HeaderValue
          slot="status"
          label="Trạng thái"
          preview={preview}
          value={status}
        />
        <HeaderValue
          slot="chart-id"
          label="Mã phân tích"
          preview={preview}
          value={preview ? "preview" : person?.analysisId.value}
        />
        <HeaderValue
          slot="location"
          label="Nơi sinh"
          preview={preview}
          value={preview ? "" : person?.location.value}
        />
        <HeaderValue
          slot="timezone"
          label="Múi giờ"
          preview={preview}
          value={preview ? "" : person?.timezone.value}
        />
      </dl>
    </div>
  );
}
