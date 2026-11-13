import{Q as H,c as U,m as V,R as Q,C as q,S as Y,I as W,L as X,D as B,l as J,T as Z,U as nn,b as tn,d as en,z as rn,e as sn,V as on,p as an,W as cn,r as un,o as ln,k as hn,w as fn,a as R,f as gn,s as dn}from"./currentResult-DmCVLR6R.js";const mn=new Set(["Khảm","Ly","Chấn","Tốn"]),pn=new Set(["Càn","Khôn","Cấn","Đoài"]),bn={Khảm:"Thủy",Ly:"Hỏa",Chấn:"Mộc",Tốn:"Mộc",Càn:"Kim",Khôn:"Thổ",Cấn:"Thổ",Đoài:"Kim"};function yn(n){return n==null?"":String(n).trim()}function f(n){return!n||typeof n!="object"||Array.isArray(n)?{}:n}function _(...n){for(const t of n){const e=yn(t);if(e)return e}return""}function $n(n){return mn.has(n)?"Đông Tứ Trạch":pn.has(n)?"Tây Tứ Trạch":""}function _n(n){return bn[n]||""}function Tn(n,t=""){const e=n??{},r=f(e.calendar),i=f(e.feng_shui),c=f(e.identity),h=f(c.person),m=f(c.four_pillars),y=f(m.year),p=f(e.bazi),u=f(p.year_pillar),x=f(r.ganzhi_routing),b=f(x.year);_(t,h.gender,f(e.customer).gender);const d=_(b.cung_phi,u.cung_phi,y.cung_phi),S=_(r.cung_phi,r.menh_quai),$=_(S,i.cung_phi,i.gua_name,i.menh_quai,d),C=$n($),k=_(r.nhom_trach,r.house_group,i.nhom_trach,i.house_group),v=C||k,E=_(_n($),r.hanh_cung);return{cungPhi:$,menhQuai:$,hanhCung:E,nhomTrach:v}}const xn=new Set(["male","nam","m","1","man","boy"]),Sn=new Set(["female","nu","nữ","f","woman","girl"]);function Cn(n){const t=(n??"").trim().toLowerCase();return t?xn.has(t)?"male":Sn.has(t)?"female":null:null}function kn(n){const t=Cn(n);return t==="male"?"Nam":t==="female"?"Nữ":"—"}function vn(n,t){return kn((n==null?void 0:n.gender_label)||(n==null?void 0:n.gender)||t)}const T="Chưa đủ dữ liệu để đưa ra kết luận.",En=[/kích hoạt khi/i,/áp dụng bảng/i,/ưu tiên xác định/i,/matched[_ ]?rules?/i,/rule[_ ]?id/i,/nếu chưa có tiết khí/i,/xác định mùa theo/i,/không thay thế kết luận phân tích/i,/presentation layer/i,/pack[_\s]?\d+/i,/knowledge base\s*·/i,/\(mock\)/i,/placeholder/i,/chờ engine/i,/sẽ được nối/i];function Nn(n){const t=(n??"").trim();return t?En.some(e=>e.test(t)):!0}function N(n){const t=(n??"").trim();return!t||Nn(t)?T:t}function I(n,t=160){var i;const e=N(n);if(e===T)return e;const r=((i=e.split(/[.\n]/)[0])==null?void 0:i.trim())||e;return r.length<=t?r:`${r.slice(0,t-1).trimEnd()}…`}function tt(n){const t=n==null?void 0:n.sections;return Array.isArray(t)?t.filter(e=>!!e&&typeof e=="object").map((e,r)=>({id:String(e.id??`section-${r+1}`),title:String(e.title??"").trim(),body:String(e.body??e.content??e.text??"").trim()})).filter(e=>e.body.length>0||e.title.length>0):[]}function et(n,t){for(const e of n){const r=e.title.toLowerCase();if(t.some(i=>i.test(r)))return e.body}return""}function D(n){if(!n||typeof n!="object")return null;const t=n;return t.capability_id!=="CAP-D1-CA-SEL"&&!t.career_direction?null:n}function An(n){var t;return n?D(n.career_selection_assessment)||D((t=n.commercial_knowledge_bundle)==null?void 0:t.career_selection_assessment):null}function Ln(n,t){if(!n)return"";const e=n[t];if(!e||typeof e!="object")return"";const r=e.text;return r==null?"":String(r).trim()}function M(n){if(!n||typeof n!="object")return null;const t=n;return t.capability_id!=="CAP-D1-CA-PRO"&&!t.promotion_readiness?null:n}function rt(n){var t;return n?M(n.promotion_readiness_assessment)||M((t=n.commercial_knowledge_bundle)==null?void 0:t.promotion_readiness_assessment):null}function it(n,t){if(!n)return"";const e=n[t];if(!e||typeof e!="object")return"";const r=e.text;return r==null?"":String(r).trim()}function st(n){return n!=null&&n.commercial_executive_summary?n.commercial_executive_summary:null}function ot(n){return n!=null&&n.primary_recommendation?n.primary_recommendation:null}function at(n){return n!=null&&n.secondary_career_milestone?n.secondary_career_milestone:null}function Gn(n){if(!n||typeof n!="object")return null;const t=n;return!t.summary&&!Array.isArray(t.sections)?null:n}function z(n){return n?n.contract==="pack05_narrative_result_v1"?!0:!!n.summary||Array.isArray(n.sections)&&n.sections.length>0:!1}function ct(n,t){if(!n)return T;const e=n[t];if(Array.isArray(e)){const r=e.map(String).filter(Boolean).join("; ");return N(r)}return N(e==null?"":String(e))}function ut(n,t){const r=(n.sections??[]).filter(c=>{const h=`${c.id??""} ${c.intent??""} ${c.title??""}`;return t.test(h)}),i=[];for(const c of r)for(const h of c.paragraphs??[]){if(h.insufficient_data)continue;const m=I(h.text);m!==T&&i.push(m)}return i}function lt(n){const t=n.recommendations??[],e=(n.sections??[]).flatMap(c=>c.recommendations??[]),r=[...t,...e],i=[];for(const c of r){if(c.insufficient_data)continue;const h=I(c.action);h!==T&&i.push(h)}return i}function ht(n,t){for(const e of n.sections??[])for(const r of e.paragraphs??[])if((r.role??"").toLowerCase()===t.toLowerCase()&&!r.insufficient_data)return N(r.text);return T}const Pn=[{id:"executive_summary",title:"Tóm tắt điều hành",match:/executive|summary|tóm tắt/i},{id:"observation",title:"Quan sát",match:/observation|quan sát/i},{id:"reasoning",title:"Lý giải",match:/reasoning|explanation|lý giải/i},{id:"impact",title:"Tác động",match:/impact|ảnh hưởng|tác động/i},{id:"recommendation",title:"Khuyến nghị",match:/recommendation|suggestion|khuyến/i},{id:"warning",title:"Lưu ý",match:/warning|caution|cảnh báo|lưu ý/i},{id:"conclusion",title:"Kết luận",match:/conclusion|kết luận/i}],jn=[{key:"year",label:"Năm",field:"year_pillar"},{key:"month",label:"Tháng",field:"month_pillar"},{key:"day",label:"Ngày",field:"day_pillar"},{key:"hour",label:"Giờ",field:"hour_pillar"}],F=/^(last-result|last_result|bte_last_result|bte_history|bte_view_result)$/i;function ft(n,t={}){var C,k,v,E,L,G;const e=t.input||{},r=n.calendar||{},i=n.bazi||{},c=Mn(n.pattern),h=U(n),m=V(n),y=Tn(n),p=n.score||{},u=n.luck,x=Gn(n.narrative_result),b=Q(n)||{Mộc:0,Hỏa:0,Thổ:0,Kim:0,Thủy:0},d=u==null?void 0:u.current_cycle,S=o(d==null?void 0:d.gan_zhi),$=((u==null?void 0:u.cycles)??[]).map(l=>{const P=o(l.gan_zhi),K=l.year_start!=null&&l.year_end!=null?`${l.year_start}–${l.year_end}`:"",j=o(l.stem_element),w=o(l.branch_element),O=[l.stem&&j?`${o(l.stem)} · ${j}`:"",l.branch&&w?`${o(l.branch)} · ${w}`:""].filter(Boolean).join(" / ");return{label:P,years:K,current:!!S&&P===S,elements:O}});return{analysisId:Dn(t.analysisId,n,e),customerName:o(((C=n.customer)==null?void 0:C.full_name)||e.full_name),gender:vn(n.customer,o(e.gender)),birthPlace:o(((k=n.customer)==null?void 0:k.birth_place)||e.birth_place),timezone:o(((v=n.customer)==null?void 0:v.timezone)||e.timezone,"Asia/Ho_Chi_Minh"),solarDate:Fn(r.solar_date,e),lunarDate:o(r.lunar_date),birthTime:In(e),dayMaster:o(i.day_master),dayMasterElement:o(i.day_master_element),yinYang:o(i.day_master_yin_yang),strengthLabel:hn(n)||o((E=n.strength)==null?void 0:E.strength_level),strengthScore:(()=>{const l=un(n);return l==null?"":ln(l)})(),strengthEvidence:an(n)||B(cn(n)),pattern:o(c.cach_cuc)||o(c.pattern),patternEvidence:on(n),usefulGod:sn(h),usefulGodReason:rn(h),hyThan:en(h),kyThan:tn(h),fiveElements:[{name:"Mộc",count:b.Mộc},{name:"Hỏa",count:b.Hỏa},{name:"Thổ",count:b.Thổ},{name:"Kim",count:b.Kim},{name:"Thủy",count:b.Thủy}],tenGods:nn(n),hiddenTenGods:Z(n),tenGodsNote:m.othersLine||String(((L=n.ten_gods)==null?void 0:L.note)||((G=n.ten_gods_result)==null?void 0:G.note)||"").trim()||"Xác định theo quan hệ Ngũ hành và âm dương với Nhật chủ.",tenGodsFeatured:m.featured,tenGodsOthersLine:m.othersLine,pillars:jn.map(l=>wn(i[l.field],l,n)),shenSha:J(n),luckStartAge:(u==null?void 0:u.start_age)!=null?String(u.start_age):"",luckCurrent:d?[o(d.gan_zhi),d.year_start!=null?`${d.year_start}–${d.year_end}`:""].filter(Boolean).join(" "):"",luckDirection:o(u==null?void 0:u.direction_label),luckEvidence:B(o(u==null?void 0:u.evidence)),luckMethod:o(u==null?void 0:u.method_note),luckCycles:$,cungPhi:y.cungPhi,menhQuai:y.menhQuai,hanhCung:y.hanhCung,nhomTrach:y.nhomTrach,tamNguyen:o(r.tam_nguyen),cuuVan:o(r.cuu_van),scoreLabel:p.total_score!=null&&p.grade?`${p.total_score} / ${p.grade}`:o(p.grade),climateState:X(n),balancingNeed:W(n),climateEvidence:Y(n),climatePreference:q(h),narrative:Bn(x),supporting:Rn(x),factsOnly:!1}}function gt(n){const t=n.customerName?`Báo cáo Bát Tự — ${n.customerName}`:"Báo cáo Bát Tự";return`<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8" /><title>${s(t)}</title>${Zn()}</head><body>
<article class="bte-full-report" data-report="canonical-full" data-analysis-id="${s(n.analysisId)}" data-facts-only="false">
${zn(n)}
${g("Thông tin sinh",Kn(n))}
${g("Tứ trụ / Bát Tự",Hn(n.pillars))}
${g("Nhật chủ · Thân · Cách cục",On(n))}
${g(H,Un(n))}
${g("Thập thần",Vn(n))}
${g("Dụng thần · Hỷ · Kỵ",Qn(n))}
${g("Thần sát",qn(n.shenSha))}
${g("Đại vận",Yn(n))}
${g("Phong thủy",Wn(n))}
${g("Điểm tổng",`<p class="bte-full-metric">${s(n.scoreLabel||"—")}</p>`)}
${Xn(n)}
${Jn(n)}
<footer class="bte-full-footer">Mã phân tích ${s(n.analysisId)}</footer>
</article></body></html>`}function wn(n,t,e){const r=R(e.ten_gods)??R(e.ten_gods_result),i=gn(r,t.key);return{key:t.key,label:t.label,stem:dn(o(n==null?void 0:n.stem),o(n==null?void 0:n.element))||o(n==null?void 0:n.stem),branch:o(n==null?void 0:n.branch),napAm:o(n==null?void 0:n.nap_am),hiddenStems:i.length?i.join(" · "):Array.isArray(n==null?void 0:n.hidden_stems)?n.hidden_stems.filter(Boolean).join(", "):o(n==null?void 0:n.hidden_stems),tenGod:o(n==null?void 0:n.ten_god),growthStage:o(n==null?void 0:n.truong_sinh)}}function Bn(n){const t=z(n)?(n==null?void 0:n.sections)??[]:[];return Pn.map(e=>{const r=t.find(c=>e.match.test(`${c.id??""} ${c.intent??""} ${c.title??""}`)),i=((r==null?void 0:r.paragraphs)??[]).map(c=>o(c.text)).filter(Boolean).join(`

`);return{id:e.id,title:e.title,body:i,present:!!i}})}function Rn(n){if(!z(n)||!n)return[];const t=An(n),e=[],r=Ln(t,"career_direction");return r&&e.push({id:"career",title:"Định hướng nghề nghiệp (hỗ trợ)",body:r}),e}function Dn(n,t,e){const r=o(n);if(r&&!F.test(r))return r;const i=o(t.analysis_id||t.request_id);return i&&!F.test(i)?i:["bte",e.year||0,e.month||0,e.day||0,e.hour||0,e.minute||0].map(String).join("-")}function Mn(n){return n&&typeof n=="object"?n:{}}function o(n,t=""){return n==null||n===""?t:String(n).trim()||t}function Fn(n,t){if(o(n))return o(n);const e=t.year,r=t.month,i=t.day;return e&&r&&i?`${A(Number(i))}/${A(Number(r))}/${e}`:""}function In(n){return n.hour==null?"":`${A(Number(n.hour))}:${A(Number(n.minute||0))}`}function A(n){return String(Number.isFinite(n)?n:0).padStart(2,"0")}function s(n){return String(n).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;")}function g(n,t){return`<section class="bte-full-section"><h2>${s(n)}</h2>${t}</section>`}function zn(n){return`<header class="bte-full-cover">
    <p class="bte-full-kicker">Báo cáo tư vấn Bát Tự</p>
    <h1>${s(n.customerName||"Khách hàng")}</h1>
    <p>${s([n.solarDate,n.lunarDate?`Âm lịch ${n.lunarDate}`:"",n.scoreLabel].filter(Boolean).join(" · "))}</p>
  </header>`}function Kn(n){return`<div class="bte-full-grid">
    ${a("Dương lịch",n.solarDate)}
    ${a("Âm lịch",n.lunarDate)}
    ${a("Giờ sinh",n.birthTime)}
    ${a("Giới tính",n.gender)}
    ${a("Nơi sinh",n.birthPlace)}
    ${a("Múi giờ",n.timezone)}
    ${a("Tam Nguyên",n.tamNguyen)}
    ${a("Cửu Vận",n.cuuVan)}
    ${a("Cung Phi",n.cungPhi)}
    ${a("Mệnh Quái",n.menhQuai)}
    ${a("Hành Cung",n.hanhCung)}
    ${a("Nhóm Trạch",n.nhomTrach)}
  </div>`}function On(n){const t=[n.climateState,n.balancingNeed,n.climatePreference].filter(Boolean).join(" · ");return`<div class="bte-full-grid">
    ${a("Nhật chủ",[n.dayMaster,n.yinYang,n.dayMasterElement].filter(Boolean).join(" · "))}
    ${a("Thân",n.strengthLabel)}
    ${a("Điểm thân",n.strengthScore)}
    ${n.strengthEvidence?a("Yếu tố chính",n.strengthEvidence):""}
    ${a("Cách cục",n.pattern)}
    ${n.patternEvidence?`<p class="bte-full-note">${s(n.patternEvidence)}</p>`:""}
    ${a("Điều hậu",t)}
    ${n.climateEvidence?`<p class="bte-full-note">${s(n.climateEvidence)}</p>`:""}
  </div>`}function Hn(n){const t=n.map(r=>`<th>${s(r.label)}</th>`).join(""),e=(r,i)=>`<tr><th scope="row">${s(r)}</th>${n.map(c=>`<td>${s(i(c)||"—")}</td>`).join("")}</tr>`;return`<div class="bte-full-table-wrap"><table class="bte-full-table">
    <thead><tr><th></th>${t}</tr></thead>
    <tbody>
      ${e("Thiên can",r=>r.stem)}
      ${e("Địa chi",r=>r.branch)}
      ${e("Nạp âm",r=>r.napAm)}
      ${e("Tàng can",r=>r.hiddenStems)}
      ${e("Thập thần",r=>r.tenGod)}
      ${e("Trường sinh",r=>r.growthStage)}
    </tbody>
  </table></div>`}function Un(n){const t=n.fiveElements.reduce((r,i)=>r+i.count,0);return`${`<ul class="bte-full-elements">${n.fiveElements.map(r=>`<li><span>${s(r.name)}</span><strong>${r.count}</strong></li>`).join("")}</ul>`}<p class="bte-full-note">${s(fn(t))}</p>`}function Vn(n){const t=n.tenGodsFeatured.map(i=>`<li><strong>${s(i.name)} — ${s(i.klass)}</strong><p class="bte-full-note">${s(i.evidence)}</p></li>`).join(""),e=n.tenGods.join(" · "),r=n.hiddenTenGods.join(" · ");return!t&&!e&&!r?'<p class="bte-full-empty">Chưa có thập thần hiển thị.</p>':`<div>
    ${t?`<p><strong>Thập thần nổi bật</strong></p><ul>${t}</ul>`:""}
    ${n.tenGodsOthersLine?`<p class="bte-full-note">${s(n.tenGodsOthersLine)}</p>`:""}
    <p><strong>Lộ can</strong> ${s(e||"—")}</p>
    <p><strong>Tàng can</strong> ${s(r||"—")}</p>
  </div>`}function Qn(n){const t=n.usefulGodReason?`<p class="bte-full-reason"><strong>Căn cứ chọn Dụng:</strong> ${s(n.usefulGodReason)}</p>`:"";return`<div class="bte-full-gods">
    <div class="bte-full-grid">
      ${a("Dụng thần",n.usefulGod)}
      ${a("Hỷ thần",n.hyThan)}
      ${a("Kỵ thần",n.kyThan)}
    </div>
    ${t}
  </div>`}function qn(n){return n.length?`<ul>${n.map(t=>{const e=t.evidence?` · ${t.evidence}`:"",r=t.presence?` — ${t.presence}`:"";return`<li><strong>${s(t.name)}</strong>${s(r)}${s(e)}</li>`}).join("")}</ul>`:'<p class="bte-full-empty">Chưa có thần sát trên lá số này.</p>'}function Yn(n){const t=`<p>Đại vận hiện tại: <strong>${s(n.luckCurrent||"—")}</strong>. Chiều vận: <strong>${s(n.luckDirection||"—")}</strong>. Tuổi khởi vận: <strong>${s(n.luckStartAge||"—")}</strong>.</p>
<p>Căn cứ: ${s(n.luckEvidence||"—")}. ${s(n.luckMethod||"")}</p>`;return n.luckCycles.length?`${t}<ol class="bte-full-luck">${n.luckCycles.map(e=>{const r=e.elements?` (${s(e.elements)})`:"";return`<li${e.current?' data-current="true"':""}>${s(e.label)} ${s(e.years)}${r}${e.current?" (hiện tại)":""}</li>`}).join("")}</ol>`:t}function Wn(n){return`<div class="bte-full-grid">
    ${a("Tam Nguyên",n.tamNguyen)}
    ${a("Cửu Vận",n.cuuVan)}
    ${a("Cung Phi",n.cungPhi)}
    ${a("Mệnh Quái",n.menhQuai)}
    ${a("Hành Cung",n.hanhCung)}
    ${a("Nhóm Trạch",n.nhomTrach)}
  </div>`}function Xn(n){return`<section class="bte-full-narrative" data-narrative="pack05">
    <h2>Luận giải</h2>
    ${n.narrative.map(t=>`<section class="bte-full-narrative__section" data-narrative-id="${s(t.id)}">
            <h3>${s(t.title)}</h3>
            <p>${s(t.body||"—")}</p>
          </section>`).join("")}
  </section>`}function Jn(n){return n.supporting.length?n.supporting.map(t=>g(t.title,`<p>${s(t.body)}</p>`)).join(""):""}function a(n,t){return`<div class="bte-full-kv"><span>${s(n)}</span><strong>${s(t||"—")}</strong></div>`}function Zn(){return`<style>
    body{font-family:"Segoe UI",system-ui,sans-serif;color:#1c2430;margin:0;background:#f7f5f2;}
    .bte-full-report{max-width:960px;margin:0 auto;padding:32px 24px 64px;}
    .bte-full-cover{margin-bottom:28px;}
    .bte-full-kicker{letter-spacing:.08em;text-transform:uppercase;font-size:12px;opacity:.7;}
    h1{font-size:28px;margin:4px 0 8px;}
    h2{font-size:18px;margin:0 0 12px;}
    h3{font-size:16px;margin:0 0 8px;}
    .bte-full-section,.bte-full-narrative{background:#fff;border:1px solid #d7e0ea;border-radius:14px;padding:16px 18px;margin:0 0 14px;}
    .bte-full-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;}
    .bte-full-reason{margin:10px 0 0;line-height:1.5;font-size:14px;}
    .bte-full-kv{background:#f4f7f7;border-radius:10px;padding:10px 12px;}
    .bte-full-kv span{display:block;font-size:12px;opacity:.7;margin-bottom:4px;}
    .bte-full-table{width:100%;border-collapse:collapse;font-size:14px;}
    .bte-full-table th,.bte-full-table td{border:1px solid #d7e0ea;padding:8px;text-align:center;}
    .bte-full-table th[scope=row]{text-align:left;background:#f4f7f7;}
    .bte-full-elements{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;list-style:none;padding:0;margin:0;}
    .bte-full-elements li{background:#f4f7f7;border-radius:10px;padding:10px;text-align:center;}
    .bte-full-luck{columns:2;padding-left:18px;}
    .bte-full-luck li[data-current="true"]{font-weight:700;}
    .bte-full-narrative__section{margin:0 0 16px;}
    .bte-full-footer{margin-top:24px;font-size:12px;opacity:.65;}
    .bte-full-empty,.bte-full-metric{margin:0;}
    @media print{
      body{background:#fff;}
      .bte-full-cover,.bte-full-section,.bte-full-narrative{break-inside:avoid;page-break-inside:avoid;}
      .bte-full-narrative{page-break-before:always;}
    }
  </style>`}export{T as U,Gn as a,ft as b,N as c,vn as d,tt as e,ct as f,kn as g,z as h,lt as i,Tn as j,An as k,st as l,ot as m,at as n,Ln as o,rt as p,I as q,gt as r,ut as s,it as t,ht as u,et as v,Cn as w,_n as x,Nn as y};
//# sourceMappingURL=fullReportViewModel-DRKahvt4.js.map
