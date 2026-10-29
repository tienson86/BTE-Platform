(function () {
  const api = window.BteAdmin || window.BtePortal;
  const labels = {bazi:'Bát Tự', marriage:'Hôn nhân', business:'Hợp tác', childbirth:'Sinh con', van_han:'Tính vận hạn', naming:'Đặt tên',date_selection:'Chọn ngày',contact:'Liên hệ hỗ trợ',legacy_case:'Hồ sơ nhập trước đây'};
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const when = s => s ? new Date(s).toLocaleString('vi-VN') : '—';
  const list = document.getElementById('historyList');
  const summary = document.getElementById('historySummary');
  let page = 1, data = null, requestSequence = 0;
  function endpoint(item) {
    const id = encodeURIComponent(item.id);
    if (item.kind === 'bazi') return '/api/v1/export/';
    if (item.kind === 'van_han') return '/api/v1/van-han/'+id;
    if (item.kind === 'childbirth') return '/api/v1/consulting/childbirth/'+id;
    return '/api/v1/consulting/marriage/' + (item.kind === 'business' ? 'business/' : '') + id;
  }
  async function download(item, format) {
    if (format==='json') {
      const result=await api.get('/api/v1/admin-archive/'+item.kind+'/'+encodeURIComponent(item.id)+'?owner='+encodeURIComponent(item.owner));
      const link=document.createElement('a');link.href=URL.createObjectURL(new Blob([JSON.stringify(result.row,null,2)],{type:'application/json'}));link.download='BTE_'+item.id+'.json';link.click();setTimeout(()=>URL.revokeObjectURL(link.href),1000);return;
    }
    const path = endpoint(item);
    const options = {headers:{Authorization:'Bearer '+api.getToken()}};
    let url;
    if (item.kind === 'bazi') {
      url = '/backend'+path+format;
      Object.assign(options, {method:'POST', body:JSON.stringify({analysis_id:item.id, source:'history', admin_owner:item.owner})});
      options.headers['Content-Type']='application/json';
    } else url = '/backend'+path+'/export/'+format;
    const response = await fetch(url, options);
    if (!response.ok) throw new Error('Chưa tải được tài liệu ('+response.status+').');
    const blob = await response.blob();
    const disposition = response.headers.get('Content-Disposition') || '';
    const utf8 = disposition.match(/filename\*=UTF-8''([^;]+)/i);
    const plain = disposition.match(/filename="?([^";]+)/i);
    let name = 'BTE_'+item.id+'.'+format;
    try { if (utf8) name=decodeURIComponent(utf8[1].replace(/^"|"$/g,'')); else if (plain) name=plain[1]; } catch (_) {}
    const link = document.createElement('a');
    link.href=URL.createObjectURL(blob); link.download=name; document.body.appendChild(link);link.click();link.remove();
    setTimeout(()=>URL.revokeObjectURL(link.href),1000);
  }
  function renderReport(node, target, depth) {
    if (!node || depth>18) return;
    if (Array.isArray(node)) {node.forEach(value=>renderReport(value,target,depth+1));return;}
    if (typeof node !== 'object') return;
    if (node.title && typeof node.title === 'string') {const h=document.createElement('h3');h.textContent=node.title;target.appendChild(h);}
    if (node.full_name && typeof node.full_name === 'string') {const h=document.createElement('h3');h.textContent=node.full_name;target.appendChild(h);}
    ['body','text','headline','description','answer','meaning','guidance','quick_guidance'].forEach(key=>{
      if (typeof node[key] === 'string' && node[key]) {const p=document.createElement('p');p.textContent=node[key];p.style.whiteSpace='pre-wrap';target.appendChild(p);}
    });
    Object.keys(node).forEach(key=>{if(typeof node[key]==='object')renderReport(node[key],target,depth+1);});
  }
  async function open(item) {
    if (window.BteAdmin || ['naming','date_selection','contact','legacy_case'].includes(item.kind)) {
      const result=await api.get('/api/v1/admin-archive/'+item.kind+'/'+encodeURIComponent(item.id)+'?owner='+encodeURIComponent(item.owner));
      const row=result.row, dialog=document.createElement('dialog');dialog.className='customer-dialog';
      const close=document.createElement('button');close.textContent='Đóng';close.onclick=()=>{dialog.close();dialog.remove();};dialog.append(close);
      const heading=document.createElement('h2');heading.textContent=labels[item.kind]+' — '+item.customer_name;dialog.append(heading);
      const actor=document.createElement('p');actor.textContent='Người tạo: '+item.creator_username+' · '+when(item.created_at);dialog.append(actor);
      if(item.kind==='contact') {
        const contact=row.contact||{};
        [contact.full_name,contact.phone,contact.subject,contact.message].forEach(text=>{const p=document.createElement('p');p.textContent=text||'';p.style.whiteSpace='pre-wrap';dialog.append(p);});
        const form=document.createElement('form'), select=document.createElement('select'), note=document.createElement('textarea'),button=document.createElement('button'),status=document.createElement('p');
        const stateLabel=document.createElement('label');stateLabel.textContent='Trạng thái xử lý';
        [['open','Mới tiếp nhận'],['handling','Đang hỗ trợ'],['resolved','Đã xử lý']].forEach(([value,text])=>{const option=document.createElement('option');option.value=value;option.textContent=text;select.append(option);});
        select.value=row.status||'open';stateLabel.append(select);
        const noteLabel=document.createElement('label');noteLabel.textContent='Ghi chú hỗ trợ';noteLabel.append(note);note.maxLength=3000;note.value=row.admin_note||'';
        button.type='submit';button.textContent='Lưu kết quả hỗ trợ';form.append(stateLabel,noteLabel,button,status);dialog.append(form);
        form.onsubmit=async event=>{event.preventDefault();button.disabled=true;try{await api.api('PATCH','/api/v1/admin/contacts/'+encodeURIComponent(item.id),{status:select.value,admin_note:note.value});status.textContent='Đã lưu thông tin xử lý.';}catch(error){status.textContent=error.message;}finally{button.disabled=false;}};
      } else {
        const content=document.createElement('div');renderReport(row.result||row.data||row,content,0);dialog.append(content);
        if(item.kind==='bazi' && (!window.BteAdmin || BteAdmin.portalSession)){const link=document.createElement('a');link.href='/result?from=history&id='+encodeURIComponent(item.id)+'&admin_owner='+encodeURIComponent(item.owner);link.textContent='Mở giao diện lá số đầy đủ';dialog.append(link);}
      }
      const detail=document.createElement('details'),label=document.createElement('summary'),raw=document.createElement('pre');label.textContent='Dữ liệu hồ sơ đã lưu';raw.textContent=JSON.stringify(row,null,2);raw.style.whiteSpace='pre-wrap';raw.style.overflowWrap='anywhere';detail.append(label,raw);dialog.append(detail);document.body.append(dialog);dialog.showModal();return;
    }
    if (item.kind==='van_han') {location.href='/tinh-van-han?id='+encodeURIComponent(item.id);return;}
    if (item.kind==='bazi') {
      location.href='/result?from=history&id='+encodeURIComponent(item.id)+'&admin_owner='+encodeURIComponent(item.owner);return;
    }
    if (item.kind==='childbirth') {location.href='/childbirth-consulting?archive_id='+encodeURIComponent(item.id);return;}
    const response = await api.get(endpoint(item) + (item.kind==='childbirth' ? '' : '/report'));
    if (response.status==='FAILED') throw new Error('Chưa mở được hồ sơ tư vấn.');
    const dialog=document.createElement('dialog');dialog.style.cssText='width:min(900px,92vw);max-height:85vh;overflow:auto;padding:24px;border:1px solid #ccc;border-radius:12px';
    const close=document.createElement('button');close.textContent='Đóng';close.onclick=()=>{dialog.close();dialog.remove();};dialog.appendChild(close);
    const h=document.createElement('h2');h.textContent=labels[item.kind]+' — '+item.customer_name;dialog.appendChild(h);
    const attribution=document.createElement('p');attribution.textContent='Người tạo: '+(item.creator_display_name ? item.creator_display_name+' · ' : '')+item.creator_username;dialog.appendChild(attribution);
    const content=document.createElement('div');renderReport(response.data || response,content,0);dialog.appendChild(content);
    if(!content.childNodes.length){const p=document.createElement('p');p.textContent='Hồ sơ đã lưu. Bạn có thể tải PDF hoặc DOCX để xem toàn bộ nội dung.';content.appendChild(p);}
    document.body.appendChild(dialog);dialog.showModal();
  }
  async function load() {
    const sequence=++requestSequence;
    const params=new URLSearchParams({page:String(page),limit:'50',kind:document.getElementById('aaKind').value,username:document.getElementById('aaUser').value,q:document.getElementById('aaSearch').value});
    summary.textContent='Đang đọc kho hồ sơ trên máy chủ…';
    try {
      const response=await api.get('/api/v1/admin-archive?'+params);
      if(sequence!==requestSequence)return;
      data=response;
      const user=document.getElementById('aaUser'), selected=user.value;
      user.innerHTML='<option value="">Mọi tài khoản</option>'+data.users.map(v=>'<option>'+esc(v)+'</option>').join('');user.value=selected;
      summary.textContent=data.total+' hồ sơ phù hợp · '+Object.keys(labels).map(k=>labels[k]+': '+(data.counts[k]||0)).join(' · ');
      const rows=data.items.map((item,i)=>'<tr><td>'+((page-1)*50+i+1)+'</td><td>'+esc(labels[item.kind]||item.kind)+'</td><td>'+esc(item.customer_name)+(item.phone?'<br>'+esc(item.phone):'')+'</td><td>'+esc(when(item.created_at))+'</td><td>'+esc(item.creator_display_name||'—')+'<br><strong>'+esc(item.creator_username)+'</strong></td><td style="overflow-wrap:anywhere">'+esc(item.id)+'</td><td><button data-aa-open="'+i+'">Mở hồ sơ</button> '+(['bazi','marriage','business','childbirth','van_han'].includes(item.kind)?'<button data-aa-download="'+i+'" data-format="pdf">PDF</button> <button data-aa-download="'+i+'" data-format="docx">DOCX</button>':'<button data-aa-download="'+i+'" data-format="json">Tải hồ sơ</button>')+'</td></tr>').join('');
      list.innerHTML='<div class="history-table-wrap"><table class="history-table"><thead><tr><th>STT</th><th>Loại tư vấn</th><th>Khách hàng</th><th>Ngày tạo</th><th>Người tạo · Username</th><th>Mã hồ sơ</th><th>Thao tác</th></tr></thead><tbody>'+rows+'</tbody></table></div>'+(rows?'':'<p>Không có hồ sơ phù hợp bộ lọc.</p>')+'<div class="toolbar"><button id="aaPrev" '+(page===1?'disabled':'')+'>Trang trước</button><span>Trang '+page+' / '+Math.max(1,Math.ceil(data.total/50))+'</span><button id="aaNext" '+(page*50>=data.total?'disabled':'')+'>Trang sau</button></div>';
      data.warnings.forEach(w=>{const p=document.createElement('p');p.className='field-error';p.textContent=w;list.appendChild(p);});
      document.getElementById('aaPrev').onclick=()=>{page--;void load();};document.getElementById('aaNext').onclick=()=>{page++;void load();};
      list.querySelectorAll('[data-aa-open]').forEach(button=>button.onclick=()=>open(data.items[Number(button.dataset.aaOpen)]).catch(error=>api.showFlash(document.getElementById('globalFlash'),error.message,'error')));
      list.querySelectorAll('[data-aa-download]').forEach(button=>button.onclick=async()=>{button.disabled=true;try{await download(data.items[Number(button.dataset.aaDownload)],button.dataset.format);}catch(error){api.showFlash(document.getElementById('globalFlash'),error.message,'error');}finally{button.disabled=false;}});
    } catch(error) { if(sequence===requestSequence){summary.textContent='Chưa đọc được kho hồ sơ';list.textContent=error.message;} }
  }
  window.BteAdminArchive={start:async function(){
    let user;
    try {user=await api.get('/api/v1/auth/me');} catch(error){list.textContent=error.status===401?'Bạn cần đăng nhập để xem hồ sơ.':error.message;return true;}
    if(user.role!=='ADMIN')return false;
    if(!window.BteAdmin && new URLSearchParams(location.search).get('scope')==='mine')return false;
    document.getElementById('btnClearHist').hidden=true;
    const heading=document.querySelector('.history-page h1');heading.removeAttribute('data-i18n');heading.textContent='Quản lý toàn bộ hồ sơ';
    const hint=document.querySelector('.page-hero .muted');hint.removeAttribute('data-i18n');hint.textContent='Hồ sơ tư vấn của mọi tài khoản, lưu trên máy chủ.';
    const toolbar=document.createElement('div');toolbar.className='toolbar';
    toolbar.innerHTML='<label>Loại tư vấn <select id="aaKind"><option value="">Tất cả</option>'+Object.keys(labels).map(k=>'<option value="'+k+'">'+labels[k]+'</option>').join('')+'</select></label><label>Người tạo <select id="aaUser"><option value="">Mọi tài khoản</option></select></label><label>Tìm khách hàng / mã hồ sơ <input id="aaSearch" type="search"></label><button id="aaRefresh">Tìm / Làm mới</button><a href="/history?scope=mine" class="btn secondary">Hồ sơ của tôi</a>';
    summary.before(toolbar);document.getElementById('aaRefresh').onclick=()=>{page=1;void load();};
    if(window.BteAdmin && !BteAdmin.portalSession)toolbar.querySelector('a')?.remove();
    ['aaKind','aaUser'].forEach(id=>document.getElementById(id).onchange=()=>{page=1;void load();});
    document.getElementById('aaSearch').onkeydown=event=>{if(event.key==='Enter'){page=1;void load();}};
    await load();return true;
  },refresh:load};
})();
