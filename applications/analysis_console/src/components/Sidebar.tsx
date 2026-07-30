import { NavLink } from "react-router-dom";
import { useSession } from "../state/session";

const links = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/chart/input", label: "Chart Input" },
  { to: "/chart", label: "Chart Viewer" },
  { to: "/analysis", label: "Analysis" },
  { to: "/interpretation", label: "Interpretation" },
  { to: "/luck", label: "Luck" },
];

type SidebarProps = {
  open: boolean;
  onClose: () => void;
};

export function Sidebar({ open, onClose }: SidebarProps) {
  const { chart, analysis, interpretation, report } = useSession();

  return (
    <>
      <div
        className={`fixed inset-0 z-30 bg-black/40 transition md:hidden ${
          open ? "opacity-100" : "pointer-events-none opacity-0"
        }`}
        onClick={onClose}
      />
      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-72 flex-col border-r border-[var(--line)] bg-[var(--bg-elevated)] p-5 transition-transform md:static md:translate-x-0 ${
          open ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="mb-8">
          <p className="font-display text-3xl font-semibold tracking-tight text-[var(--fg)]">
            BTE
          </p>
          <p className="mt-1 text-sm text-[var(--muted)]">Analysis Console</p>
        </div>

        <nav className="flex flex-1 flex-col gap-1">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.end}
              onClick={onClose}
              className={({ isActive }) =>
                `rounded-xl px-3 py-2.5 text-sm font-medium transition ${
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
          <p>Chart: {chart?.chart_id ?? "—"}</p>
          <p>Analysis: {analysis?.analysis_id ?? "—"}</p>
          <p>Interp: {interpretation?.interpretation_id ?? "—"}</p>
          <p>Report: {report?.report_id ?? "—"}</p>
        </div>
      </aside>
    </>
  );
}
