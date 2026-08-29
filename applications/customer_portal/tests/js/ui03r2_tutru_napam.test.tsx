/**
 * UI-03R2 — Tứ Trụ summary short Nạp âm (Ngũ hành) vs Bát Tự full names.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render } from "@testing-library/react";
import { TuTruPanel } from "../../src/components/canonical";
import {
  CommercialDashboardPage,
  adaptIdentityHeader,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");
const CANONICAL = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/components/canonical");
const DATE_SELECTION = resolve(
  dirname(fileURLToPath(import.meta.url)),
  "../../src/features/date_selection/components.tsx",
);

const CASE_0001 = {
  identity: {
    four_pillars: {
      year: { stem: "Bính", branch: "Dần", can_chi: "Bính Dần", nayin_element: "Hỏa", cung_phi: "Khôn" },
      month: { stem: "Tân", branch: "Sửu", can_chi: "Tân Sửu", nayin_element: "Thổ", cung_phi: "Càn" },
      day: { stem: "Canh", branch: "Ngọ", can_chi: "Canh Ngọ", nayin_element: "Thổ", cung_phi: "Khảm" },
      hour: { stem: "Mậu", branch: "Dần", can_chi: "Mậu Dần", nayin_element: "Thổ", cung_phi: "Khôn" },
    },
  },
  bazi: {
    day_master: "Canh",
    year_pillar: { stem: "Bính", branch: "Dần", nap_am: "Lư Trung Hỏa" },
    month_pillar: { stem: "Tân", branch: "Sửu", nap_am: "Bích Thượng Thổ" },
    day_pillar: { stem: "Canh", branch: "Ngọ", nap_am: "Lộ Bàng Thổ" },
    hour_pillar: { stem: "Mậu", branch: "Dần", nap_am: "Thành Đầu Thổ" },
  },
} as AnalysisDataDto;

const FULL_NAP_AM = ["Lư Trung Hỏa", "Bích Thượng Thổ", "Lộ Bàng Thổ", "Thành Đầu Thổ"] as const;

function renderCase() {
  return render(
    <CommercialDashboardPage analysis={CASE_0001} resultSource="current" layoutMode="live" />,
  );
}

afterEach(cleanup);

describe("UI-03R2 Tứ Trụ short Nạp âm", () => {
  it("R2-1 Tứ Trụ summary Nạp Âm values are short five-element labels", () => {
    const { container } = renderCase();
    const values = [...container.querySelectorAll('[data-region="pillars"] [data-kind="nap-am"]')].map(
      (node) => node.textContent,
    );
    for (const value of values) {
      expect(value).toMatch(/^(Mộc|Hỏa|Thổ|Kim|Thủy)$/);
    }
  });

  it("R2-2 CASE-0001 summary renders Hỏa / Thổ / Thổ / Thổ", () => {
    const { container } = renderCase();
    const values = [...container.querySelectorAll('[data-region="pillars"] [data-kind="nap-am"]')].map(
      (node) => node.textContent,
    );
    expect(values).toEqual(["Hỏa", "Thổ", "Thổ", "Thổ"]);
    expect(adaptIdentityHeader(CASE_0001).pillars.year.napAm).toBe("Hỏa");
    expect(adaptIdentityHeader(CASE_0001).pillars.month.napAm).toBe("Thổ");
  });

  it("R2-3 Tứ Trụ summary does not render full Nạp Âm names", () => {
    const { container } = renderCase();
    const region = container.querySelector('[data-region="pillars"]')?.textContent || "";
    for (const name of FULL_NAP_AM) {
      expect(region).not.toContain(name);
    }
  });

  it("R2-4 Bát Tự detail still renders the four full Nạp Âm names", () => {
    const { container } = renderCase();
    const values = [...container.querySelectorAll('[data-card="bazi"] [data-bazi-field="nap-am"]')].map(
      (node) => node.textContent,
    );
    expect(values).toEqual([...FULL_NAP_AM]);
  });

  it("R2-5 Good Date TuTruPanel behavior remains unchanged", () => {
    const { container } = render(
      <TuTruPanel
        year={{ canChi: "Bính Ngọ", napAm: "Thủy", cungPhi: "Khảm" }}
        month={{ canChi: "Bính Thân", napAm: "Hỏa", cungPhi: "Khôn" }}
        day={{ canChi: "Đinh Sửu", napAm: "Thủy", cungPhi: "Chấn" }}
        hour={{ canChi: "Ất Tỵ", napAm: "Hỏa", cungPhi: "Khôn" }}
      />,
    );
    const napAm = [...container.querySelectorAll('[data-kind="nap-am"]')].map((node) => node.textContent);
    expect(napAm).toEqual(["Thủy", "Hỏa", "Thủy", "Hỏa"]);
    const panel = readFileSync(resolve(CANONICAL, "TuTruPanel.tsx"), "utf8");
    const dateSource = readFileSync(DATE_SELECTION, "utf8");
    expect(dateSource).toContain("nayin_element");
    expect(panel).not.toMatch(/nayin_lookup|NAP_AM_MAP|Lư Trung Hỏa/);
  });

  it("R2-6 Cung Phi unchanged", () => {
    const bound = adaptIdentityHeader(CASE_0001);
    expect(bound.pillars.year.cungPhi).toBe("Khôn");
    expect(bound.pillars.month.cungPhi).toBe("Càn");
    expect(bound.pillars.day.cungPhi).toBe("Khảm");
    expect(bound.pillars.hour.cungPhi).toBe("Khôn");
    const { container } = renderCase();
    const cung = [...container.querySelectorAll('[data-region="pillars"] [data-kind="cung-phi"]')].map(
      (node) => node.textContent,
    );
    expect(cung).toEqual(["Khôn", "Càn", "Khảm", "Khôn"]);
  });

  it("R2-7 Can Chi unchanged", () => {
    const { container } = renderCase();
    const values = [...container.querySelectorAll('[data-region="pillars"] .bte-tu-tru__can-chi')].map(
      (node) => node.textContent,
    );
    expect(values).toEqual(["Bính Dần", "Tân Sửu", "Canh Ngọ", "Mậu Dần"]);
  });

  it("R2-8 does not add astrology calculation to the frontend", () => {
    const adapter = readFileSync(resolve(ROOT, "adapter.ts"), "utf8");
    const four = readFileSync(resolve(ROOT, "FourPillars.tsx"), "utf8");
    const panel = readFileSync(resolve(CANONICAL, "TuTruPanel.tsx"), "utf8");
    const tokens = readFileSync(resolve(CANONICAL, "tokens.ts"), "utf8");
    for (const source of [adapter, four, panel]) {
      expect(source).not.toMatch(/engines\./);
      expect(source).not.toMatch(/nayin_lookup|pillar_contract|hoa_giap|NAP_AM_MAP/);
    }
    expect(adapter).toContain("nayin_element");
    expect(adapter).not.toContain("baziPillar?.nap_am");
    expect(tokens).toContain("napAmBadgeToken");
  });
});
