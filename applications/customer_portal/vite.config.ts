/**
 * Vite production build for Canonical Desktop V2 Result page.
 * Output: static/dist/result.* (served by FastAPI /static).
 */

import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";
import { fileURLToPath } from "node:url";

const rootDir = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, rootDir, "");
  return {
    plugins: [react()],
    root: rootDir,
    base: "/static/dist/",
    define: {
      "import.meta.env.VITE_DATA_SOURCE": JSON.stringify(
        env.VITE_DATA_SOURCE || "api",
      ),
      "import.meta.env.VITE_API_BASE_URL": JSON.stringify(
        env.VITE_API_BASE_URL || "/backend/api/v1",
      ),
    },
    build: {
      outDir: path.resolve(rootDir, "static/dist"),
      emptyOutDir: true,
      sourcemap: true,
      rollupOptions: {
        input: path.resolve(rootDir, "src/entries/resultApp.tsx"),
        output: {
          entryFileNames: "result.js",
          chunkFileNames: "chunks/[name]-[hash].js",
          assetFileNames: (assetInfo) => {
            if (assetInfo.name?.endsWith(".css")) {
              return "result.css";
            }
            return "assets/[name]-[hash][extname]";
          },
        },
      },
    },
    resolve: {
      alias: {
        "@": path.resolve(rootDir, "src"),
      },
    },
  };
});
