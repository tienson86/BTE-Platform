import type { MouseEvent, ReactNode } from "react";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";
import {
  IconMenu,
  IconSun,
  SidebarIcon,
  IconStarLogo,
} from "../icons";

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
  const target = document.getElementById("xuat");
  if (target) {
    target.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }
  window.location.hash = "xuat";
}

export function PortalHeader(): ReactNode {
  // Customer chrome is server-rendered from CUSTOMER_NAV_ITEMS
  // (templates_util._customer_header_html). Do not reintroduce a second stack.
  return null;
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
