/**
 * Vite config for RB16 Number Energy runtime screenshot harness only.
 * Does not change the public numberEnergy.js production entry.
 */
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";
import { fileURLToPath } from "node:url";

const rootDir = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react()],
  root: rootDir,
  mode: "production",
  define: {
    "process.env.NODE_ENV": JSON.stringify("production"),
  },
  base: "/static/dist/",
  build: {
    outDir: path.resolve(rootDir, "screenshots/number_energy/rb16/harness"),
    emptyOutDir: true,
    sourcemap: false,
    cssCodeSplit: false,
    lib: {
      entry: path.resolve(rootDir, "src/entries/numberEnergyRuntimeScreenshotApp.tsx"),
      formats: ["es"],
      fileName: () => "numberEnergyRuntime.js",
    },
    rollupOptions: {
      output: {
        inlineDynamicImports: true,
      },
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(rootDir, "src"),
    },
  },
});
