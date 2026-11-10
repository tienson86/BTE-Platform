import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { afterEach, expect, it, vi } from "vitest";
const script = readFileSync(resolve(__dirname, "../../static/js/auth_gate.js"), "utf8");
const publicPaths = ["/good-date", "/name-analysis", "/number-energy"];
const memberPaths = ["/analyze", "/choose-date", "/marriage-consulting", "/childbirth-consulting", "/naming-consulting", "/business-consulting", "/tinh-van-han"];
function mount(token: string, user: any, verify?: Promise<any>) {
  history.replaceState(null, "", "/number-energy");
  document.body.innerHTML = '<header><button id="btnNavToggle" hidden></button><nav>' + publicPaths.map((path, i) => `<a data-nav-id="public-${i}" href="${path}">Free</a>`).join("") + '</nav></header><aside id="memberSidebar" hidden>' + memberPaths.map((path, i) => `<a data-nav-id="member-${i}" href="${path}">Member</a>`).join("") + '<a data-admin-only hidden>Admin</a></aside><p id="siteAnnouncement" hidden></p>';
  const api = { getToken: () => token, getUser: () => ({role: "ADMIN"}), setSession: vi.fn(), clearSession: vi.fn(),
    get: vi.fn((path: string) => path.endsWith("/plan") ? Promise.resolve({public_notice: ""}) : verify || Promise.resolve(user)) };
  vi.stubGlobal("BtePortal", api);
  new Function(script)();
  if (document.readyState === "loading") document.dispatchEvent(new Event("DOMContentLoaded"));
  return api;
}
afterEach(() => { document.body.innerHTML = ""; vi.unstubAllGlobals(); vi.restoreAllMocks(); });
it("shows all three free tools to guests without showing the member sidebar", async () => {
  const api = mount("", null);
  await vi.waitFor(() => expect(api.get).toHaveBeenCalled());
  expect((document.getElementById("memberSidebar") as HTMLElement).hidden).toBe(true);
  expect([...document.querySelectorAll('[data-nav-id^="public-"]')].every(el => !(el as HTMLElement).hidden)).toBe(true);
  expect([...document.querySelectorAll('[data-nav-id^="member-"]')].every(el => (el as HTMLElement).hidden)).toBe(true);
});
it.each(["CUSTOMER", "ADMIN"])("shows the seven member tools after verifying a %s account", async role => {
  mount("test-token", {user_id: "member", role, member_access: true});
  await vi.waitFor(() => expect((document.getElementById("memberSidebar") as HTMLElement).hidden).toBe(false));
  expect(document.body.dataset.memberNav).toBe("true");
  expect(document.querySelectorAll('[data-nav-id^="member-"]').length).toBe(7);
  expect((document.querySelector("[data-admin-only]") as HTMLElement).hidden).toBe(role !== "ADMIN");
});
it("does not reveal member navigation using only a cached profile", async () => {
  let resolveUser: (value: any) => void = () => {};
  const promise = new Promise(resolve => { resolveUser = resolve; });
  mount("test-token", null, promise);
  expect((document.getElementById("memberSidebar") as HTMLElement).hidden).toBe(true);
  resolveUser({role: "CUSTOMER", member_access: true});
  await vi.waitFor(() => expect((document.getElementById("memberSidebar") as HTMLElement).hidden).toBe(false));
});
it("keeps free pages open and hides member tools for a stale token", async () => {
  const api = mount("expired", null, Promise.reject(new Error("expired")));
  await vi.waitFor(() => expect(api.clearSession).toHaveBeenCalled());
  expect(location.pathname).toBe("/number-energy");
  expect((document.getElementById("memberSidebar") as HTMLElement).hidden).toBe(true);
});
