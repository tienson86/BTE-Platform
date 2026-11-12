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
  const byId = id => document.getElementById(id);
  const date = value => value ? new Date(value).toLocaleString('vi-VN', {timeZone:'Asia/Ho_Chi_Minh'}) : '—';
  const money = value => value == null ? '—' : Number(value).toLocaleString('vi-VN') + ' đ';
  const membershipStatus = {pending:'Chờ xác nhận',active:'Đã xác nhận',rejected:'Chưa chấp thuận',refunded:'Đã hoàn tiền',existing:'Đã cấp quyền trước đây'};
  const previous = byId('registeredPrevious'), next = byId('registeredNext');
  let directoryPage = 1, listRequest = 0;
  async function load(page = directoryPage){
    const request = ++listRequest;
    state.textContent="Đang tải thành viên…";
    previous.disabled = next.disabled = true;
    const params = new URLSearchParams({
      q: byId('registeredQuery').value.trim(), deleted: byId('registeredScope').value === 'deleted',
      tier: byId('registeredTier').value, status: byId('registeredStatus').value,
      expiring: byId('registeredExpiring').checked, pending: byId('registeredPending').checked, page,
    });
    try{
      const data = await BteAdmin.get('/api/v1/admin/registered-customers?' + params);
      if (request !== listRequest) return;
      rows.replaceChildren();
      directoryPage = data.page;
      const items = data.items;
      items.forEach(user=>{
        const row=node("tr");row.append(node("td",user.display_name),node("td",user.username));
        const phone=node("td");if(user.phone){const link=node("a",user.phone);link.href="tel:"+user.phone;phone.append(link);}else phone.textContent="Chưa bổ sung";row.append(phone);
        const labels={pending:"Chờ xác nhận",active:user.member_access?"Còn hiệu lực":"Đã hết hạn",rejected:"Chưa chấp thuận",refunded:"Đã hoàn tiền",existing:"Đã cấp quyền trước đây"};
        row.append(node('td',(user.member_tier?'Cấp '+user.member_tier:'Chưa phân cấp')+(user.source_label && user.source_label!=='—'?' • '+user.source_label:'')));
        row.append(node("td",user.deleted_at?'Đã xóa':user.is_active?labels[user.membership_status]||user.membership_status:"Đã khóa"));
        row.append(node('td',user.membership_expires_at?new Date(user.membership_expires_at).toLocaleString('vi-VN'):'—'));
        row.append(node('td',date(user.last_activity)));
        const action=node("td"); action.className='toolbar';
        function button(text,click,cls){const b=node('button',text);b.type='button';if(cls)b.className=cls;b.onclick=click;action.append(b);}
        button('Xem hồ sơ', () => openHistory(user));
        if(user.deleted_at)button('Khôi phục',()=>showAction(user,'restore'),'secondary');
        else {button('Điều chỉnh',()=>openEdit(user),'secondary');button('Cấp thành viên',()=>showGrant(user),'secondary');button(user.is_active?'Khóa':'Mở khóa',()=>showAction(user,user.is_active?'lock':'unlock'),'secondary');button('Xóa',()=>showAction(user,'delete'),'danger');}
        row.append(action);rows.append(row);
      });
      const pages = Math.max(1, Math.ceil(data.total / data.page_size));
      previous.disabled = directoryPage <= 1;
      next.disabled = directoryPage >= pages;
      state.textContent = data.total ? data.total + ' thành viên · Trang ' + directoryPage + '/' + pages : 'Không tìm thấy thành viên.';

    }catch(error){if (request === listRequest) state.textContent=error.message;}
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
  const refresh = () => load(1);
  byId('registeredSearch').onclick = refresh;
  byId('registeredQuery').onkeydown = event => {
    if (event.key === 'Enter') { event.preventDefault(); void refresh(); }
  };
  for (const id of ['registeredTier','registeredScope','registeredStatus','registeredExpiring','registeredPending']) {
    byId(id).onchange = refresh;
  }
  previous.onclick = () => load(directoryPage - 1);
  next.onclick = () => load(directoryPage + 1);

  function profilePath(user) {
    return '/api/v1/admin/registered-customers/' + encodeURIComponent(user.user_id);
  }
  async function openEdit(user) {
    try {
      const data = await BteAdmin.get(profilePath(user) + '/usage');
      open({...user, usage:data.items});
    } catch (error) { state.textContent = error.message; }
  }

  const history = byId('memberHistoryDialog');
  const section = byId('memberHistorySection');
  const historyRows = byId('memberHistoryRows'), historyState = byId('memberHistoryState');
  const historyPrevious = byId('memberHistoryPrevious'), historyNext = byId('memberHistoryNext');
  let historyUser, historyPage = 1, historyRequest = 0;
  const columns = {
    membership: ['Gói / Cấp','Hình thức','Trạng thái','Tiền đã xác nhận','Ngày ghi nhận','Hết hạn','Ngày hoàn tiền','Mã giao dịch','Ghi chú duyệt'],
    usage: ['Dịch vụ','Thời gian','Mã hồ sơ'],
    orders: ['Loại','Nội dung','Trạng thái','Số lượng','Tổng tại lúc gửi','Linh Thạch đã cộng','Ngày gửi'],
    learning: ['Khóa Online','Đã đánh dấu hoàn thành','Linh Thạch đã dùng','Mở lúc','Hết hạn'],
    wallet: ['Thời gian','Biến động','Lý do'],
  };
  function historyValues(key, item) {
    switch (key) {
      case 'membership': return [item.title || (item.tier ? 'Cấp ' + item.tier : '—'), item.source, item.source === 'Cấp thủ công' && item.status === 'active' ? 'Đã cấp' : (membershipStatus[item.status] || item.status), money(item.confirmed_amount), date(item.at), date(item.expires_at), date(item.refunded_at), item.reference, item.note];
      case 'usage': {
        const link = node('a', item.id);
        const query = new URLSearchParams({owner:'user:' + historyUser.user_id, kind:item.kind, q:item.id});
        link.href = 'cases?' + query;
        return [item.label, date(item.created_at), link];
      }
      case 'orders': return [item.kind === 'shop' ? 'Vật phẩm' : 'Khóa Offline', item.title, {pending:'Chờ xử lý',confirmed:'Đã xác nhận mua',cancelled:'Đã hủy'}[item.status], item.quantity, money(item.total), item.reward_granted, date(item.created_at)];
      case 'learning': return [item.title, item.completed + '/' + item.lesson_count, item.price ?? '—', date(item.started_at), item.started_at ? (item.expires_at ? date(item.expires_at) : 'Không hết hạn') : 'Học thử'];
      case 'wallet': return [date(item.created_at), item.delta > 0 ? '+' + item.delta : item.delta, item.description];
    }
  }
  function historyTable(headers, values) {
    const table = node('table'), head = node('thead'), header = node('tr'), body = node('tbody');
    headers.forEach(value => header.append(node('th', value)));
    head.append(header);
    for (const valuesRow of values) {
      const row = node('tr');
      valuesRow.forEach(value => {
        const cell = node('td');
        if (value instanceof HTMLElement) cell.append(value);
        else cell.textContent = value ?? '—';
        row.append(cell);
      });
      body.append(row);
    }
    table.append(head, body);
    return table;
  }
  async function loadHistory(page) {
    const request = ++historyRequest, key = section.value;
    historyPrevious.disabled = historyNext.disabled = true;
    historyState.textContent = 'Đang tải hồ sơ…';
    historyRows.replaceChildren();
    try {
      const data = await BteAdmin.get(profilePath(historyUser) + '/history?' + new URLSearchParams({section:key,page}));
      if (request !== historyRequest || !history.open) return;
      historyPage = data.page;
      if (data.usage) historyRows.append(historyTable(['Chức năng','Đã dùng','Đang xử lý','Còn lại'], data.usage.map(row => [
        row.label,row.used,row.pending,row.enabled ? (row.remaining ?? 'Không giới hạn') : 'Tắt',
      ])));
      if (data.items.length) historyRows.append(historyTable(columns[key],data.items.map(item=>historyValues(key,item))));
      else historyRows.append(node('p','Chưa có dữ liệu đã lưu.'));
      historyState.textContent = key === 'wallet' ? 'Số dư: ' + data.balance + ' Linh Thạch · Trang ' + historyPage : 'Trang ' + historyPage;
      historyPrevious.disabled = historyPage <= 1;
      historyNext.disabled = !data.has_next;
    } catch (error) {
      if (request === historyRequest) historyState.textContent = error.message;
    }
  }
  function openHistory(user) {
    historyUser = user;
    byId('memberHistoryTitle').textContent = 'Hồ sơ ' + user.display_name + ' (@' + user.username + ')';
    section.value = 'membership';
    history.showModal();
    void loadHistory(1);
  }
  section.onchange = () => loadHistory(1);
  historyPrevious.onclick = () => loadHistory(historyPage - 1);
  historyNext.onclick = () => loadHistory(historyPage + 1);
  byId('memberHistoryClose').onclick = () => history.close();

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
