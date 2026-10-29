import {readFileSync} from "node:fs";
import {resolve} from "node:path";
import {afterEach, expect, it, vi} from "vitest";
const adminRoot = resolve(__dirname, "../../../web_admin");
const apiScript = readFileSync(resolve(adminRoot, "static/js/api.js"), "utf8");
const accountScript = readFileSync(resolve(adminRoot, "static/js/accounts.js"), "utf8");
const memberScript = readFileSync(resolve(__dirname, "../../static/js/admin_membership.js"), "utf8");
const memberTemplate = readFileSync(resolve(adminRoot, "templates/membership.html"), "utf8");
function response(data:any, ok=true, status=200) { return {ok, status, text:async()=>JSON.stringify(data)}; }
afterEach(() => {
  sessionStorage.clear(); document.body.innerHTML = "";
  delete document.documentElement.dataset.adminSession;
  vi.unstubAllGlobals(); vi.restoreAllMocks();
});
it("reuses the portal session after the server verifies ADMIN", async () => {
  document.documentElement.dataset.adminSession = "portal";
  sessionStorage.setItem("bte_portal_token", "fake-admin-token");
  const fetcher = vi.fn().mockResolvedValueOnce(response({role:"ADMIN", username:"admin"})).mockResolvedValueOnce(response([]));
  vi.stubGlobal("fetch", fetcher); new Function(apiScript)();
  const admin = (window as any).BteAdmin;
  await admin.get("/api/v1/users");
  expect(fetcher.mock.calls.map(call=>call[0])).toEqual(["/backend/api/v1/auth/me", "/backend/api/v1/users"]);
  expect(fetcher.mock.calls[1][1].headers.Authorization).toBe("Bearer fake-admin-token");
  admin.clearSession(); expect(sessionStorage.getItem("bte_portal_token")).toBeNull();
});
it.each(["CUSTOMER", "CONSULTANT"])("blocks %s from loading admin data even with a cached ADMIN profile", async role => {
  document.documentElement.dataset.adminSession = "portal";
  sessionStorage.setItem("bte_portal_token", "fake-customer-token");
  sessionStorage.setItem("bte_portal_user", JSON.stringify({role:"ADMIN"}));
  const fetcher = vi.fn().mockResolvedValue(response({role, username:"customer"}));
  vi.stubGlobal("fetch", fetcher); new Function(apiScript)();
  await expect((window as any).BteAdmin.get("/api/v1/users")).rejects.toThrow("chỉ dành cho tài khoản ADMIN");
  expect(fetcher).toHaveBeenCalledTimes(1);
});
it("does not fetch admin data for guests", async () => {
  document.documentElement.dataset.adminSession = "portal";
  const fetcher = vi.fn(); vi.stubGlobal("fetch", fetcher); new Function(apiScript)();
  await expect((window as any).BteAdmin.get("/api/v1/membership/admin/applications")).rejects.toThrow("đăng nhập");
  expect(fetcher).not.toHaveBeenCalled();
});
it("renders registered names as text in the unified account list", async () => {
  document.body.innerHTML = readFileSync(resolve(adminRoot, "templates/accounts.html"), "utf8") + '<div id="globalFlash"></div>';
  const name = '<img src=x onerror="alert(1)">';
  vi.stubGlobal("BteAdmin", {get:vi.fn().mockResolvedValue([{username:"customer",display_name:name,is_active:true,analyses_used:0}]),fmt:(value:any)=>value??"—"});
  new Function(accountScript)();
  await vi.waitFor(()=>expect(document.getElementById("accountRows")?.textContent).toContain(name));
  expect(document.querySelector("#accountRows img")).toBeNull();
});
it.each(["memberships", "website-settings"])("shows the appropriate section of the shared %s page", async view => {
  document.body.innerHTML = memberTemplate.replaceAll("{{ACTIVE}}", view);
  const plan = {title:"Thử",registration_enabled:true,bank_name:"SHB"};
  const api = {get:vi.fn((path:string)=>Promise.resolve(path.endsWith("/me")?{role:"ADMIN"}:path.endsWith("/plan")?plan:{items:[]})),api:vi.fn(),post:vi.fn()};
  vi.stubGlobal("BteAdmin", api); new Function(memberScript)();
  await vi.waitFor(()=>expect((document.getElementById("memberAdminContent") as HTMLElement).hidden).toBe(false));
  expect((document.getElementById("memberSettingsForm") as HTMLElement).hidden).toBe(view==="memberships");
  expect((document.getElementById("memberApplicationsSection") as HTMLElement).hidden).toBe(view==="website-settings");
  if(view==="website-settings") expect(api.get).not.toHaveBeenCalledWith("/api/v1/membership/admin/applications");
});
