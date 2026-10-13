(function(){
  const byId=id=>document.getElementById(id), state=byId('vhState');
  const esc=v=>String(v==null?'':v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let sources=[],active=null,busy=false;
  const year=new Date().getFullYear();byId('vhStart').value=year;byId('vhEnd').value=year;
  function setBusy(value){busy=value;byId('vhCalculate').disabled=value;byId('vhCreate').disabled=value;}
  async function loadSources(selected){
    const response=await BtePortal.get('/api/v1/van-han/sources');sources=response.items;
    byId('vhSource').innerHTML='<option value="">Chọn lá số đã lưu</option>'+sources.map((s,i)=>'<option value="'+i+'">'+esc(s.name)+' · '+esc(s.creator_username||'')+' · '+esc(new Date(s.created_at).toLocaleString('vi-VN'))+'</option>').join('');
    if(selected){const index=sources.findIndex(s=>s.id===selected);if(index>=0)byId('vhSource').value=String(index);}
  }
  async function history(){
    const response=await BtePortal.get('/api/v1/van-han/history');
    byId('vhHistory').innerHTML=response.items.map(r=>'<p><button data-open="'+esc(r.id)+'">'+esc(r.name)+'</button> · '+esc(new Date(r.created_at).toLocaleString('vi-VN'))+' · '+esc(r.creator_username)+'</p>').join('')||'<p>Chưa có hồ sơ vận hạn.</p>';
    byId('vhHistory').querySelectorAll('[data-open]').forEach(button=>button.onclick=async()=>{if(busy)return;setBusy(true);try{const response=await BtePortal.get('/api/v1/van-han/'+encodeURIComponent(button.dataset.open));render(response.row);}catch(e){state.textContent=e.message;}finally{setBusy(false);}});
  }
  function render(row){
    active=row;window.history.replaceState(null,'','/tinh-van-han?id='+encodeURIComponent(row.id));const result=row.result,p=result.profile,u=p.useful;
    byId('vhResult').innerHTML='<h2>'+esc(result.name)+'</h2><p>Cung '+esc(result.years[0].cung_phi.personal)+' · '+esc(p.strength)+' · Dụng thần '+esc(u.element)+' '+esc(u.stem)+' · Hỷ thần '+esc(u.favorable.join(', '))+' · Kỵ thần '+esc(u.unfavorable.join(', '))+'</p><p>Hồ sơ '+esc(row.id)+' · Người tạo: '+esc(row.creator_display_name)+' · '+esc(row.creator_username)+'</p><div class="toolbar"><label>Xem năm <select id="vhYear"><option value="all">Tất cả</option>'+result.years.map(y=>'<option>'+y.year+'</option>').join('')+'</select></label><label><input id="vhOnly" type="checkbox"> Chỉ hiện năm/tháng có dấu hiệu cần lưu ý</label><button data-export="pdf">Tải PDF</button><button data-export="docx">Tải DOCX</button></div><div id="vhPeriods"></div>';
    byId('vhYear').onchange=periods;byId('vhOnly').onchange=periods;periods();
    byId('vhResult').querySelectorAll('[data-export]').forEach(button=>button.onclick=()=>download(button));
  }
  function periods(){
    const chosen=byId('vhYear').value,only=byId('vhOnly').checked;
    const content=active.result.years.filter(y=>chosen==='all'||String(y.year)===chosen).map(y=>{
      const months=y.months.filter(m=>!only||m.review_candidate);
      if(only&&!y.review_candidate&&!months.length)return '';
      const rows=months.map(m=>'<tr><td>'+m.month+(m.leap?' nhuận':'')+'</td><td>'+esc(m.start)+' – '+esc(m.end)+'</td><td>'+esc(m.ganzhi)+'</td><td>'+esc(m.cung_phi.period)+' · '+esc(m.cung_phi.relationship)+'</td><td>'+esc(m.bazi.verdict)+'</td><td><details><summary>Luận và cơ sở</summary><p>'+esc(m.narrative)+'</p><ul>'+m.bazi.evidence.map(e=>'<li>'+esc(e.text)+'</li>').join('')+'</ul></details></td></tr>').join('');
      return '<section><h3>'+y.year+' · '+esc(y.ganzhi)+'</h3><p>Cung phi: '+esc(y.cung_phi.relationship)+' · Bát Tự: '+esc(y.bazi.verdict)+'</p><p>'+esc(y.narrative)+'</p><div class="history-table-wrap"><table class="history-table"><thead><tr><th>Tháng âm</th><th>Ngày dương lịch</th><th>Can Chi</th><th>Cung phi · Du Niên</th><th>Bát Tự</th><th>Chi tiết</th></tr></thead><tbody>'+rows+'</tbody></table></div></section>';
    }).join('');byId('vhPeriods').innerHTML=content||'<p>Không có thời điểm phù hợp bộ lọc.</p>';
  }
  async function download(button){
    button.disabled=true;try{
      const response=await fetch('/backend/api/v1/van-han/'+encodeURIComponent(active.id)+'/export/'+button.dataset.export,{headers:{Authorization:'Bearer '+BtePortal.getToken()}});
      if(!response.ok)throw Error('Chưa xuất được tài liệu ('+response.status+').');
      const link=document.createElement('a');link.href=URL.createObjectURL(await response.blob());link.download='BTE_TinhVanHan_'+active.id+'.'+button.dataset.export;document.body.appendChild(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(link.href),1000);
    }catch(e){state.textContent=e.message;}finally{button.disabled=false;}
  }
  byId('vhForm').onsubmit=async event=>{
    event.preventDefault();if(busy)return;const index=byId('vhSource').value;
    if(index===''){state.textContent='Bạn cần chọn lá số nguồn.';return;}
    const source=sources[Number(index)];setBusy(true);state.textContent='Đang tính và lưu hồ sơ trên máy chủ…';
    try{const response=await BtePortal.post('/api/v1/van-han/analyze',{analysis_id:source.id,source_owner:source.owner,start_year:Number(byId('vhStart').value),end_year:Number(byId('vhEnd').value)});render(response.row);await history();state.textContent='Đã lưu hồ sơ vận hạn trên máy chủ.';}catch(e){state.textContent=e.message;}finally{setBusy(false);}
  };
  byId('vhCreate').onclick=async()=>{
    if(busy)return;const date=byId('vhBirth').value,time=byId('vhTime').value;
    if(!date||!time){state.textContent='Nhập đủ ngày và giờ sinh để lập lá số nguồn.';return;}
    const d=date.split('-').map(Number),t=time.split(':').map(Number);setBusy(true);state.textContent='Đang lập và lưu lá số nguồn…';
    try{const response=await BtePortal.post('/api/v1/analyze',{full_name:byId('vhName').value,gender:byId('vhGender').value,year:d[0],month:d[1],day:d[2],hour:t[0],minute:t[1],birth_place:byId('vhPlace').value,timezone:'Asia/Ho_Chi_Minh'});const data=response.data||response;await loadSources(data.analysis_id||response.analysis_id);state.textContent='Đã lập lá số. Chọn khoảng năm rồi bấm Tính và lưu vận hạn.';}catch(e){state.textContent=e.message;}finally{setBusy(false);}
  };
  (async()=>{try{await BtePortal.get('/api/v1/auth/me');await loadSources();await history();const id=new URLSearchParams(location.search).get('id');if(id){const response=await BtePortal.get('/api/v1/van-han/'+encodeURIComponent(id));render(response.row);}}catch(e){state.textContent=e.status===401?'Bạn cần đăng nhập để tính và xem hồ sơ vận hạn.':e.message;}})();
})();
