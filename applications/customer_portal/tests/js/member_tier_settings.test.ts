import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { afterEach, expect, it, vi } from "vitest";

const template=readFileSync(resolve(__dirname,"../../templates/admin_membership.html"),"utf8");
const script=readFileSync(resolve(__dirname,"../../static/js/admin_membership.js"),"utf8");
const publicTemplate=readFileSync(resolve(__dirname,"../../templates/member_plans.html"),"utf8");
const publicScript=readFileSync(resolve(__dirname,"../../static/js/member_plans_catalog.js"),"utf8");
const features={bazi:"Xem lá số",date_selection:"Chọn ngày tốt",marriage:"Tư vấn hôn nhân",childbirth:"Tư vấn sinh con",naming:"Tư vấn đặt tên",business:"Tư vấn hợp tác",van_han:"Tính vận hạn"};
function settings() {
  return {title:"BTE",description:"Giới thiệu",public_notice:"",public_base_url:"",bank_name:"SHB",bank_account:"123456",bank_holder:"Chủ tài khoản",payment_note:"Ghi chú",
    amount_vnd:2777777,validity_days:368,analysis_limit:27,registration_enabled:true,ready:true,revision:"revision-1",features,
    tiers:[1,2,3].map(tier=>({tier,title:"Cấp "+tier,amount_vnd:100000*tier,validity_days:30*tier,analysis_limit:2,referral_reward:10*tier,enabled:true,
      feature_limits:Object.fromEntries(Object.keys(features).map(feature=>[feature,2])),enabled_features:Object.keys(features)}))};
}
afterEach(()=>{document.body.innerHTML="";vi.unstubAllGlobals();vi.restoreAllMocks();});

it("renders editable tier panels and sends individual quotas with the configuration revision",async()=>{
  document.body.innerHTML=template;
  const data=settings();
  const api={get:vi.fn((path:string)=>Promise.resolve(path.endsWith("/auth/me")?{role:"ADMIN"}:path.endsWith("/settings")?data:{items:[]})),
    api:vi.fn().mockResolvedValue({}),post:vi.fn()};
  vi.stubGlobal("BtePortal",api);new Function(script)();
  await vi.waitFor(()=>expect(document.querySelectorAll("#memberTierSettings [data-tier]")).toHaveLength(3));
  const tier=document.querySelector('[data-tier="1"]')!;
  (tier.querySelector('[data-tier-field="amount_vnd"]') as HTMLInputElement).value="999999";
  (tier.querySelector('[data-tier-field="validity_days"]') as HTMLInputElement).value="45";
  (tier.querySelector('[data-feature="naming"] input[type="number"]') as HTMLInputElement).value="7";
  (tier.querySelector('[data-feature="marriage"] input[type="checkbox"]') as HTMLInputElement).checked=false;
  const form=document.getElementById("memberSettingsForm") as HTMLFormElement;
  form.dispatchEvent(new Event("submit",{bubbles:true,cancelable:true}));
  await vi.waitFor(()=>expect(api.api).toHaveBeenCalledTimes(1));
  const [method,path,payload,options]=api.api.mock.calls[0];
  expect([method,path]).toEqual(["PUT","/api/v1/membership/admin/settings"]);
  expect(payload.tiers[0].amount_vnd).toBe(999999);
  expect(payload.tiers[0].validity_days).toBe(45);
  expect(payload.tiers[0].feature_limits.naming).toBe(7);
  expect(payload.tiers[0].enabled_features).not.toContain("marriage");
  expect(options.headers["If-Match"]).toBe("revision-1");
});

it("shows current admin prices and permissions publicly and stops registration for a closed tier",async()=>{
  document.body.innerHTML=publicTemplate;
  const data=settings();
  data.tiers[0].amount_vnd=919191;
  data.tiers[0].feature_limits.naming=8;
  data.tiers[1].enabled=false;
  vi.stubGlobal("BtePortal",{get:vi.fn().mockResolvedValue(data)});
  new Function(publicScript)();
  await vi.waitFor(()=>expect(document.querySelector('[data-tier="1"] [data-tier-price]')?.textContent).toContain("919.191"));
  expect(document.querySelector('[data-tier="1"] [data-tier-rights]')?.textContent).toContain("Tư vấn đặt tên — 8 lượt");
  expect(document.querySelector('[data-tier="2"] [data-tier-register]')?.getAttribute("href")).toBeNull();
  expect(document.querySelector('[data-tier="2"] [data-tier-register]')?.textContent).toBe("Tạm ngừng đăng ký");
});

it("tells readers when the current price cannot be loaded",async()=>{
  document.body.innerHTML=publicTemplate;
  vi.stubGlobal("BtePortal",{get:vi.fn().mockRejectedValue(new Error("offline"))});
  new Function(publicScript)();
  await vi.waitFor(()=>expect(document.getElementById("memberPlansState")?.textContent).toContain("Chưa tải được biểu phí"));
  expect(document.body.textContent).not.toContain("688.888");
});
