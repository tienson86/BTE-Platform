import type { EnvironmentConfig } from "./types";

export const stagingEnvironment: EnvironmentConfig = {
  name: "staging",
  label: "Staging",
  diagnostics: true,
  strictMode: true,
};
