import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { afterEach, expect, it, vi } from "vitest";

const script = readFileSync(resolve(__dirname, "../../static/js/consulting_session.js"), "utf8");
afterEach(() => { vi.unstubAllGlobals(); document.body.replaceChildren(); });

it("shows an accessible quota alert for portal and consulting tools without consuming the response", async () => {
  document.body.innerHTML = '<main id="mainContent"></main>';
  vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({code:"quota_exhausted"}), {status:429})));
  vi.stubGlobal("BtePortal", {getToken:() => "member"});
  new Function(script)();
  for (const path of ["/backend/api/v1/van-han/good-years/analyze", "/backend/api/v1/consulting/naming/analyze"]) {
    const response = await fetch(path, {method:"POST"});
    expect(await response.json()).toEqual({code:"quota_exhausted"});
    const alert = document.querySelector("#quotaWarning")!;
    expect(alert.getAttribute("role")).toBe("alert");
    expect(document.activeElement).toBe(alert);
    expect(alert.querySelector('a[href="/linh-thach"]')).toBeTruthy();
    expect(alert.querySelector('a[href="/thanh-vien-bte"]')).toBeTruthy();
    (alert.querySelector("button") as HTMLButtonElement).click();
    expect(document.querySelector("#quotaWarning")).toBeNull();
  }
});
