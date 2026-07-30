import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/library", label: "Library" },
  { to: "/create", label: "New asset" },
  { to: "/approval", label: "Approval" },
];

export function Sidebar() {
  return (
    <aside className="flex w-56 shrink-0 flex-col gap-6 border-r border-[var(--line)] px-4 py-6">
      <div>
        <p className="font-display text-xl tracking-tight text-[var(--accent)]">
          BTE
        </p>
        <p className="mt-1 text-xs uppercase tracking-[0.18em] text-[var(--muted)]">
          Knowledge Console
        </p>
      </div>
      <nav className="flex flex-col gap-1" aria-label="Primary">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.end}
            className={({ isActive }) =>
              [
                "rounded-md px-3 py-2 text-sm transition-colors",
                isActive
                  ? "bg-[var(--accent-soft)] font-medium text-[var(--accent)]"
                  : "text-[var(--muted)] hover:bg-[var(--accent-soft)] hover:text-[var(--fg)]",
              ].join(" ")
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
      <div className="mt-auto text-xs text-[var(--muted)]">
        Editor workspace · Sprint 2
      </div>
    </aside>
  );
}
