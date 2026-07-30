import { useTheme } from "../hooks/useTheme";

export function TopBar({ title }: { title?: string }) {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="flex items-center justify-between border-b border-[var(--line)] px-6 py-4">
      <div>
        <h1 className="font-display text-lg text-[var(--fg)]">
          {title ?? "Knowledge Editor"}
        </h1>
        <p className="text-xs text-[var(--muted)]">
          Rules · Sentences · Phrases · Terminology
        </p>
      </div>
      <button
        type="button"
        onClick={toggleTheme}
        className="rounded-md border border-[var(--line)] px-3 py-1.5 text-xs text-[var(--muted)] hover:text-[var(--fg)]"
        aria-label="Toggle color theme"
      >
        {theme === "dark" ? "Light" : "Dark"}
      </button>
    </header>
  );
}
