import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
const source = readFileSync(resolve("static/js/childbirth_consulting.js"), "utf8");
const template = readFileSync(resolve("templates/childbirth_consulting.html"), "utf8");
const year = new Date().getFullYear();
const person = (name: string, date: string) => ({full_name:name,birth_date:date,birth_time:"04:00",birth_place:{display_name:"Hà Nội"}});
const profile = {consultation_id:"CB-test",saved_at:"2026-11-13T00:00:00Z",input:{father:person("Bố thử","1990-01-01"),mother:person("Mẹ thử","1992-02-02"),options:{start_year:year,years_ahead:12}},start_year:year,years_ahead:12,parents:{},recommendations:[],summary:{headline:"Kết quả thử"},eligibility:{rule:"Quy tắc tuổi",ineligible_years:[]},notice:"Không thay thế tư vấn bác sĩ"};
const response = (data: unknown) => Promise.resolve({ok:true,json:async()=>({status:"SUCCESS",data})});
const settle = async () => {for(let i=0;i<10;i++) await Promise.resolve();};
beforeEach(()=>{window.history.replaceState({},"","/");document.body.innerHTML=template;vi.stubGlobal("fetch",vi.fn(()=>response({items:[]})));});
afterEach(()=>vi.unstubAllGlobals());
function start(){window.eval(source);}
function fill(){(document.querySelector("#cb-father-date") as HTMLInputElement).value="01/01/1990";(document.querySelector("#cb-mother-date") as HTMLInputElement).value="02/02/1992";}
function submit(){document.querySelector("form")!.dispatchEvent(new Event("submit",{bubbles:true,cancelable:true}));}
describe("childbirth UI review",()=>{
 it("restores direct archive input and locks submission while it loads",async()=>{
  window.history.replaceState({},"","/?archive_id=CB-test");
  let finish:(value:unknown)=>void=()=>{};
  vi.stubGlobal("fetch",vi.fn((url:string)=>url.endsWith("/history")?response({items:[]}):new Promise(resolve=>{finish=resolve;})));
  start();expect((document.querySelector("[data-testid=submit-childbirth]") as HTMLButtonElement).disabled).toBe(true);
  fill();submit();expect(fetch).toHaveBeenCalledTimes(2);
  finish({ok:true,json:async()=>({status:"SUCCESS",data:profile})});await settle();
  expect((document.querySelector("#cb-father-name") as HTMLInputElement).value).toBe("Bố thử");
  expect((document.querySelector("#cb-mother-date") as HTMLInputElement).value).toBe("02/02/1992");
  expect((document.querySelector("[data-testid=submit-childbirth]") as HTMLButtonElement).disabled).toBe(false);
 });
 it("refreshes history after autosave and shows the medical limitation",async()=>{
  const mock=vi.fn((url:string)=>url.endsWith("/history")?response({items:[]}):response(profile));vi.stubGlobal("fetch",mock);
  start();await settle();fill();submit();await settle();
  expect(mock.mock.calls.filter(([url])=>url.endsWith("/history"))).toHaveLength(2);
  expect(document.querySelector("[data-testid=childbirth-result]")!.textContent).toContain("Không thay thế tư vấn bác sĩ");
  expect((document.querySelector("[data-cb-action=save]") as HTMLButtonElement).disabled).toBe(true);
 });
 it.each([String(year-1),String(year+0.5),"9999"])("rejects invalid start %s without submitting",async(value)=>{
  start();await settle();fill();(document.querySelector("#cb-start-year") as HTMLInputElement).value=value;submit();await settle();
  expect(fetch).toHaveBeenCalledTimes(1);expect(document.querySelector("[data-testid=childbirth-state]")!.textContent).toContain("Nhập năm bắt đầu");
 });
 it("explains missing time instead of asking to expand the years",async()=>{
  vi.stubGlobal("fetch",vi.fn((url:string)=>url.endsWith("/history")?response({items:[]}):response({...profile,analysis_status:"insufficient_data",summary:{headline:"Cần bổ sung giờ sinh",note:"Chưa biết giờ sinh của mẹ."}})));
  start();await settle();fill();submit();await settle();
  expect(document.querySelector("[data-testid=childbirth-result]")!.textContent).toContain("Chưa xếp hạng năm");
  expect(document.querySelector("[data-testid=childbirth-result]")!.textContent).not.toContain("Hãy mở rộng số năm");
 });
});
