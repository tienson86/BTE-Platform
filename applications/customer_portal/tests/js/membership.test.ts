import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { afterEach, expect, it, vi } from "vitest";
const template = readFileSync(resolve(__dirname, "../../templates/membership.html"), "utf8");
const script = readFileSync(resolve(__dirname, "../../static/js/membership.js"), "utf8");
const adminTemplate = readFileSync(resolve(__dirname, "../../templates/admin_membership.html"), "utf8");
const adminScript = readFileSync(resolve(__dirname, "../../static/js/admin_membership.js"), "utf8");
const plan = {title: "Thành viên BTE", description: "Giới thiệu", amount_vnd: 100000, validity_days: 365, analysis_limit: null,
  bank_name: "SHB", bank_account: "28676875", bank_holder: "Nguyễn Tiến Sơn", ready: true, registration_enabled: true, public_notice: "", payment_note: "Chuyển đúng mã"};
function details(status = "pending", access = false) {
  return { user: {user_id: "new-user", username: "test", display_name: "Khách thử", member_access: access, role: "CUSTOMER"},
    membership: {status, reference: "BTEABC123", plan: {...plan}, payment_note: "", payment_reported_at: null, expires_at: "2027-10-29T00:00:00+00:00"}, transfer_content: "Khách thử test", transfer_instructions_updated: false };
}
function mount(token = "", data = details(), ready = true) {
  document.body.innerHTML = template;
  const api = {getToken: () => token, setSession: vi.fn(), get: vi.fn((path: string) => Promise.resolve(path.endsWith("/plan") ? {...plan, ready} : data)), post: vi.fn().mockResolvedValue(data)};
  vi.stubGlobal("BtePortal", api); new Function(script)(); return api;
}
afterEach(() => { document.body.innerHTML = ""; vi.unstubAllGlobals(); vi.restoreAllMocks(); });
it("waits for an actual price configuration before allowing paid registration", async () => {
  mount("", details(), false);
  await vi.waitFor(() => expect(document.getElementById("membershipState")?.textContent).toContain("biểu phí"));
  expect((document.getElementById("memberRegisterFields") as HTMLFieldSetElement).disabled).toBe(true);
});
it("renders the full name and username as transfer content without the internal code", async () => {
  mount("test-token");
  await vi.waitFor(() => expect(document.getElementById("memberAccount")?.hidden).toBe(false));
  expect(document.getElementById("memberAccount")?.textContent).toContain("28676875");
  expect(document.getElementById("memberAccount")?.textContent).toContain("Nội dung chuyển khoản: Khách thử test");
  expect(document.getElementById("memberAccount")?.textContent).not.toContain("BTEABC123");
  expect(document.getElementById("memberAccount")?.textContent).not.toContain("Mã đăng ký");
  expect(document.querySelector('#memberAccount a[href="/analyze"]')).toBeNull();
});
it("labels the registration name field Họ và Tên", async () => {
  mount();
  await vi.waitFor(() => expect((document.getElementById("memberRegisterForm") as HTMLFormElement).hidden).toBe(false));
  expect(document.querySelector('label:has(input[name="display_name"])')?.textContent).toBe("Họ và Tên");
});
it("places duplicate username errors beside the field and lets the customer correct it", async () => {
  const api = mount();
  await vi.waitFor(() => expect((document.getElementById("memberRegisterFields") as HTMLFieldSetElement).disabled).toBe(false));
  const form = document.getElementById("memberRegisterForm") as HTMLFormElement;
  const fields = form.elements as any;
  fields.display_name.value = "Nguyễn Văn An"; fields.username.value = "existing";
  fields.password.value = fields.password_confirmation.value = "test-password-123";
  api.post.mockRejectedValueOnce(Object.assign(new Error("Tên đăng nhập đã có người dùng rồi."), {status:409, payload:{code:"username_taken"}}));
  form.dispatchEvent(new Event("submit", {bubbles:true, cancelable:true}));
  const error = document.getElementById("memberUsernameError") as HTMLElement;
  await vi.waitFor(() => expect(error.hidden).toBe(false));
  expect(error.textContent).toContain("Bạn hãy chọn tên đăng nhập khác");
  expect(error.classList.contains("member-field-error")).toBe(true);
  expect(fields.username.getAttribute("aria-invalid")).toBe("true");
  expect(document.activeElement).toBe(fields.username);
  expect(fields.display_name.value).toBe("Nguyễn Văn An");
  expect(api.post).toHaveBeenCalledTimes(1);
  expect(api.setSession).not.toHaveBeenCalled();
  fields.username.value = "new-name";
  fields.username.dispatchEvent(new Event("input", {bubbles:true}));
  expect(error.hidden).toBe(true);
  expect(fields.username.hasAttribute("aria-invalid")).toBe(false);
  api.post.mockRejectedValueOnce(new Error("Máy chủ đang bận."));
  form.dispatchEvent(new Event("submit", {bubbles:true, cancelable:true}));
  await vi.waitFor(() => expect(document.getElementById("memberRegisterError")?.textContent).toContain("Máy chủ đang bận"));
  expect(error.hidden).toBe(true);
});
it("tells old pending customers they do not need to transfer again", async () => {
  const data = details(); data.transfer_instructions_updated = true;
  mount("test-token", data);
  await vi.waitFor(() => expect(document.getElementById("memberAccount")?.textContent).toContain("không cần chuyển lại"));
  expect(document.getElementById("memberAccount")?.textContent).not.toContain("BTEABC123");
});
it("reports payment without sending a role or a request to activate membership", async () => {
  const api = mount("test-token");
  await vi.waitFor(() => expect(document.getElementById("memberPaymentForm")).not.toBeNull());
  (document.querySelector('[name="payment_note"]') as HTMLTextAreaElement).value = "Giao dịch thử";
  document.getElementById("memberPaymentForm")?.dispatchEvent(new Event("submit", {bubbles: true, cancelable: true}));
  await vi.waitFor(() => expect(api.post).toHaveBeenCalledWith("/api/v1/membership/payment-notice", {note: "Giao dịch thử"}));
  expect(document.getElementById("membershipState")?.textContent).toContain("sau khi quản trị viên xác nhận");
});
it("only links to paid tools and saved downloads for an active member", async () => {
  mount("test-token", details("active", true));
  await vi.waitFor(() => expect(document.querySelector('#memberAccount a[href="/analyze"]')).not.toBeNull());
  expect(document.querySelector('#memberAccount a[href="/history"]')).not.toBeNull();
});
it("does not render configured or user-supplied text as HTML", async () => {
  const data = details(); data.user.display_name = "<img src=x onerror=alert(1)>";
  mount("test-token", data);
  await vi.waitFor(() => expect(document.getElementById("memberAccount")?.hidden).toBe(false));
  expect(document.querySelector("#memberAccount img")).toBeNull();
  expect(document.getElementById("memberAccount")?.textContent).toContain(data.user.display_name);
});
it("requires explicit transaction verification before the admin approval action", async () => {
  document.body.innerHTML = adminTemplate;
  const data = details();
  const api = {get: vi.fn((path: string) => Promise.resolve(path.endsWith("/me") ? {role: "ADMIN"} : path.endsWith("/plan") ? plan : {items: [data]})), post: vi.fn(), api: vi.fn()};
  vi.stubGlobal("BtePortal", api); new Function(adminScript)();
  await vi.waitFor(() => expect(document.querySelector(".membership-application")).not.toBeNull());
  expect(document.querySelector(".membership-application")?.textContent).toContain("Mã đăng ký nội bộ: BTEABC123");
  expect(document.querySelector(".membership-application")?.textContent).toContain("Nội dung chuyển khoản: Khách thử test");
  expect(document.querySelector('.membership-application label.check')?.textContent).toContain("nội dung chuyển khoản: Khách thử test");
  const buttons = document.querySelectorAll(".membership-application button");
  (buttons[0] as HTMLButtonElement).click();
  expect(api.post).not.toHaveBeenCalled();
  expect(document.getElementById("memberAdminState")?.textContent).toContain("đối chiếu khoản tiền");
  (document.querySelector('.membership-application input[type="checkbox"]') as HTMLInputElement).checked = true;
  api.post.mockResolvedValue(details("active", true));
  (buttons[0] as HTMLButtonElement).click();
  await vi.waitFor(() => expect(api.post).toHaveBeenCalledWith("/api/v1/membership/admin/applications/new-user/review", {decision: "approve", expected_reference: "BTEABC123", note: ""}));
});
