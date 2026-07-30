import { Link } from "react-router-dom";
import { useLibrary } from "../state/library";

type TopBarProps = {
  theme: "light" | "dark";
  onToggleTheme: () => void;
  onOpenNav: () => void;
  apiStatus: "checking" | "online" | "offline";
};

export function TopBar({
  theme,
  onToggleTheme,
  onOpenNav,
  apiStatus,
}: TopBarProps) {
  const { settings, profile } = useLibrary();

  return (
    <header className="flex items-center justify-between gap-3 border-b border-[var(--line)] px-4 py-3 md:px-6">
      <div className="flex items-center gap-3">
        <button
          type="button"
          className="rounded-lg border border-[var(--line)] px-3 py-2 text-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)] md:hidden"
          onClick={onOpenNav}
          aria-label="Open navigation"
          aria-controls="app-sidebar"
        >
          Menu
        </button>
        <div>
          <p className="font-display text-xl font-semibold md:text-2xl">
            BTE Analysis Console
          </p>
          <p className="text-xs text-[var(--muted)] md:text-sm">
            Project · Charts · Timeline · Report
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        {settings.show_api_status ? (
          <span
            className={`hidden rounded-full px-3 py-1 text-xs font-medium sm:inline-flex ${
              apiStatus === "online"
                ? "bg-[var(--accent-soft)] text-[var(--accent)]"
                : apiStatus === "offline"
                  ? "bg-red-500/15 text-[var(--danger)]"
                  : "bg-[var(--line)] text-[var(--muted)]"
            }`}
            role="status"
            aria-live="polite"
          >
            API {apiStatus}
          </span>
        ) : null}
        <Link
          to="/profile"
          className="hidden rounded-xl border border-[var(--line)] px-3 py-2 text-sm font-medium transition hover:border-[var(--accent)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)] sm:inline-flex"
        >
          {profile.display_name}
        </Link>
        <button
          type="button"
          onClick={onToggleTheme}
          className="rounded-xl border border-[var(--line)] bg-[var(--bg-elevated)] px-3 py-2 text-sm font-medium transition hover:border-[var(--accent)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
          aria-label={
            theme === "dark" ? "Switch to light mode" : "Switch to dark mode"
          }
        >
          {theme === "dark" ? "Light" : "Dark"}
        </button>
      </div>
    </header>
  );
}
