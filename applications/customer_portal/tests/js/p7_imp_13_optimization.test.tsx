/**
 * P7-IMP-13 Life Optimization Action Plan adapter. Copy published compact only.
 */

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ACTION_PLAN_TITLE, adaptOptimizationPlan, ActionPlanCard } from "../../src/screens/commercial_dashboard";
import type { AnalysisDataDto } from "../../src/models";
import type { DashboardCardSpec } from "../../src/screens/commercial_dashboard/types";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../src/screens/commercial_dashboard");
const CARD: DashboardCardSpec = { id: "action-plan", title: ACTION_PLAN_TITLE, span: 12 };

const LIVE = {
  optimization: {
    title: "KẾ HOẠCH TỐI ƯU",
    top_priorities: [
      { rank: 1, label: "Ưu tiên 1", domain: "Sự nghiệp", title: "Kiểm soát khối lượng việc", reason: "Sự nghiệp đang quá tải", action: "Bảo vệ", scope: "Vận hiện tại" },
      { rank: 2, label: "Ưu tiên 2", domain: "Tài", title: "Giữ kỷ luật vốn", reason: "Tài biến động cao", action: "Giữ vốn", scope: "Dài hạn" },
      { rank: 3, label: "Ưu tiên 3", domain: "Quan hệ", title: "Tăng chất lượng giao tiếp", reason: "Nút thắt giao tiếp", action: "Phát triển", scope: "Dài hạn" },
    ],
    groups: {
      develop: [{ domain: "Quan hệ", title: "Tăng chất lượng giao tiếp", reason: "Nút thắt giao tiếp", action: "Phát triển" }],
      improve: [{ domain: "Tài", title: "Giữ kỷ luật vốn", reason: "Tài biến động cao", action: "Giữ vốn" }],
      control: [{ domain: "Sự nghiệp", title: "Kiểm soát khối lượng việc", reason: "Sự nghiệp đang quá tải", action: "Bảo vệ" }],
      avoid: [{ domain: "Sự nghiệp", title: "Không tăng khối lượng việc", reason: "Đang quá tải", action: "Hạn chế" }],
      temporal: [{ domain: "Sự nghiệp", title: "Kiểm soát khối lượng việc", reason: "Sự nghiệp đang quá tải", action: "Bảo vệ", scope: "Vận hiện tại" }],
    },
    natal: { title: "Dài hạn", items: [{ domain: "Tài", title: "Giữ kỷ luật vốn", reason: "Tài biến động cao", action: "Giữ vốn" }] },
    temporal: { title: "Vận hiện tại / Năm 2026", year: "2026", items: [{ domain: "Sự nghiệp", title: "Kiểm soát khối lượng việc", reason: "Quá tải", action: "Bảo vệ" }] },
    domains: [
      { id: "wealth", title: "Tài", target: "capital_discipline", why: "Tài biến động cao", action: "Giữ kỷ luật vốn", condition: "", caution: "Hạn chế mở rộng", temporal: "" },
    ],
    conflicts: [{ title: "Sự nghiệp cần đầu ra, sinh lực cần phục hồi", domains: "Sự nghiệp · Sinh lực", resolution: "Giữ cả hai điều kiện" }],
    useful_god: { element: "Hỏa", functions: ["kích hoạt", "hiển lộ"], reason: "Dụng thần cần được dùng theo chức năng cấu trúc" },
    elements: [{ element: "Hỏa", function: "kích hoạt, hiển lộ", direction: "cần tăng chức năng", domains: ["Sự nghiệp"], reason: "Hỗ trợ chức năng hành" }],
  },
} as AnalysisDataDto;

describe("P7-IMP-13 Life Optimization Action Plan", () => {
  it("keeps the frozen card title and shows top 3", () => {
    const model = adaptOptimizationPlan(LIVE);
    expect(model?.title).toBe(ACTION_PLAN_TITLE);
    expect(model?.optimization?.topPriorities).toHaveLength(3);
    const { container } = render(<ActionPlanCard card={CARD} model={model!} />);
    expect(container.querySelector(".bte-cdash__card-title")?.textContent).toBe(ACTION_PLAN_TITLE);
    expect(container.querySelector("[data-ap-section='top-priorities']")?.textContent).toContain("Ưu tiên 1");
    expect(container.querySelector("[data-ap-section='natal']")).toBeTruthy();
    expect(container.querySelector("[data-ap-section='temporal']")).toBeTruthy();
  });

  it("does not turn Useful God Fire into wear-red copy", () => {
    const model = adaptOptimizationPlan(LIVE);
    const dump = JSON.stringify(model).toLowerCase();
    expect(dump).not.toContain("mặc đỏ");
    expect(dump).not.toContain("wear red");
    expect(model?.optimization?.usefulGod?.reason).toContain("chức năng");
  });

  it("returns null without a published optimization compact", () => {
    expect(adaptOptimizationPlan({ useful_god: { useful_god: "Hỏa" } } as AnalysisDataDto)).toBeNull();
  });

  it("does not invent decorative feng shui in the adapter", () => {
    const adapter = readFileSync(resolve(ROOT, "actionPlanAdapter.ts"), "utf8");
    expect(adapter).not.toContain("mặc đỏ");
    expect(adapter).not.toContain("sống gần nước");
    expect(adapter).not.toContain("mua cây");
  });
});
