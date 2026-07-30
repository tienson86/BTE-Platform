import { useEffect, useState, type ReactNode } from "react";
import { api } from "../api/client";
import { useTheme } from "../hooks/useTheme";
import { useLibrary } from "../state/library";
import { Sidebar } from "./Sidebar";
import { TopBar } from "./TopBar";

export function AppShell({ children }: { children: ReactNode }) {
  const { theme, toggle, setTheme } = useTheme();
  const { settings } = useLibrary();
  const [navOpen, setNavOpen] = useState(false);
  const [apiStatus, setApiStatus] = useState<"checking" | "online" | "offline">(
    "checking",
  );

  useEffect(() => {
    if (settings.theme_preference === "system") return;
    setTheme(settings.theme_preference);
  }, [settings.theme_preference, setTheme]);

  useEffect(() => {
    document.documentElement.dataset.density = settings.density;
    document.documentElement.classList.toggle(
      "reduce-motion",
      settings.reduce_motion,
    );
  }, [settings.density, settings.reduce_motion]);

  useEffect(() => {
    let cancelled = false;
    api
      .health()
      .then(() => {
        if (!cancelled) setApiStatus("online");
      })
      .catch(() => {
        if (!cancelled) setApiStatus("offline");
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="min-h-screen md:flex">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-xl focus:bg-[var(--accent)] focus:px-4 focus:py-2 focus:text-sm focus:font-semibold focus:text-white"
      >
        Skip to main content
      </a>
      <Sidebar open={navOpen} onClose={() => setNavOpen(false)} />
      <div className="flex min-h-screen min-w-0 flex-1 flex-col">
        <TopBar
          theme={theme}
          onToggleTheme={toggle}
          onOpenNav={() => setNavOpen(true)}
          apiStatus={apiStatus}
        />
        <main
          id="main-content"
          tabIndex={-1}
          className="flex-1 px-4 py-6 outline-none md:px-8 md:py-8"
        >
          {children}
        </main>
      </div>
    </div>
  );
}
