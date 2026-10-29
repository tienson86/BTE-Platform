import {readFileSync} from "node:fs";
import {resolve} from "node:path";
import {afterEach,beforeEach,expect,it,vi} from "vitest";
const portal=resolve(__dirname,"../.."), admin=resolve(__dirname,"../../../web_admin");
const read=(root:string,path:string)=>readFileSync(resolve(root,path),"utf8");
beforeEach(()=>{
  HTMLDialogElement.prototype.showModal=function(){this.open=true;};
  HTMLDialogElement.prototype.close=function(){this.open=false;};
});
afterEach(()=>{document.body.innerHTML="";vi.unstubAllGlobals();vi.restoreAllMocks();delete (window as any).BteAdminArchive;});
it("includes the phone number in a registration request",async()=>{
  document.body.innerHTML=read(portal,"templates/membership.html");
  const api={getToken:()=>"",get:vi.fn().mockResolvedValue({ready:true,analysis_limit:31}),post:vi.fn().mockRejectedValue(new Error("Thử nghiệm dừng trước đăng nhập"))};
  vi.stubGlobal("BtePortal",api);new Function(read(portal,"static/js/membership.js"))();
  await vi.waitFor(()=>expect((document.getElementById("memberRegisterFields") as HTMLFieldSetElement).disabled).toBe(false));
  const form=document.getElementById("memberRegisterForm") as HTMLFormElement,f=form.elements as any;
  f.display_name.value="Khách mới";f.phone.value="0912345678";f.username.value="newperson";f.password.value=f.password_confirmation.value="test-password-123";
  form.dispatchEvent(new Event("submit",{cancelable:true,bubbles:true}));
  await vi.waitFor(()=>expect(api.post).toHaveBeenCalledWith("/api/v1/membership/register",expect.objectContaining({phone:"0912345678",username:"newperson"})));
  expect(document.getElementById("memberAllowance")?.textContent).toContain("tính riêng");
});
it("lists registered customers with a call link and preserves per-tool usage when increasing a limit",async()=>{
  document.body.innerHTML=read(admin,"templates/customers.html");
  const user={username:"client",display_name:'<img src=x onerror="alert(1)">',phone:"0912345678",role:"CUSTOMER",is_active:true,analysis_limit:31,membership_status:"active",member_access:true,
    usage:[{label:"Tư vấn đặt tên",feature:"naming",limit:31,used:2,pending:0,remaining:29}]};
  const api={get:vi.fn().mockResolvedValue({items:[user]}),api:vi.fn().mockResolvedValue(user),post:vi.fn()};
  vi.stubGlobal("BteAdmin",api);new Function(read(admin,"static/js/registered_customers.js"))();
  await vi.waitFor(()=>expect(document.getElementById("registeredRows")?.textContent).toContain(user.display_name));
  expect(document.querySelector("#registeredRows img")).toBeNull();
  expect(document.querySelector('#registeredRows a[href="tel:0912345678"]')).not.toBeNull();
  (document.querySelector("#registeredRows button") as HTMLButtonElement).click();
  expect((document.getElementById("registeredDialog") as HTMLDialogElement).open).toBe(true);
  expect(document.getElementById("registeredUsage")?.textContent).toContain("Tư vấn đặt tên");
  const form=document.getElementById("registeredCustomerForm") as HTMLFormElement;
  (form.elements as any).analysis_limit.value="62";
  form.dispatchEvent(new Event("submit",{cancelable:true,bubbles:true}));
  await vi.waitFor(()=>expect(api.api).toHaveBeenCalledWith("PATCH","/api/v1/admin/registered-customers/client",expect.objectContaining({analysis_limit:62,phone:"0912345678"})));
  expect(api.api.mock.calls[0][2]).not.toHaveProperty("analyses_used");
});
it("keeps customer accounts out of internal account management",async()=>{
  document.body.innerHTML=read(admin,"templates/accounts.html")+'<div id="globalFlash"></div>';
  vi.stubGlobal("BteAdmin",{get:vi.fn().mockResolvedValue([{username:"internaladmin",role:"ADMIN"},{username:"publiccustomer",role:"CUSTOMER"}]),fmt:(value:any)=>value??"—"});
  new Function(read(admin,"static/js/accounts.js"))();
  await vi.waitFor(()=>expect(document.getElementById("accountRows")?.textContent).toContain("internaladmin"));
  expect(document.getElementById("accountRows")?.textContent).not.toContain("publiccustomer");
});
it("uses the unified archive for naming and contact records",async()=>{
  document.body.innerHTML=read(admin,"templates/cases.html");
  const items=[{kind:"naming",id:"name-1",customer_name:"Khách đặt tên",owner:"user:u-client",creator_username:"client",created_at:"2026-10-29"},
    {kind:"contact",id:"contact-1",customer_name:"Khách gọi",owner:"guest:1",creator_username:"Khách",phone:"0912345678",created_at:"2026-10-29"}];
  const api={get:vi.fn((path:string)=>Promise.resolve(path.endsWith("/me")?{role:"ADMIN"}:{items,total:2,users:["client"],counts:{naming:1,contact:1},warnings:[]})),getToken:()=>"test",showFlash:vi.fn()};
  vi.stubGlobal("BteAdmin",api);new Function(read(portal,"static/js/admin_archive.js"))();
  await (window as any).BteAdminArchive.start();
  expect(api.get).toHaveBeenCalledWith(expect.stringContaining("/api/v1/admin-archive?"));
  expect(document.getElementById("historyList")?.textContent).toContain("Đặt tên");
  expect(document.getElementById("historyList")?.textContent).toContain("Liên hệ hỗ trợ");
  expect(document.querySelector('[data-aa-download][data-format="pdf"]')).toBeNull();
  expect(document.querySelectorAll('[data-aa-download][data-format="json"]').length).toBe(2);
});
it("stores a support request without exposing response text as HTML",async()=>{
  document.body.innerHTML=read(portal,"templates/contact.html");
  const api={getToken:()=>"",post:vi.fn().mockResolvedValue({id:"CT-test",message:"Đã lưu yêu cầu"})};
  vi.stubGlobal("BtePortal",api);new Function(read(portal,"static/js/contact.js"))();
  const form=document.getElementById("supportForm") as HTMLFormElement,f=form.elements as any;
  f.full_name.value="Khách cần hỗ trợ";f.phone.value="0912345678";f.message.value="Tôi cần cấp thêm hạn mức";
  form.dispatchEvent(new Event("submit",{cancelable:true,bubbles:true}));
  await vi.waitFor(()=>expect(document.getElementById("supportState")?.textContent).toContain("CT-test"));
  expect(api.post).toHaveBeenCalledWith("/api/v1/contacts",expect.objectContaining({phone:"0912345678",message:"Tôi cần cấp thêm hạn mức"}));
});
