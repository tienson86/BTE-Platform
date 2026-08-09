import type { ReactNode } from "react";
import { PortalIcon } from "../components/Icon";
import { PvSearch, PvToast } from "../components/primitives";
import {
  breadcrumbsFor,
  PORTAL_NAV,
  portalHref,
  ROUTE_TITLES,
  type PortalRoute,
} from "./routes";

export type PortalShellProps = {
  route: PortalRoute;
  search: string;
  toast: string | null;
  sidebarOpen: boolean;
  onSearch: (value: string) => void;
  onNavigate: (route: PortalRoute) => void;
  onToggleSidebar: () => void;
  children: ReactNode;
};

export function PortalShell({
  route,
  search,
  toast,
  sidebarOpen,
  onSearch,
  onNavigate,
  onToggleSidebar,
  children,
}: PortalShellProps) {
  const crumbs = breadcrumbsFor(route);
  const activeNav =
    route.startsWith("analyze") ? "analyze" : route === "result" ? "results" : route;

  return (
    <div className="pv-shell" data-portal="px5" data-route={route}>
      <a className="pv-skip" href="#pv-main">
        Đến nội dung chính
      </a>
      <header className="pv-topbar">
        <button type="button" className="pv-icon-btn pv-topbar__menu" aria-label="Mở điều hướng" onClick={onToggleSidebar}>
          <PortalIcon name="summary" />
        </button>
        <a className="pv-brand" href={portalHref("home")} onClick={(event) => { event.preventDefault(); onNavigate("home"); }}>
          BTE <span>Tư vấn</span>
        </a>
        <div className="pv-topbar__search">
          <PvSearch label="Tìm trong cổng tư vấn" value={search} placeholder="Tìm kết quả hoặc kiến thức" onChange={onSearch} />
        </div>
        <div className="pv-topbar__actions">
          <button type="button" className="pv-icon-btn" aria-label="Thông báo — sắp có" disabled>
            <PortalIcon name="warning" />
          </button>
          <button type="button" className="pv-user" aria-label="Nguyễn Văn An" onClick={() => onNavigate("profile")}>
            A
          </button>
        </div>
      </header>
      <div className="pv-shell__body">
        {sidebarOpen ? (
          <button type="button" className="pv-sidebar-backdrop" aria-label="Đóng điều hướng" onClick={onToggleSidebar} />
        ) : null}
        <aside className="pv-sidebar" data-open={sidebarOpen || undefined} aria-label="Điều hướng chính">
          <nav>
            <p className="pv-nav__group">Tư vấn</p>
            <ul className="pv-nav__list">
              {PORTAL_NAV.filter((item) => item.group === "primary").map((item) => (
                <li key={item.id}>
                  <a
                    className="pv-nav__link"
                    href={portalHref(item.id)}
                    aria-current={activeNav === item.id ? "page" : undefined}
                    onClick={(event) => {
                      event.preventDefault();
                      onNavigate(item.id);
                    }}
                  >
                    <PortalIcon name={item.icon} />
                    <span>{item.label}</span>
                  </a>
                </li>
              ))}
            </ul>
            <p className="pv-nav__group">Tài khoản</p>
            <ul className="pv-nav__list">
              {PORTAL_NAV.filter((item) => item.group === "secondary").map((item) => (
                <li key={item.id}>
                  <a
                    className="pv-nav__link"
                    href={portalHref(item.id)}
                    aria-current={activeNav === item.id ? "page" : undefined}
                    onClick={(event) => {
                      event.preventDefault();
                      onNavigate(item.id);
                    }}
                  >
                    <PortalIcon name={item.icon} />
                    <span>{item.label}</span>
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </aside>
        <div className="pv-main-wrap">
          <nav className="pv-breadcrumb" aria-label="Đường dẫn">
            <ol>
              {crumbs.map((item, index) => {
                const last = index === crumbs.length - 1;
                return (
                  <li key={item.id}>
                    {item.href && item.route && !last ? (
                      <a
                        href={item.href}
                        onClick={(event) => {
                          event.preventDefault();
                          onNavigate(item.route as PortalRoute);
                        }}
                      >
                        {item.label}
                      </a>
                    ) : (
                      <span aria-current={last ? "page" : undefined}>{item.label}</span>
                    )}
                  </li>
                );
              })}
            </ol>
          </nav>
          <main className="pv-main" id="pv-main" tabIndex={-1}>
            <h1 className="pv-sr-only">{ROUTE_TITLES[route]}</h1>
            {children}
          </main>
        </div>
      </div>
      <footer className="pv-footer">
        <PortalIcon name="footer" />
        <span>BTE · Cổng tư vấn</span>
      </footer>
      <PvToast message={toast} />
    </div>
  );
}
