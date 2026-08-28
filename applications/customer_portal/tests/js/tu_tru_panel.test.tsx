import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { TuTruPanel } from "../../src/components/canonical";

afterEach(() => {
  cleanup();
});

const sample = {
  year: { canChi: "Bính Ngọ", napAm: "Thủy", cungPhi: "Khảm" },
  month: { canChi: "Bính Thân", napAm: "Hỏa", cungPhi: "Khôn" },
  day: { canChi: "Đinh Sửu", napAm: "Thủy", cungPhi: "Chấn" },
  hour: { canChi: "Ất Tỵ", napAm: "Hỏa", cungPhi: "Khôn" },
};

describe("TuTruPanel", () => {
  it("renders Can Chi, Nạp âm, and Cung Phi columns with Năm Tháng Ngày Giờ", () => {
    render(<TuTruPanel {...sample} />);
    const panel = screen.getByTestId("tu-tru-panel");
    expect(panel.textContent).toContain("TỨ TRỤ");
    expect(panel.textContent).toContain("Can Chi");
    expect(panel.textContent).toContain("Nạp âm");
    expect(panel.textContent).toContain("Cung Phi");
    expect(panel.textContent).toContain("Năm");
    expect(panel.textContent).toContain("Tháng");
    expect(panel.textContent).toContain("Ngày");
    expect(panel.textContent).toContain("Giờ");
    expect(panel.textContent).not.toContain("Mệnh");
    expect(panel.textContent).not.toContain("Ngũ hành");
  });

  it("renders supplied Can Chi values without inventing labels", () => {
    render(<TuTruPanel {...sample} />);
    const panel = screen.getByTestId("tu-tru-panel");
    expect(panel.textContent).toContain("Bính Ngọ");
    expect(panel.textContent).toContain("Bính Thân");
    expect(panel.textContent).toContain("Đinh Sửu");
    expect(panel.textContent).toContain("Ất Tỵ");
    const canChi = panel.querySelectorAll(".bte-tu-tru__can-chi");
    expect(canChi).toHaveLength(4);
    expect(canChi[0].className).toContain("bte-tu-tru__can-chi");
  });

  it("renders Nạp âm and Cung Phi as colored badges", () => {
    render(<TuTruPanel {...sample} />);
    const napAm = Array.from(document.querySelectorAll('[data-kind="nap-am"]')).map(
      (el) => el.textContent,
    );
    const cung = Array.from(document.querySelectorAll('[data-kind="cung-phi"]')).map(
      (el) => el.textContent,
    );
    expect(napAm).toEqual(["Thủy", "Hỏa", "Thủy", "Hỏa"]);
    expect(cung).toEqual(["Khảm", "Khôn", "Chấn", "Khôn"]);
    expect(document.querySelector('[data-kind="nap-am"]')?.className).toContain("bte-tu-tru__badge--thuy");
    expect(document.querySelector('[data-kind="cung-phi"]')?.className).toContain("bte-tu-tru__badge--thuy");
  });

  it("is reusable from supplied props only", () => {
    const { container } = render(
      <TuTruPanel
        year={{ canChi: "Canh Ngọ", napAm: "Thổ", cungPhi: "Đoài" }}
        month={{ canChi: "Tân Tỵ", napAm: "Kim", cungPhi: "Càn" }}
        day={{ canChi: "Giáp Tý", napAm: "Mộc", cungPhi: "Ly" }}
        hour={{ canChi: "Ất Tỵ", napAm: "Hỏa", cungPhi: "Khôn" }}
      />,
    );
    expect(container.querySelector("[data-canonical='tu-tru-panel']")).toBeTruthy();
    expect(container.textContent).toContain("Canh Ngọ");
    expect(container.textContent).toContain("Tân Tỵ");
    expect(container.textContent).toContain("Giáp Tý");
    expect(container.textContent).toContain("Ất Tỵ");
    expect(container.textContent).not.toContain("—");
    expect(container.querySelectorAll(".bte-tu-tru__empty")).toHaveLength(0);
    expect(container.textContent).not.toContain("date_selection");
    expect(container.textContent).not.toContain("Bazi");
  });
});
