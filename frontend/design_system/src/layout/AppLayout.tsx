import { memo, type ReactNode } from "react";
import { cx } from "../utils/cx";

export type NavItem = {
  id: string;
  label: string;
  href?: string;
  active?: boolean;
  onClick?: () => void;
};

export const Sidebar = memo(function Sidebar({
  brand,
  items,
  open = true,
  className,
  children,
}: {
  brand?: ReactNode;
  items?: NavItem[];
  open?: boolean;
  className?: string;
  children?: ReactNode;
}) {
  return (
    <aside className={cx("bte-app-sidebar", className)} data-open={open}>
      {brand ? <div className="bte-stack-2" style={{ marginBottom: "var(--bte-space-4)" }}>{brand}</div> : null}
      {items?.length ? (
        <nav className="bte-sidebar-nav" aria-label="Sidebar">
          {items.map((item) =>
            item.href ? (
              <a
                key={item.id}
                href={item.href}
                className="bte-sidebar-link"
                data-active={!!item.active}
              >
                {item.label}
              </a>
            ) : (
              <button
                key={item.id}
                type="button"
                className="bte-sidebar-link"
                data-active={!!item.active}
                onClick={item.onClick}
              >
                {item.label}
              </button>
            ),
          )}
        </nav>
      ) : null}
      {children}
    </aside>
  );
});

export function Header({
  left,
  right,
  className,
}: {
  left?: ReactNode;
  right?: ReactNode;
  className?: string;
}) {
  return (
    <header className={cx("bte-app-header", className)}>
      <div className="bte-row-3">{left}</div>
      <div className="bte-row-3">{right}</div>
    </header>
  );
}

export function Content({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return <main className={cx("bte-app-content", className)}>{children}</main>;
}

export function InspectorPanel({
  children,
  open = true,
  title,
  className,
}: {
  children: ReactNode;
  open?: boolean;
  title?: string;
  className?: string;
}) {
  return (
    <aside className={cx("bte-app-inspector", className)} data-open={open}>
      {title ? <h2 className="bte-h3" style={{ marginBottom: "var(--bte-space-4)" }}>{title}</h2> : null}
      {children}
    </aside>
  );
}

export function Footer({
  children,
  className,
}: {
  children?: ReactNode;
  className?: string;
}) {
  return <footer className={cx("bte-app-footer", className)}>{children}</footer>;
}

export function AppLayout({
  sidebar,
  header,
  inspector,
  footer,
  children,
  showInspector = false,
  className,
}: {
  sidebar?: ReactNode;
  header?: ReactNode;
  inspector?: ReactNode;
  footer?: ReactNode;
  children: ReactNode;
  showInspector?: boolean;
  className?: string;
}) {
  return (
    <div
      className={cx("bte-app-layout", className)}
      data-inspector={showInspector ? "true" : "false"}
    >
      {sidebar}
      {header}
      <Content>{children}</Content>
      {showInspector ? inspector : null}
      {footer}
    </div>
  );
}
