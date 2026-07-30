import { useTheme } from "../hooks/useTheme";

export function TopBar({ title }: { title?: string }) {
  const { theme, toggleTheme } = useTheme();
  return (
    <header className="flex items-center justify-between border-b border-[var(--line)] px-6 py-4">
      <div>
        <h1 className="font-display text-lg">
          {title ?? "Golden Dataset Manager"}
        </h1>
        <p className="text-xs text-[var(--muted)]">
          Create · Import · Compare · Regression · Coverage
        </p>
      </div>
      <button
        type="button"
        onClick={toggleTheme}
        className="rounded-md border border-[var(--line)] px-3 py-1.5 text-xs text-[var(--muted)]"
        aria-label="Toggle color theme"
      >
        {theme === "dark" ? "Light" : "Dark"}
      </button>
    </header>
  );
}
