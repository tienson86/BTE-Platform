import { NavLink } from "react-router-dom";
import { useLibrary } from "../state/library";
import { useSession } from "../state/session";

const primaryLinks = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/charts", label: "Charts" },
  { to: "/history", label: "Customer History" },
  { to: "/timeline", label: "Timeline" },
  { to: "/chart/input", label: "Chart Input" },
  { to: "/chart", label: "Chart Viewer" },
  { to: "/analysis", label: "Analysis" },
  { to: "/interpretation", label: "Interpretation" },
  { to: "/luck", label: "Luck" },
];

const workspaceLinks = [
  { to: "/data", label: "Export / Import" },
  { to: "/settings", label: "Settings" },
  { to: "/profile", label: "User Profile" },
];

type SidebarProps = {
  open: boolean;
  onClose: () => void;
};

export function Sidebar({ open, onClose }: SidebarProps) {
  const { chart, analysis, interpretation, report } = useSession();
  const { profile, pinnedCharts } = useLibrary();

  return (
    <>
      <div
        className={`fixed inset-0 z-30 bg-black/40 transition md:hidden ${
          open ? "opacity-100" : "pointer-events-none opacity-0"
        }`}
        onClick={onClose}
        aria-hidden={!open}
      />
      <aside
        id="app-sidebar"
        aria-label="Primary"
        className={`fixed inset-y-0 left-0 z-40 flex w-72 flex-col border-r border-[var(--line)] bg-[var(--bg-elevated)] p-5 transition-transform md:static md:translate-x-0 ${
          open ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="mb-8">
          <p className="font-display text-3xl font-semibold tracking-tight text-[var(--fg)]">
            BTE
          </p>
          <p className="mt-1 text-sm text-[var(--muted)]">Analysis Console</p>
          <p className="mt-2 truncate text-xs text-[var(--accent)]">
            {profile.display_name}
          </p>
        </div>

        <nav className="flex flex-1 flex-col gap-1 overflow-y-auto" aria-label="Console">
          {primaryLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.end}
              onClick={onClose}
              className={({ isActive }) =>
                `rounded-xl px-3 py-2.5 text-sm font-medium transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)] ${
                  isActive
                    ? "bg-[var(--accent-soft)] text-[var(--accent)]"
                    : "text-[var(--muted)] hover:bg-[var(--accent-soft)] hover:text-[var(--fg)]"
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}

          <p className="mb-1 mt-5 px-3 text-[11px] font-semibold uppercase tracking-wide text-[var(--muted)]">
            Workspace
          </p>
          {workspaceLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              onClick={onClose}
              className={({ isActive }) =>
                `rounded-xl px-3 py-2.5 text-sm font-medium transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)] ${
                  isActive
                    ? "bg-[var(--accent-soft)] text-[var(--accent)]"
                    : "text-[var(--muted)] hover:bg-[var(--accent-soft)] hover:text-[var(--fg)]"
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </nav>

        <div className="mt-6 space-y-2 border-t border-[var(--line)] pt-4 text-xs text-[var(--muted)]">
          <p>Pinned: {pinnedCharts.length}</p>
          <p>Chart: {chart?.chart_id ?? "—"}</p>
          <p>Analysis: {analysis?.analysis_id ?? "—"}</p>
          <p>Interp: {interpretation?.interpretation_id ?? "—"}</p>
          <p>Report: {report?.report_id ?? "—"}</p>
        </div>
      </aside>
    </>
  );
}
