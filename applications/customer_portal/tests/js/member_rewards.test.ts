import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { afterEach, expect, it, vi } from "vitest";

const script = readFileSync(resolve(__dirname, "../../static/js/member_rewards.js"), "utf8");
const rewards = {balance:10,referral_code:"BTE-TEST",referral_base_url:"https://bte.example.vn",usage:[],entries:[],referral_tiers:[{tier:1,title:"Cấp 1",discounted_amount_vnd:551110,referral_reward:10,enabled:true},{tier:2,title:"Cấp 2",discounted_amount_vnd:2222222,referral_reward:50,enabled:true},{tier:3,title:"Cấp 3",discounted_amount_vnd:10666666,referral_reward:100,enabled:true}]};
afterEach(() => {document.body.innerHTML="";vi.unstubAllGlobals();delete (window as any).BteMemberRewards;});

it("keeps referral promotion and link out of the member status wallet", async () => {
  document.body.innerHTML='<section id="memberRewards"></section>';
  vi.stubGlobal("BtePortal",{get:vi.fn().mockResolvedValue(rewards)});
  new Function(script)();
  await (window as any).BteMemberRewards.render("memberRewards");
  const host=document.getElementById("memberRewards")!;
  expect(host.textContent).toContain("10 Linh Thạch");
  expect(host.textContent).not.toContain("Giới thiệu bạn đồng hành");
  expect(host.textContent).not.toContain("giảm 20%");
  expect(host.textContent).not.toContain("BTE-TEST");
  expect(host.querySelector("input")).toBeNull();
});

it("shows the full policy only inside the member referral share page", async () => {
  document.body.innerHTML='<section id="referralRewards"></section>';
  vi.stubGlobal("BtePortal",{get:vi.fn().mockResolvedValue(rewards)});
  new Function(script)();
  await vi.waitFor(() => expect(document.body.textContent).toContain("Giới thiệu bạn đồng hành — Cùng nhận ưu đãi"));
  expect(document.body.textContent).toContain("nhận 10 Linh Thạch");
  expect(document.body.textContent).toContain("nhận 50 Linh Thạch");
  expect(document.body.textContent).toContain("nhận 100 Linh Thạch");
  expect(document.body.textContent).toContain("admin xác nhận");
  expect(document.querySelector("input")?.value).toBe("https://bte.example.vn/membership?ref=BTE-TEST");
});

it("renders no promotion when authenticated reward access is refused", async () => {
  document.body.innerHTML='<section id="referralRewards"></section>';
  vi.stubGlobal("BtePortal",{get:vi.fn().mockRejectedValue(new Error("Vui lòng đăng nhập"))});
  new Function(script)();
  await vi.waitFor(() => expect(document.body.textContent).toContain("Vui lòng đăng nhập"));
  expect(document.body.textContent).not.toContain("Giới thiệu bạn đồng hành");
  expect(document.querySelector("input")).toBeNull();
});
