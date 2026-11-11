import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";

const template = readFileSync(resolve(__dirname, "../../templates/name_analysis.html"), "utf8");
const script = readFileSync(resolve(__dirname, "../../static/js/name_analysis.js"), "utf8");
const authGate = readFileSync(resolve(__dirname, "../../static/js/auth_gate.js"), "utf8");

function responseData() {
  return {
    full_name: "Nguyễn Tiến Sơn", basis: "birth_chart",
    name_reading: {
      given_part: "Tiến Sơn", meaning: "Tên gọi gợi sự vững chãi.", element: "Thổ",
      family_part: "Nguyễn", middle_part: "Tiến", main_part: "Sơn",
      element_basis: "Sơn là núi.", parts: [{ word: "Sơn", meaning: "Núi.", element: "Thổ", known: true,
        han_characters: [{ character: "山", meaning: "núi" }], interpretation: "Hình ảnh ngọn núi gợi một điểm tựa vững chãi." }],
      han_viet: { phrase: "Tiến Sơn", paragraphs: ["Tiến gợi bước đi, Sơn gợi nền móng vững chãi.", "Tên có thể gửi gắm sự tiến bộ bền bỉ."], note: "Một âm tên có thể ứng với nhiều chữ Hán." },
      family_reading: {word: "Nguyễn", characters: "阮", paragraph: "Nguyễn là phần họ."},
      rhythm: {paragraph: "Tên gồm 3 tiếng.", tones: [{word: "Nguyễn", tone: "ngã", group: "Trắc"}, {word: "Tiến", tone: "sắc", group: "Trắc"}, {word: "Sơn", tone: "ngang", group: "Bằng"}]},
    },
    signals: { pillars: {year: "Bính Dần", month: "Tân Sửu", day: "Canh Ngọ", hour: "Mậu Dần"}, nap_am: "Lư Trung Hỏa", cung_phi: "Khôn", cung_phi_element: "Thổ" },
    fit: { level: "caution", title: "Cần cân nhắc theo Bát Tự", reason: "Hành tên trùng Kỵ thần." },
    factors: [{ label: "Kỵ thần", elements: ["Thổ", "Kim"], explanation: "Tên thuộc Thổ." }],
    comparisons: [{ label: "Nạp Âm", relation: "reference_generates_name", title: "Tương sinh", explanation: "Hỏa sinh Thổ." }],
    notes: [], notice: "Chỉ tham khảo.",
  };
}

function mount() {
  document.body.innerHTML = template;
  const fetcher = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ status: "SUCCESS", data: responseData() }) });
  vi.stubGlobal("fetch", fetcher);
  new Function(script)();
  const form = document.getElementById("name-analysis-form") as HTMLFormElement;
  (form.elements.namedItem("full_name") as HTMLInputElement).value = "Nguyễn Tiến Sơn";
  (form.elements.namedItem("gender") as HTMLSelectElement).value = "male";
  (form.elements.namedItem("birth_date") as HTMLInputElement).value = "1987-01-21";
  (form.elements.namedItem("birth_time") as HTMLSelectElement).value = "04:00";
  return { form, fetcher };
}

function submit(form: HTMLFormElement) {
  form.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
}

afterEach(() => {
  document.body.innerHTML = "";
  history.replaceState(null, "", "/");
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe("public current name analysis", () => {
  it("submits birth date and time without requiring credentials", async () => {
    const { form, fetcher } = mount();
    const savedItems = sessionStorage.length;
    submit(form);
    await vi.waitFor(() => expect(document.getElementById("na-result")?.hidden).toBe(false));
    const [url, options] = fetcher.mock.calls[0];
    expect(url).toBe("/backend/api/v1/public/naming/analyze-current-birth");
    expect(JSON.parse(options.body)).toEqual({ full_name: "Nguyễn Tiến Sơn", gender: "male", birth_date: "1987-01-21", birth_time: "04:00", timezone: "Asia/Ho_Chi_Minh" });
    expect(options.headers).not.toHaveProperty("Authorization");
    expect(document.getElementById("na-result")?.textContent).toContain("Lư Trung Hỏa");
    expect(document.getElementById("na-result")?.textContent).toContain("Cần cân nhắc theo Bát Tự");
    expect(sessionStorage.length).toBe(savedItems);
  });

  it("renders rich Han Viet paragraphs and possible characters as text", async () => {
    const { form } = mount();
    submit(form);
    await vi.waitFor(() => expect(document.getElementById("na-result")?.hidden).toBe(false));
    const section = document.querySelector(".na-han-viet");
    expect(section?.textContent).toContain("Luận nghĩa Hán–Việt");
    expect(section?.textContent).toContain("tiến bộ bền bỉ");
    expect(section?.textContent).toContain("nhiều chữ Hán");
    expect(section?.querySelector(".na-han-character")?.textContent).toBe("山");
    expect(section?.querySelectorAll(".na-prose").length).toBe(4);
    expect(document.querySelector(".na-name-structure")?.textContent).toContain("Tên chínhSơn");
    expect(document.querySelector(".na-rhythm")?.textContent).toContain("Sơn · ngang (bằng)");
  });

  it("keeps semantic reading prominent when a name has no assigned element", async () => {
    const { form, fetcher } = mount();
    const data = responseData();
    data.name_reading.element = "";
    data.fit = {level: "undetermined", title: "Tên chính trung tính về ngũ hành", reason: "Chưa xác định hành tên."};
    data.comparisons = [{label: "Nạp Âm", relation: "unresolved", title: "Chưa đủ cơ sở đối chiếu", explanation: "Chưa xác định hành tên."}];
    fetcher.mockResolvedValueOnce({ok: true, json: async () => ({status: "SUCCESS", data})});
    submit(form);
    await vi.waitFor(() => expect(document.getElementById("na-result")?.hidden).toBe(false));
    expect(document.querySelector(".na-han-viet")?.textContent).toContain("tiến bộ bền bỉ");
    expect(document.getElementById("na-result")?.textContent).toContain("Tên chính trung tính về ngũ hành");
    expect(document.getElementById("na-result")?.textContent).not.toContain("Chưa xác định hành của tên gọi.");
    expect(document.querySelectorAll(".na-comparisons > section").length).toBe(1);
    expect(document.getElementById("na-result")?.textContent).toContain("Bính Dần");
  });

  it("does not display a year-only response as a birth chart result", async () => {
    const { form, fetcher } = mount();
    const data = { ...responseData(), basis: "birth_year_only", birth_year: 1986 };
    fetcher.mockResolvedValueOnce({ ok: true, json: async () => ({ status: "SUCCESS", data }) });
    submit(form);
    await vi.waitFor(() => expect(document.getElementById("na-state")?.textContent).toContain("chưa hỗ trợ phân tích theo ngày giờ sinh"));
    expect(document.getElementById("na-result")?.hidden).toBe(true);
    expect((document.getElementById("na-fields") as HTMLFieldSetElement).disabled).toBe(false);
  });

  it.each(["1899-01-01", "1987-02-30", "2101-01-01"])("blocks invalid date %s before sending", (date) => {
    const { form, fetcher } = mount();
    (form.elements.namedItem("birth_date") as HTMLInputElement).value = date;
    submit(form);
    expect(fetcher).not.toHaveBeenCalled();
  });

  it("blocks missing gender", () => {
    const { form, fetcher } = mount();
    (form.elements.namedItem("gender") as HTMLSelectElement).value = "";
    submit(form);
    expect(fetcher).not.toHaveBeenCalled();
  });

  it("keeps returned names and explanations as text", async () => {
    const { form, fetcher } = mount();
    const data = responseData();
    data.full_name = '<img src=x onerror="alert(1)">';
    data.name_reading.meaning = "<script>alert(1)</script>";
    data.name_reading.han_viet.paragraphs[0] = "<img src=x onerror=alert(1)>";
    data.name_reading.parts[0].han_characters[0].character = "<script>alert(1)</script>";
    data.name_reading.family_reading.characters = "<img src=x onerror=alert(1)>";
    data.name_reading.rhythm.tones[0].word = "<script>alert(1)</script>";
    fetcher.mockResolvedValueOnce({ ok: true, json: async () => ({ status: "SUCCESS", data }) });
    submit(form);
    await vi.waitFor(() => expect(document.getElementById("na-result")?.hidden).toBe(false));
    expect(document.querySelector("#na-result img, #na-result script")).toBeNull();
    expect(document.getElementById("na-result")?.textContent).toContain(data.full_name);
  });

  it("clears stale results after input changes", async () => {
    const { form } = mount();
    submit(form);
    await vi.waitFor(() => expect(document.getElementById("na-result")?.hidden).toBe(false));
    (form.elements.namedItem("full_name") as HTMLInputElement).dispatchEvent(new Event("input", { bubbles: true }));
    expect(document.getElementById("na-result")?.hidden).toBe(true);
    expect(document.getElementById("na-result")?.textContent).toBe("");
  });

  it("shows a service failure and allows retry", async () => {
    const { form, fetcher } = mount();
    fetcher.mockResolvedValueOnce({ ok: false, json: async () => ({ status: "FAILED", errors: [{ message: "Vui lòng thử lại." }] }) });
    submit(form);
    await vi.waitFor(() => expect(document.getElementById("na-state")?.textContent).toBe("Vui lòng thử lại."));
    expect((document.getElementById("na-fields") as HTMLFieldSetElement).disabled).toBe(false);
    submit(form);
    await vi.waitFor(() => expect(document.getElementById("na-result")?.hidden).toBe(false));
    expect(fetcher).toHaveBeenCalledTimes(2);
  });

  it.each([false, true])("shows the public menu without redirecting guests; stale token=%s", async (staleToken) => {
    history.replaceState(null, "", "/name-analysis");
    document.body.innerHTML = '<nav><a href="/good-date" data-nav-id="home">Home</a><a href="/name-analysis" data-nav-id="name-analysis">Name</a><a href="/naming-consulting" data-nav-id="naming-consulting">Private</a></nav>';
    const portal = {
      getToken: () => staleToken ? "expired-token" : "", getUser: () => null,
      get: vi.fn().mockRejectedValue(new Error("expired")), clearSession: vi.fn(), setSession: vi.fn(),
    };
    vi.stubGlobal("BtePortal", portal);
    new Function(authGate)();
    if (document.readyState === "loading") document.dispatchEvent(new Event("DOMContentLoaded"));
    await vi.waitFor(() => expect((document.querySelector('[data-nav-id="name-analysis"]') as HTMLAnchorElement).hidden).toBe(false));
    if (staleToken) await vi.waitFor(() => expect(portal.clearSession).toHaveBeenCalled());
    expect((document.querySelector('[data-nav-id="home"]') as HTMLAnchorElement).hidden).toBe(false);
    expect((document.querySelector('[data-nav-id="naming-consulting"]') as HTMLAnchorElement).hidden).toBe(true);
    expect(location.pathname).toBe("/name-analysis");
  });
});
