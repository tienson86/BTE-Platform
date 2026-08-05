import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    include: ["tests/**/*.test.ts", "tests/**/*.test.tsx", "tests/js/**/*.test.ts", "tests/js/**/*.test.tsx"],
    env: {
      // Keep Wave UI tests on mock fixtures; integration tests set api + fetch mocks.
      BTE_DATA_SOURCE: "mock",
      VITEST: "true",
    },
  },
});
