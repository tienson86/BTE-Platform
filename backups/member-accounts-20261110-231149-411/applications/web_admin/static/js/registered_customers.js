(function () {
  const rows=document.getElementById("registeredRows"), state=document.getElementById("registeredState");
  if(!rows)return;
  const dialog=document.getElementById("registeredDialog"), form=document.getElementById("registeredCustomerForm"), notice=document.getElementById("registeredDialogState");
  let editing=null, busy=false;
  function node(tag,text){const element=document.createElement(tag);if(text!==undefined)element.textContent=text;return element;}
  function usage(items){
    const target=document.getElementById("registeredUsage"); target.replaceChildren();
    if(!items?.length)return;
    const table=node("table"),head=node("tr");
    ["Chức năng","Hạn mức","Đã dùng","Đang xử lý","Còn lại"].forEach(text=>head.append(node("th",text)));table.append(head);
    items.forEach(item=>{const row=node("tr");[item.label,item.limit??"Không giới hạn",item.used,item.pending,item.remaining??"Không giới hạn"].forEach(text=>row.append(node("td",text)));table.append(row);});target.append(table);
  }
  function open(user){
    editing=user||null; const fields=form.elements; notice.textContent="";
    fields.username.value=user?.username||""; fields.username.disabled=!!user;
    fields.display_name.value=user?.display_name||""; fields.phone.value=user?.phone||"";
    fields.phone.required=!user; fields.password.value=""; fields.password.required=!user;
    fields.analysis_limit.value=user ? user.analysis_limit??"" : 31;
    fields.is_active.checked=user?.is_active??true;
    usage(user?.usage);document.getElementById("registeredRelease").hidden=!user?.usage?.some(item=>item.pending>0);
    document.getElementById("registeredDialogTitle").textContent=user ? "Khách hàng: "+user.username : "Tạo khách hàng";
    dialog.showModal();
  }
  async function load(){
    state.textContent="Đang tải khách hàng…";
    try{
      const data=await BteAdmin.get("/api/v1/admin/registered-customers?q="+encodeURIComponent(document.getElementById("registeredQuery").value.trim()));
      rows.replaceChildren();
      data.items.forEach(user=>{
        const row=node("tr");row.append(node("td",user.display_name),node("td",user.username));
        const phone=node("td");if(user.phone){const link=node("a",user.phone);link.href="tel:"+user.phone;phone.append(link);}else phone.textContent="Chưa bổ sung";row.append(phone);
        const labels={pending:"Chờ xác nhận",active:user.member_access?"Còn hiệu lực":"Đã hết hạn",rejected:"Chưa chấp thuận",existing:"Đã cấp quyền trước đây"};
        row.append(node("td",user.is_active?labels[user.membership_status]||user.membership_status:"Đã khóa"),node("td",user.analysis_limit??"Không giới hạn"));
        const action=node("td"),button=node("button","Xem / Điều chỉnh");button.type="button";button.onclick=()=>open(user);action.append(button);row.append(action);rows.append(row);
      });state.textContent=data.items.length+" tài khoản khách hàng.";
    }catch(error){state.textContent=error.message;}
  }
  form.addEventListener("submit",async event=>{
    event.preventDefault();if(busy||!form.reportValidity())return;
    const fields=form.elements, limit=fields.analysis_limit.value;
    const payload={display_name:fields.display_name.value.trim(),phone:fields.phone.value.trim(),analysis_limit:limit===""?null:Number(limit),is_active:fields.is_active.checked};
    if(fields.password.value)payload.password=fields.password.value;
    busy=true;form.querySelector('button[type="submit"]').disabled=true;
    try{
      if(editing)await BteAdmin.api("PATCH","/api/v1/admin/registered-customers/"+encodeURIComponent(editing.username),payload);
      else {delete payload.is_active;payload.username=fields.username.value.trim();await BteAdmin.post("/api/v1/users",payload);}
      dialog.close();await load();state.textContent="Đã lưu thông tin và hạn mức khách hàng.";
    }catch(error){notice.textContent=error.message;}
    finally{busy=false;form.querySelector('button[type="submit"]').disabled=false;}
  });
  document.getElementById("registeredRelease").onclick=async()=>{
    if(!editing)return;
    try{const result=await BteAdmin.post("/api/v1/admin/registered-customers/"+encodeURIComponent(editing.username)+"/release-pending",{});notice.textContent="Đã giải phóng "+result.released+" lượt chờ quá 30 phút.";await load();}catch(error){notice.textContent=error.message;}
  };
  document.getElementById("registeredClose").onclick=()=>dialog.close();
  document.getElementById("registeredCreate").onclick=()=>open(null);
  document.getElementById("registeredSearch").onclick=load;
  document.getElementById("registeredQuery").onkeydown=event=>{if(event.key==="Enter"){event.preventDefault();void load();}};
  void load();
})();
