/**
 * P7-IMP-14 Narrative Composer adapter. Copy published compact only.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import {
  INTERPRETATION_TITLE,
  adaptPack07Narrative,
  InterpretationCard,
} from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";
import type { DashboardCardSpec } from "../../src/screens/commercial_dashboard/types";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");
const CARD: DashboardCardSpec = { id: "interpretation", title: INTERPRETATION_TITLE, span: 12 };

const LIVE = {
  detailed_narrative: {
    title: "LUẬN GIẢI TỔNG THỂ",
    executive: "Lá số này thuộc mệnh cục Kiêm, hạng B. Trọng tâm hiện tại là giữ kỷ luật vốn.",
    strengths: [{ title: "Điểm mạnh", summary: "Nền tảng giữ tài vững.", domain: "wealth", priority: "P0" }],
    risks: [{ title: "Rủi ro", summary: "Sự nghiệp đang quá tải.", domain: "career", priority: "P1" }],
    opportunities: [{ title: "Cơ hội", summary: "Biểu đạt sự nghiệp còn dư địa.", domain: "career", priority: "P1" }],
    domains: [
      {
        id: "career",
        title: "Sự nghiệp",
        summary: "Sự nghiệp: Mạnh.",
        state: "Mạnh",
        driver: "Thực Thương",
        bottleneck: "Ấn quá vượng kìm biểu đạt",
        opportunity: "Biểu đạt",
        caution: "Quá tải",
        condition: "Không tăng khối lượng việc",
      },
    ],
    luck: [{ title: "Vận hiện tại", summary: "Đại vận hiện tại: 2022–2031.", domain: "", priority: "P1" }],
    actions: [{ title: "Giữ kỷ luật vốn", summary: "Giữ kỷ luật vốn. Tài biến động cao.", domain: "wealth", priority: "P0" }],
    closing: "Giữ thứ tự: xử lý nút thắt trước, rồi mới mở rộng. Giữ kỷ luật vốn",
    labels: {
      executive: "Tóm tắt",
      strengths: "Điểm mạnh",
      risks: "Rủi ro",
      opportunities: "Cơ hội",
      domains: "Sáu trụ cột",
      luck: "Vận hiện tại",
      actions: "Việc ưu tiên",
      closing: "Kết luận",
      fields: {
        state: "Hiện trạng",
        driver: "Động lực",
        bottleneck: "Điểm nghẽn",
        opportunity: "Cơ hội",
        caution: "Lưu ý",
        condition: "Điều kiện",
      },
    },
  },
} as AnalysisDataDto;

describe("P7-IMP-14 Narrative Composer", () => {
  it("keeps the frozen card title and story order", () => {
    const model = adaptPack07Narrative(LIVE);
    expect(model?.title).toBe(INTERPRETATION_TITLE);
    expect(model?.composer?.executive).toContain("mệnh cục");
    const { container } = render(<InterpretationCard card={CARD} model={model!} />);
    expect(container.querySelector(".bte-cdash__card-title")?.textContent).toBe(INTERPRETATION_TITLE);
    const order = [...container.querySelectorAll("[data-int-section]")].map((node) =>
      node.getAttribute("data-int-section"),
    );
    expect(order).toEqual([
      "executive",
      "strengths",
      "risks",
      "opportunities",
      "domains",
      "luck",
      "actions",
      "closing",
    ]);
  });

  it("returns null without a published composer compact so UI-11 stays intact", () => {
    expect(adaptPack07Narrative({ narrative_result: { overview: "legacy" } } as AnalysisDataDto)).toBeNull();
  });

  it("does not invent decorative advice in the adapter", () => {
    const adapter = readFileSync(resolve(ROOT, "narrativeComposerAdapter.ts"), "utf8");
    expect(adapter).not.toContain("mặc đỏ");
    expect(adapter).not.toContain("sống gần nước");
    expect(adapter).not.toContain("mua cây");
    expect(adapter).not.toContain("năm nay kết hôn");
  });
});
