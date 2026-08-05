import { useCallback, useEffect, useState, type ReactNode } from "react";
import { cx } from "../utils";
import { Footer } from "./Footer";
import { Header } from "./Header";
import { resolveActiveNavId } from "./Navigation/navItems";
import { Sidebar } from "./Sidebar";

export type AppLayoutProps = {
  children?: ReactNode;
  pathname?: string;
  activeNavId?: string;
  userLabel?: string;
  brand?: ReactNode;
  className?: string;
};

type ViewportMode = "desktop" | "tablet" | "mobile";

function readViewportMode(): ViewportMode {
  if (typeof window === "undefined" || typeof window.matchMedia !== "function") {
    return "desktop";
  }
  if (window.matchMedia("(max-width: 767px)").matches) {
    return "mobile";
  }
  if (window.matchMedia("(max-width: 1023px)").matches) {
    return "tablet";
  }
  return "desktop";
}

/**
 * Portal application shell (WP03 / ADR-004).
 * Fixed header, responsive sidebar, content, footer, modal/notification roots.
 */
export function AppLayout({
  children,
  pathname = "/",
  activeNavId,
  userLabel,
  brand,
  className,
}: AppLayoutProps): ReactNode {
  const [viewport, setViewport] = useState<ViewportMode>("desktop");
  const [drawerOpen, setDrawerOpen] = useState(false);

  useEffect(() => {
    const update = () => setViewport(readViewportMode());
    update();
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);

  useEffect(() => {
    setDrawerOpen(false);
  }, [pathname]);

  const closeDrawer = useCallback(() => setDrawerOpen(false), []);
  const toggleDrawer = useCallback(() => setDrawerOpen((open) => !open), []);

  const resolvedActive = activeNavId ?? resolveActiveNavId(pathname);
  const collapsed = viewport === "tablet";
  const isMobile = viewport === "mobile";

  return (
    <div
      className={cx("cui-app-shell", className)}
      data-viewport={viewport}
      data-sidebar-collapsed={collapsed || undefined}
    >
      <Header
        brand={brand}
        userLabel={userLabel}
        showMenuButton={isMobile}
        onMenuClick={toggleDrawer}
      />
      <div className="cui-app-shell__body">
        <Sidebar
          activeId={resolvedActive}
          collapsed={collapsed}
          open={isMobile ? drawerOpen : false}
          onClose={closeDrawer}
          onNavigate={isMobile ? closeDrawer : undefined}
        />
        <main className="cui-app-shell__main" id="main-content" tabIndex={-1}>
          {children}
        </main>
      </div>
      <Footer />
      <div className="cui-app-shell__notifications" id="cui-notification-root" />
      <div className="cui-app-shell__modals" id="cui-modal-root" />
    </div>
  );
}
