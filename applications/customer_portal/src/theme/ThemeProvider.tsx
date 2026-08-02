import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import type { ThemeMode } from "../tokens/color";
import {
  THEME_MODES,
  applyThemeMode,
  initializeTheme,
  loadThemePreference,
  persistThemePreference,
  readThemeMode,
  resolveThemeMode,
  type ThemePreference,
} from "./runtime";

export type ThemeContextValue = {
  mode: ThemeMode;
  preference: ThemePreference;
  setPreference: (preference: ThemePreference) => void;
  toggleMode: () => void;
  modes: readonly ThemeMode[];
};

const ThemeContext = createContext<ThemeContextValue | null>(null);

export type ThemeProviderProps = {
  children: ReactNode;
  root?: HTMLElement | null;
  initialPreference?: ThemePreference;
};

function readSystemPrefersDark(): boolean {
  return (
    typeof window !== "undefined" &&
    typeof window.matchMedia === "function" &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
  );
}

/**
 * React ThemeProvider — mode, toggle, persistence, initialization.
 * Business logic must remain outside this provider.
 */
export function ThemeProvider({
  children,
  root,
  initialPreference,
}: ThemeProviderProps): ReactNode {
  const [preference, setPreferenceState] = useState<ThemePreference>(
    () => initialPreference ?? loadThemePreference(),
  );
  const [mode, setMode] = useState<ThemeMode>(() => {
    if (typeof document === "undefined") {
      return resolveThemeMode(initialPreference ?? "system", false);
    }
    return initializeTheme(root ?? document.documentElement);
  });

  const resolveRoot = useCallback((): HTMLElement | null => {
    if (root !== undefined) {
      return root;
    }
    return typeof document !== "undefined" ? document.documentElement : null;
  }, [root]);

  const applyPreference = useCallback(
    (nextPreference: ThemePreference) => {
      const nextMode = resolveThemeMode(nextPreference, readSystemPrefersDark());
      applyThemeMode(nextMode, resolveRoot());
      persistThemePreference(nextPreference);
      setPreferenceState(nextPreference);
      setMode(nextMode);
    },
    [resolveRoot],
  );

  useEffect(() => {
    const nextMode = resolveThemeMode(preference, readSystemPrefersDark());
    applyThemeMode(nextMode, resolveRoot());
    setMode(nextMode);
  }, [preference, resolveRoot]);

  useEffect(() => {
    if (typeof window === "undefined" || typeof window.matchMedia !== "function") {
      return;
    }
    const media = window.matchMedia("(prefers-color-scheme: dark)");
    const onChange = (): void => {
      if (preference !== "system") {
        return;
      }
      const nextMode = resolveThemeMode("system", media.matches);
      applyThemeMode(nextMode, resolveRoot());
      setMode(nextMode);
    };
    media.addEventListener("change", onChange);
    return () => media.removeEventListener("change", onChange);
  }, [preference, resolveRoot]);

  const toggleMode = useCallback(() => {
    const current = readThemeMode(resolveRoot());
    const next: ThemeMode = current === "dark" ? "light" : "dark";
    applyPreference(next);
  }, [applyPreference, resolveRoot]);

  const value = useMemo<ThemeContextValue>(
    () => ({
      mode,
      preference,
      setPreference: applyPreference,
      toggleMode,
      modes: THEME_MODES,
    }),
    [mode, preference, applyPreference, toggleMode],
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

/** Consume theme context. Throws if used outside ThemeProvider. */
export function useTheme(): ThemeContextValue {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within ThemeProvider");
  }
  return context;
}
