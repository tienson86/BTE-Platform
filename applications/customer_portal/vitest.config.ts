import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    include: ["tests/**/*.test.ts", "tests/**/*.test.tsx", "tests/js/**/*.test.ts", "tests/js/**/*.test.tsx"],
  },
});
