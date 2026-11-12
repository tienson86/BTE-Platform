(function () {
  const rows=document.getElementById("registeredRows"), state=document.getElementById("registeredState");
  if(!rows)return;
  const dialog=document.getElementById("registeredDialog"), form=document.getElementById("registeredCustomerForm"), notice=document.getElementById("registeredDialogState");
  let editing=null, busy=false, granting=null, acting=null, tiers=[];
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
      const data=await BteAdmin.get("/api/v1/admin/registered-customers?q="+encodeURIComponent(document.getElementById("registeredQuery").value.trim())+'&deleted='+(document.getElementById('registeredScope').value==='deleted'));
      rows.replaceChildren();
      const tier=document.getElementById('registeredTier').value;
      const items=data.items.filter(u=>!tier||(tier==='none'?!u.member_tier:String(u.member_tier)===tier));
      items.forEach(user=>{
        const row=node("tr");row.append(node("td",user.display_name),node("td",user.username));
        const phone=node("td");if(user.phone){const link=node("a",user.phone);link.href="tel:"+user.phone;phone.append(link);}else phone.textContent="Chưa bổ sung";row.append(phone);
        const labels={pending:"Chờ xác nhận",active:user.member_access?"Còn hiệu lực":"Đã hết hạn",rejected:"Chưa chấp thuận",existing:"Đã cấp quyền trước đây"};
        row.append(node('td',(user.member_tier?'Cấp '+user.member_tier:'Chưa phân cấp')+(user.membership_source==='manual'?' • Cấp thủ công':'')));
        row.append(node("td",user.deleted_at?'Đã xóa':user.is_active?labels[user.membership_status]||user.membership_status:"Đã khóa"));
        row.append(node('td',user.membership_expires_at?new Date(user.membership_expires_at).toLocaleString('vi-VN'):'—'));
        const limits=(user.usage||[]).filter(u=>u.enabled).map(u=>u.limit);const different=new Set(limits).size>1;
        row.append(node('td',different?'Theo từng chức năng':user.analysis_limit??'Không giới hạn'));
        const action=node("td"); action.className='toolbar';
        function button(text,click,cls){const b=node('button',text);b.type='button';if(cls)b.className=cls;b.onclick=click;action.append(b);}
        if(user.deleted_at)button('Khôi phục',()=>showAction(user,'restore'),'secondary');
        else {button('Xem / Điều chỉnh',()=>open(user));button('Cấp thành viên',()=>showGrant(user),'secondary');button(user.is_active?'Khóa':'Mở khóa',()=>showAction(user,user.is_active?'lock':'unlock'),'secondary');button('Xóa',()=>showAction(user,'delete'),'danger');}
        row.append(action);rows.append(row);
      });state.textContent=items.length+" tài khoản thành viên.";
    }catch(error){state.textContent=error.message;}
  }
  form.addEventListener("submit",async event=>{
    event.preventDefault();if(busy||!form.reportValidity())return;
    const fields=form.elements, limit=fields.analysis_limit.value;
    const payload={display_name:fields.display_name.value.trim(),phone:fields.phone.value.trim(),is_active:fields.is_active.checked};
    const quota=limit===""?null:Number(limit);
    if(!editing||quota!==editing.analysis_limit)payload.analysis_limit=quota;
    if(editing)payload.expected_revision=editing.account_revision;
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
  document.getElementById('registeredTier').onchange=load;
  document.getElementById('registeredScope').onchange=load;
  const grantDialog=document.getElementById('memberGrantDialog'),grantForm=document.getElementById('memberGrantForm'),grantState=document.getElementById('memberGrantState');
  function grantBenefits(){const tier=tiers.find(t=>t.tier===Number(grantForm.elements.tier.value));if(!tier)return;grantForm.elements.validity_days.value=tier.validity_days??'';document.getElementById('memberGrantBenefits').textContent=tier.title+' — '+Object.entries(tier.feature_limits).map(([key,value])=>({bazi:'Lá số',date_selection:'Ngày tốt',marriage:'Hôn nhân',childbirth:'Sinh con',naming:'Đặt tên',business:'Hợp tác',van_han:'Vận hạn'}[key]||key)+': '+(tier.enabled_features.includes(key)?value??'Không giới hạn':'Tắt')).join(' · ');}
  async function showGrant(user){
    granting=user;grantState.textContent='';grantForm.reset();document.getElementById('memberGrantTarget').textContent=user.display_name+' (@'+user.username+')';
    try{const plan=await BteAdmin.get('/api/v1/membership/admin/settings');tiers=plan.tiers||[];grantForm.elements.tier.value=String(user.member_tier||1);grantBenefits();grantDialog.showModal();}
    catch(error){state.textContent=error.message;}
  }
  grantForm.elements.tier.onchange=grantBenefits;
  grantForm.onsubmit=async event=>{event.preventDefault();if(busy||!granting||!grantForm.reportValidity())return;busy=true;const submit=grantForm.querySelector('[type="submit"]');submit.disabled=true;
    try{await BteAdmin.post('/api/v1/users/'+encodeURIComponent(granting.username)+'/membership-grant',{tier:Number(grantForm.elements.tier.value),validity_days:Number(grantForm.elements.validity_days.value),note:grantForm.elements.note.value.trim(),expected_revision:granting.account_revision});grantDialog.close();await load();state.textContent='Đã cấp thành viên. Giữ nguyên lượt đã dùng và số dư; không phát sinh thanh toán hoặc thưởng giới thiệu.';}
    catch(error){grantState.textContent=error.message;}finally{busy=false;submit.disabled=false;}
  };
  document.getElementById('memberGrantClose').onclick=()=>{if(!busy)grantDialog.close();};
  const actionDialog=document.getElementById('memberActionDialog'),actionForm=document.getElementById('memberActionForm'),actionState=document.getElementById('memberActionState');
  function showAction(user,action){acting={user,action};actionForm.reset();actionState.textContent='';const labels={lock:'Khóa tài khoản',unlock:'Mở khóa tài khoản',delete:'Xóa tài khoản',restore:'Khôi phục tài khoản'};document.getElementById('memberActionTitle').textContent=labels[action]+' @'+user.username;
    document.getElementById('memberActionDescription').textContent=action==='delete'?'Tài khoản sẽ bị chặn đăng nhập và chuyển vào danh sách đã xóa. Giữ hồ sơ, số dư và quyền khóa học để có thể khôi phục.':action==='restore'?'Khôi phục vào danh sách hiện tại ở trạng thái khóa. Admin có thể mở khóa sau khi kiểm tra.':'Thay đổi quyền đăng nhập, giữ nguyên cấp thành viên, ngày hết hạn và dữ liệu.';
    document.getElementById('memberDeleteConfirmLabel').hidden=action!=='delete';actionForm.elements.confirm_username.required=action==='delete';actionDialog.showModal();}
  actionForm.onsubmit=async event=>{event.preventDefault();if(busy||!acting||!actionForm.reportValidity())return;if(acting.action==='delete'&&actionForm.elements.confirm_username.value!==acting.user.username){actionState.textContent='Tên đăng nhập xác nhận chưa khớp.';return;}
    busy=true;const submit=actionForm.querySelector('[type="submit"]');submit.disabled=true;
    try{await BteAdmin.post('/api/v1/users/'+encodeURIComponent(acting.user.username)+'/account-action/'+acting.action,{expected_revision:acting.user.account_revision,note:actionForm.elements.note.value.trim()});actionDialog.close();await load();state.textContent='Đã cập nhật trạng thái tài khoản.';}
    catch(error){actionState.textContent=error.message;}finally{busy=false;submit.disabled=false;}
  };
  [grantDialog,actionDialog].forEach(d=>d.addEventListener('cancel',e=>{if(busy)e.preventDefault();}));
  document.getElementById('memberActionClose').onclick=()=>{if(!busy)actionDialog.close();};
  void load();
})();
