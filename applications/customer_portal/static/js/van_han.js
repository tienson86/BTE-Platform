(function(){
  const byId=id=>document.getElementById(id), state=byId('vhState');
  const esc=v=>String(v==null?'':v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let sources=[],selectedSource=null,active=null,busy=false,exporting=false,sourceDirty=false;
  const searchInput=byId("vhSourceSearch"),popup=byId("vhSourcePopup"),options=byId("vhSourceOptions");
  let searchSequence=0,searchTimer=null,openWanted=false,activeIndex=-1,hasMore=false;
  const year=new Date().getFullYear();byId('vhStart').value=year;byId('vhEnd').value=year;
  function setBusy(value){busy=value;byId('vhCalculate').disabled=value;byId('vhCreate').disabled=value;searchInput.disabled=value;byId('vhSourceToggle').disabled=value;byId('vhSourceMore').disabled=value;updateExportAvailability();}
  function updateExportAvailability(){byId('vhResult').querySelectorAll('[data-export]').forEach(button=>button.disabled=busy||exporting||sourceDirty);}
  function when(value){const d=new Date(value);return Number.isNaN(d.getTime())?'Chưa có ngày lập':d.toLocaleString('vi-VN');}
  function birthLabel(source){return source.birth_date ? source.birth_date.split('-').reverse().join('/') : 'Chưa có ngày sinh';}
  function sourceLabel(source){return source.name+' · '+birthLabel(source)+' · '+(source.birth_time||'Chưa có giờ sinh')+' · '+(source.creator_username||'');}
  function closePopup(){openWanted=false;popup.hidden=true;searchInput.setAttribute('aria-expanded','false');searchInput.removeAttribute('aria-activedescendant');}
  function choose(source){
    selectedSource=source;searchSequence++;searchInput.value=source.name;
    sourceDirty=Boolean(active&&(active.result.source_analysis_id!==source.id||(active.result.source_owner&&active.result.source_owner!==source.owner)));
    if(sourceDirty)state.textContent='Bạn đã đổi lá số nguồn. Bấm Tính và lưu vận hạn để tạo kết quả mới.';updateExportAvailability();
    byId('vhSourceChosen').textContent='Đã chọn: '+sourceLabel(source)+' · Lập '+when(source.created_at)+' · Mã '+source.id;
    closePopup();
  }
  function highlight(index){
    activeIndex=index;options.querySelectorAll('[role="option"]').forEach((el,i)=>el.setAttribute('aria-selected',String(i===index)));
    const option=byId('vhSourceOption'+index);if(option){searchInput.setAttribute('aria-activedescendant',option.id);option.scrollIntoView({block:'nearest'});}
  }
  function renderOptions(total){
    options.innerHTML=sources.map((source,i)=>'<button type="button" id="vhSourceOption'+i+'" class="vh-source-option" role="option" aria-selected="false"><strong>'+esc(source.name)+'</strong><small>Ngày sinh dương lịch '+esc(birthLabel(source))+' · '+esc(source.gender==='male'?'Nam':source.gender==='female'?'Nữ':'—')+' · '+esc(source.birth_time||'Chưa có giờ sinh')+' · '+esc(source.creator_username)+'</small><small>Lập '+esc(when(source.created_at))+' · Mã '+esc(source.id.slice(-8))+'</small></button>').join('')||'<p>Không tìm thấy họ tên phù hợp.</p>';
    options.querySelectorAll('[role="option"]').forEach((button,i)=>button.onclick=()=>{choose(sources[i]);searchInput.focus();});
    activeIndex=-1;byId('vhSourceCount').textContent='Hiển thị '+sources.length+' / '+total+' hồ sơ';byId('vhSourceMore').hidden=!hasMore;
    popup.hidden=!openWanted;searchInput.setAttribute('aria-expanded',String(openWanted));
  }
  async function querySources(append=false){
    const sequence=++searchSequence,query=searchInput.value.trim(),offset=append?sources.length:0;
    if(!append){sources=[];activeIndex=-1;searchInput.removeAttribute('aria-activedescendant');options.innerHTML='<p>Đang tìm hồ sơ…</p>';}
    popup.hidden=!openWanted;searchInput.setAttribute('aria-expanded',String(openWanted));
    try{
      const params=new URLSearchParams({q:query,limit:'30',offset:String(offset)});
      const response=await BtePortal.get('/api/v1/van-han/sources?'+params);
      if(sequence!==searchSequence)return;
      sources=append?sources.concat(response.items.filter(s=>!sources.some(old=>old.owner===s.owner&&old.id===s.id))):response.items;
      hasMore=response.has_more;renderOptions(response.total);
    }catch(error){if(sequence===searchSequence){options.textContent='Chưa đọc được hồ sơ. '+error.message;hasMore=false;byId('vhSourceMore').hidden=true;}}
  }
  async function loadSources(selected,owner){
    if(!selected){sources=[];return;}
    const sequence=++searchSequence;
    const params=new URLSearchParams({analysis_id:selected,limit:'2'});if(owner)params.set('source_owner',owner);
    const response=await BtePortal.get('/api/v1/van-han/sources?'+params);
    if(sequence!==searchSequence)return;
    if(response.items.length===1)choose(response.items[0]);
    else{selectedSource=null;byId('vhSourceChosen').textContent='Chọn lại lá số nguồn theo họ tên và ngày sinh.';}
  }
  searchInput.addEventListener('input',()=>{
    if(busy)return;selectedSource=null;sourceDirty=true;updateExportAvailability();sources=[];activeIndex=-1;searchInput.removeAttribute('aria-activedescendant');options.innerHTML='<p>Đang tìm hồ sơ…</p>';byId('vhSourceCount').textContent='';byId('vhSourceMore').hidden=true;byId('vhSourceChosen').textContent='Chọn đúng hồ sơ trong danh sách trước khi tính.';
    openWanted=true;searchSequence++;clearTimeout(searchTimer);searchTimer=setTimeout(()=>querySources(),250);
  });
  byId('vhSourceToggle').onclick=()=>{if(busy)return;if(!popup.hidden){closePopup();return;}openWanted=true;searchInput.focus();void querySources();};
  byId('vhSourceMore').onclick=()=>querySources(true);
  searchInput.addEventListener('keydown',event=>{
    if(event.key==='Escape'){closePopup();return;}
    if(event.key==='ArrowDown'||event.key==='ArrowUp'){
      event.preventDefault();if(popup.hidden){openWanted=true;void querySources();return;}
      if(sources.length)highlight(Math.max(0,Math.min(sources.length-1,activeIndex+(event.key==='ArrowDown'?1:-1))));
    }
    if(event.key==='Enter'&&!popup.hidden){event.preventDefault();if(activeIndex>=0)choose(sources[activeIndex]);else if(sources.length===1)choose(sources[0]);}
    if(event.key==='Tab')closePopup();
  });
  document.addEventListener('pointerdown',event=>{if(!event.target.closest('.vh-source-picker'))closePopup();});
  async function history(){
    const response=await BtePortal.get('/api/v1/van-han/history');
    byId('vhHistory').innerHTML=response.items.map(r=>'<p><button data-open="'+esc(r.id)+'">'+esc(r.name)+'</button> · '+esc(new Date(r.created_at).toLocaleString('vi-VN'))+' · '+esc(r.creator_username)+'</p>').join('')||'<p>Chưa có hồ sơ vận hạn.</p>';
    byId('vhHistory').querySelectorAll('[data-open]').forEach(button=>button.onclick=async()=>{if(busy)return;setBusy(true);try{const response=await BtePortal.get('/api/v1/van-han/'+encodeURIComponent(button.dataset.open));render(response.row);}catch(e){state.textContent=e.message;}finally{setBusy(false);}});
  }
  function render(row){
    active=row;sourceDirty=false;void loadSources(row.result.source_analysis_id,row.result.source_owner).catch(e=>{byId('vhSourceChosen').textContent=e.message;});window.history.replaceState(null,'','/tinh-van-han?id='+encodeURIComponent(row.id));const result=row.result,p=result.profile,u=p.useful;
    byId('vhResult').innerHTML='<h2>'+esc(result.name)+'</h2><p>Cung '+esc(result.years[0].cung_phi.personal)+' · '+esc(p.strength)+' · Dụng thần '+esc(u.element)+' '+esc(u.stem)+' · Hỷ thần '+esc(u.favorable.join(', '))+' · Kỵ thần '+esc(u.unfavorable.join(', '))+'</p><p>Hồ sơ '+esc(row.id)+' · Người tạo: '+esc(row.creator_display_name)+' · '+esc(row.creator_username)+'</p><div class="toolbar"><label>Xem năm <select id="vhYear"><option value="all">Tất cả</option>'+result.years.map(y=>'<option>'+y.year+'</option>').join('')+'</select></label><label><input id="vhOnly" type="checkbox"> Chỉ hiện năm/tháng có dấu hiệu cần lưu ý</label><button data-export="pdf">Tải PDF</button><button data-export="docx">Tải DOCX</button></div><div id="vhPeriods"></div>';
    byId('vhYear').onchange=periods;byId('vhOnly').onchange=periods;periods();updateExportAvailability();
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
    if(exporting||busy||sourceDirty||!active)return;exporting=true;setBusy(true);closePopup();
    const identifier=active.id,format=button.dataset.export,label=button.textContent;
    const buttons=Array.from(byId('vhResult').querySelectorAll('[data-export]'));
    buttons.forEach(b=>b.disabled=true);button.textContent='Đang tạo '+format.toUpperCase()+'…';
    state.textContent='Đang tạo tài liệu '+format.toUpperCase()+'. Hồ sơ dài có thể cần thêm thời gian.';
    const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),330000);
    try{
      const response=await fetch('/backend/api/v1/van-han/'+encodeURIComponent(identifier)+'/export/'+format,{headers:{Authorization:'Bearer '+BtePortal.getToken()},signal:controller.signal});
      if(!response.ok){let detail='';try{const data=await response.json();detail=typeof data.detail==='string'?data.detail:data.message||'';}catch(_){}throw Error(detail||'Chưa xuất được tài liệu ('+response.status+').');}
      const blob=await response.blob(),head=new Uint8Array(await blob.slice(0,4).arrayBuffer());
      if((format==='pdf'&&String.fromCharCode(...head)!=='%PDF')||(format==='docx'&&(head[0]!==80||head[1]!==75)))throw Error('Máy chủ chưa trả về tệp '+format.toUpperCase()+' hợp lệ.');
      const disposition=response.headers.get('Content-Disposition')||'',utf8=disposition.match(/filename\*=UTF-8''([^;]+)/i),plain=disposition.match(/filename="?([^";]+)/i);
      let filename='BTE_TinhVanHan_'+identifier+'.'+format;
      try{if(utf8)filename=decodeURIComponent(utf8[1].replace(/^"|"$/g,''));else if(plain)filename=plain[1];}catch(_){}
      const link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download=filename;document.body.appendChild(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(link.href),1000);
      state.textContent='Đã tải '+format.toUpperCase()+'.';
    }catch(error){state.textContent=error.name==='AbortError'?'Tạo tài liệu vượt thời gian chờ. Hãy thử lại với khoảng năm ngắn hơn.':error instanceof TypeError?'Mất kết nối khi tải tài liệu. Hãy kiểm tra BTE đang chạy và thử lại.':error.message;}
    finally{clearTimeout(timer);exporting=false;setBusy(false);updateExportAvailability();button.textContent=label;}
  }
  byId('vhForm').onsubmit=async event=>{
    event.preventDefault();if(busy)return;
    if(!selectedSource){state.textContent='Bạn cần chọn lá số nguồn.';return;}
    const source=selectedSource;closePopup();setBusy(true);state.textContent='Đang tính và lưu hồ sơ trên máy chủ…';
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
