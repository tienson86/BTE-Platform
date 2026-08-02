/**
 * Typed environment names for Commercial UI V3 presentation.
 * Architecture only — no business feature configuration.
 */

export const ENVIRONMENT_NAMES = ["development", "staging", "production"] as const;

export type EnvironmentName = (typeof ENVIRONMENT_NAMES)[number];

export type EnvironmentConfig = {
  name: EnvironmentName;
  label: string;
  diagnostics: boolean;
  strictMode: boolean;
};
