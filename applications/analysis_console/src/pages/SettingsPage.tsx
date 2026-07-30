import { useEffect } from "react";
import { PageHeader } from "../components/PageHeader";
import { useTheme } from "../hooks/useTheme";
import { useLibrary } from "../state/library";

export function SettingsPage() {
  const { settings, updateSettings } = useLibrary();
  const { theme, setTheme } = useTheme();

  useEffect(() => {
    if (settings.theme_preference === "system") {
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      setTheme(prefersDark ? "dark" : "light");
      return;
    }
    setTheme(settings.theme_preference);
  }, [settings.theme_preference, setTheme]);

  useEffect(() => {
    document.documentElement.dataset.density = settings.density;
    document.documentElement.classList.toggle(
      "reduce-motion",
      settings.reduce_motion,
    );
  }, [settings.density, settings.reduce_motion]);

  return (
    <div className="mx-auto max-w-2xl">
      <PageHeader
        eyebrow="Preferences"
        title="Settings"
        description="Theme, density, motion, and workspace defaults for the Analysis Console."
      />

      <form
        className="surface space-y-6 rounded-2xl p-6"
        onSubmit={(event) => event.preventDefault()}
      >
        <label className="block space-y-2 text-sm">
          <span className="text-[var(--muted)]">Theme preference</span>
          <select
            className="w-full rounded-xl border border-[var(--line)] bg-transparent px-3 py-2.5 outline-none focus-visible:border-[var(--accent)] focus-visible:ring-2 focus-visible:ring-[var(--accent)]/30"
            value={settings.theme_preference}
            onChange={(event) =>
              updateSettings({
                theme_preference: event.target.value as
                  | "light"
                  | "dark"
                  | "system",
              })
            }
          >
            <option value="system">System</option>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
          <span className="text-xs text-[var(--muted)]">
            Active theme: {theme}
          </span>
        </label>

        <label className="block space-y-2 text-sm">
          <span className="text-[var(--muted)]">Density</span>
          <select
            className="w-full rounded-xl border border-[var(--line)] bg-transparent px-3 py-2.5 outline-none focus-visible:border-[var(--accent)] focus-visible:ring-2 focus-visible:ring-[var(--accent)]/30"
            value={settings.density}
            onChange={(event) =>
              updateSettings({
                density: event.target.value as "comfortable" | "compact",
              })
            }
          >
            <option value="comfortable">Comfortable</option>
            <option value="compact">Compact</option>
          </select>
        </label>

        <label className="block space-y-2 text-sm">
          <span className="text-[var(--muted)]">Default timezone</span>
          <input
            className="w-full rounded-xl border border-[var(--line)] bg-transparent px-3 py-2.5 outline-none focus-visible:border-[var(--accent)] focus-visible:ring-2 focus-visible:ring-[var(--accent)]/30"
            value={settings.default_timezone}
            onChange={(event) =>
              updateSettings({ default_timezone: event.target.value })
            }
          />
        </label>

        <fieldset className="space-y-3">
          <legend className="text-sm text-[var(--muted)]">Workspace</legend>
          {(
            [
              ["auto_save_charts", "Auto-save charts to library"],
              ["show_api_status", "Show API status in top bar"],
              ["reduce_motion", "Reduce motion"],
            ] as const
          ).map(([key, label]) => (
            <label key={key} className="flex items-center gap-3 text-sm">
              <input
                type="checkbox"
                checked={settings[key]}
                onChange={(event) =>
                  updateSettings({ [key]: event.target.checked })
                }
              />
              {label}
            </label>
          ))}
        </fieldset>
      </form>
    </div>
  );
}
