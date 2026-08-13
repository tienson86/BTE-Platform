import type { MouseEvent, ReactNode } from "react";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";
import {
  IconBell,
  IconMenu,
  IconSun,
  SidebarIcon,
  IconStarLogo,
} from "../icons";

const HEADER_NAV_HREF: Record<string, string> = {
  home: "/dashboard",
  analysis: "/result#interpretation",
  result: "/result",
  report: "/reports",
  history: "/history",
  account: "/profile",
  guide: "/dashboard",
};

const SIDEBAR_NAV_HREF: Record<string, string> = {
  "tom-tat": "#summary",
  "bat-tu": "#analysis",
  "bieu-do": "#visualization",
  "phan-tich": "#analysis",
  "luan-giai": "#interpretation",
  "kien-thuc": "#knowledge",
  "so-sanh": "/history",
  "luu-tru": "/history",
  xuat: "#xuat",
};

function hrefForNav(id: string, table: Record<string, string>): string {
  return table[id] ?? `#${id}`;
}

function handleCanonicalNav(event: MouseEvent<HTMLAnchorElement>, href: string): void {
  if (href !== "#xuat") return;
  event.preventDefault();
  window.print();
}

export function PortalHeader(): ReactNode {
  const data = useCanonicalDesktop();
  return (
    <header className="cd-header" role="banner">
      <button type="button" className="cd-header__toggle" aria-label="Menu">
        <IconMenu size={20} />
      </button>
      <nav className="cd-header__nav" aria-label="Điều hướng chính">
        {data.header.nav.map((item) => {
          const href = hrefForNav(item.id, HEADER_NAV_HREF);
          return (
          <a
            key={item.id}
            href={href}
            onClick={(event) => handleCanonicalNav(event, href)}
            className={
              item.active ? "cd-header__link cd-header__link--active" : "cd-header__link"
            }
          >
            {item.label}
          </a>
          );
        })}
      </nav>
      <div className="cd-header__utils">
        <button type="button" className="cd-header__icon-btn" aria-label="Chế độ sáng">
          <IconSun size={18} />
        </button>
        <button type="button" className="cd-header__icon-btn" aria-label="Thông báo">
          <IconBell size={18} />
          <span className="cd-header__badge">{data.header.notifications}</span>
        </button>
        <div className="cd-header__user">
          <div className="cd-header__avatar" aria-hidden="true">
            {data.header.user.initials}
          </div>
          <div className="cd-header__user-meta">
            <span className="cd-header__user-name">{data.header.user.name}</span>
            <span className="cd-header__user-role">{data.header.user.role}</span>
          </div>
        </div>
      </div>
    </header>
  );
}

export function PortalSidebar(): ReactNode {
  const data = useCanonicalDesktop();
  return (
    <aside className="cd-sidebar" aria-label="Thanh bên">
      <div className="cd-sidebar__brand">
        <IconStarLogo className="cd-sidebar__logo" />
        <span className="cd-sidebar__brand-text">{data.sidebar.brand}</span>
        <button type="button" className="cd-sidebar__menu-btn" aria-label="Thu gọn">
          <IconMenu size={18} />
        </button>
      </div>

      {data.sidebar.groups.map((group) => (
        <div key={group.title} className="cd-sidebar__group">
          <div className="cd-sidebar__group-title">{group.title}</div>
          <ul className="cd-sidebar__nav">
            {group.items.map((item) => (
              <li key={item.id}>
                <a
                  href={hrefForNav(item.id, SIDEBAR_NAV_HREF)}
                  onClick={(event) =>
                    handleCanonicalNav(event, hrefForNav(item.id, SIDEBAR_NAV_HREF))
                  }
                  className={
                    item.active
                      ? "cd-sidebar__item cd-sidebar__item--active"
                      : "cd-sidebar__item"
                  }
                >
                  <SidebarIcon name={item.icon} className="cd-sidebar__icon" size={18} />
                  <span>{item.label}</span>
                </a>
              </li>
            ))}
          </ul>
        </div>
      ))}

      <div className="cd-sidebar__footer">
        <div className="cd-sidebar__theme">
          <span className="cd-sidebar__theme-label">{data.sidebar.themeLabel}</span>
          <div className="cd-sidebar__theme-value">
            <IconSun size={14} />
            <span>{data.sidebar.themeValue}</span>
          </div>
        </div>
        <div className="cd-sidebar__version">
          <div>{data.sidebar.version}</div>
          <div>{data.sidebar.copyright}</div>
        </div>
      </div>
    </aside>
  );
}

export function PortalFooter(): ReactNode {
  const data = useCanonicalDesktop();
  return (
    <footer className="cd-footer">
      <div className="cd-footer__inner">
        <span className="cd-footer__mark" aria-hidden="true">
          ✦
        </span>
        <span>{data.footer}</span>
      </div>
    </footer>
  );
}
