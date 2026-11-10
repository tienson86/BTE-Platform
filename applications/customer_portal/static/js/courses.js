(function () {
  const host=document.getElementById('courseContent'),state=document.getElementById('courseState');
  if(!host)return;
  const api=window.BtePortal, query=new URLSearchParams(location.search);
  const courseId=query.get('course'),lessonId=query.get('lesson');
  let videoUrl=null;
  function el(tag,text){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;}
  function link(text,url,cls){const a=el('a',text);a.href=url;if(cls)a.className=cls;return a;}
  function url(id,lesson){return '/khoa-hoc?course='+encodeURIComponent(id)+(lesson?'&lesson='+encodeURIComponent(lesson):'');}
  function span(days){return days===null?'Không giới hạn thời gian':days+' ngày kể từ khi mở khóa';}
  function date(value){return value?new Date(value).toLocaleString('vi-VN'):'Không giới hạn thời gian';}
  function card(){const n=el('section');n.className='course-card';return n;}
  function money(n){return Number(n).toLocaleString('vi-VN')+' Linh Thạch';}
  function accessText(c){if(!c.access)return 'Chưa mở khóa';return c.access.active?'Đã mở • '+(c.access.expires_at?'Truy cập đến '+date(c.access.expires_at):'Không giới hạn thời gian'):'Quyền truy cập đã hết hạn';}
  function confirmPurchase(c,balance,onConfirm){
    const dialog=el('dialog');dialog.className='course-dialog';dialog.append(el('h2','Xác nhận mở khóa học'),el('p',c.title),el('p','Chi phí: '+money(c.price)),el('p',span(c.access_days)),el('p','Số dư: '+money(balance)+' → Còn lại: '+money(balance-c.price)));
    const actions=el('div');actions.className='course-tabs';const cancel=el('button','Quay lại'),yes=el('button','Xác nhận đổi');yes.className='course-action';
    const note=el('p');note.setAttribute('role','status');cancel.onclick=()=>dialog.close();
    yes.onclick=async()=>{yes.disabled=true;cancel.disabled=true;note.textContent='Đang mở khóa…';try{await onConfirm();dialog.close();location.assign(url(c.id));}catch(e){note.textContent=e.message;yes.disabled=false;cancel.disabled=false;}};
    actions.append(cancel,yes);dialog.append(actions,note);dialog.addEventListener('close',()=>dialog.remove());document.body.append(dialog);dialog.showModal();
  }
  async function catalog(){
    const data=await api.get('/api/v1/courses');state.textContent='Số dư của bạn: '+money(data.balance);host.replaceChildren();
    const controls=el('div');controls.className='course-tabs';const all=el('button','Tất cả khóa học'),mine=el('button','Khóa học của tôi');controls.append(all,mine);host.append(controls);
    const grid=el('div');grid.className='course-grid';host.append(grid);
    function draw(owned){grid.replaceChildren();const courses=data.courses.filter(c=>!owned||c.access);if(!courses.length)grid.append(el('p','Bạn chưa mở khóa học nào.'));
      courses.forEach(c=>{const box=card();box.append(el('p',c.subject),el('h2',c.title),el('p',c.summary));
        box.append(el('p',c.ready?c.lesson_count+' bài • Có bài học thử':'Đang biên soạn'));
        if(c.access)box.append(el('p',accessText(c)));
        box.append(el('p',c.status==='published'?money(c.price)+' • '+span(c.access_days):c.status==='paused'?'Tạm ngừng mở đổi mới':'Đang chuẩn bị • Chưa mở đổi'));
        box.append(link(c.access?.active?'Tiếp tục học':c.ready?'Xem lộ trình và học thử':'Xem giới thiệu',url(c.id),'course-action'));grid.append(box);
      });}
    all.onclick=()=>draw(false);mine.onclick=()=>draw(true);draw(false);
  }
  async function detail(){
    const [c,wallet]=await Promise.all([api.get('/api/v1/courses/'+encodeURIComponent(courseId)),api.get('/api/v1/courses')]);
    state.textContent='Số dư của bạn: '+money(wallet.balance);host.replaceChildren(link('← Tất cả khóa học','/khoa-hoc'));
    const intro=card();intro.style.marginTop='20px';intro.append(el('p',c.subject),el('h2',c.title),el('p',c.summary),el('p',accessText(c)));
    if(c.admin_preview)intro.append(el('p','Chế độ Admin: xem trước bài học, không cần đổi khóa.'));
    if(!c.access?.active&&c.ready&&c.status==='published'&&!c.admin_preview){
      intro.append(el('p','Giá mở khóa: '+money(c.price)+' • '+span(c.access_days)));
      const button=el('button','Đổi '+money(c.price)+' để mở khóa');button.className='course-action';button.disabled=wallet.balance<c.price;
      if(button.disabled)intro.append(el('p','Số dư Linh Thạch chưa đủ.'));
      const key=(window.crypto?.randomUUID?.()||'op_'+Date.now()+'_'+Math.random().toString(36).slice(2));
      button.onclick=()=>confirmPurchase(c,wallet.balance,()=>api.post('/api/v1/courses/'+encodeURIComponent(c.id)+'/redeem',{operation_key:key,expected_revision:c.revision}));intro.append(button);
    }else if(!c.access?.active&&!c.admin_preview)intro.append(el('p','Khóa học chưa mở đổi. Bài học thử vẫn có thể xem nếu đã sẵn sàng.'));
    const progressLabel=el('p');function updateProgress(){progressLabel.textContent='Tiến độ: '+c.lessons.filter(l=>l.completed).length+'/'+c.lessons.length+' bài đã đánh dấu hoàn thành.';}updateProgress();intro.append(progressLabel);host.append(intro);
    if(!c.lessons.length)return;
    const study=el('div');study.className='course-study';const main=card(),aside=card();const heading=el('h3','Danh sách bài học');aside.append(heading);
    const selected=c.lessons.find(l=>l.id===lessonId)||c.lessons.find(l=>!l.completed&&!l.locked)||c.lessons.find(l=>!l.locked)||c.lessons[0];
    c.lessons.forEach(l=>{const a=link((l.completed?'✓ ':l.locked?'🔒 ':'')+l.title+(l.trial?' • Học thử':''),url(c.id,l.id),'course-lesson-link');if(l.id===selected.id)a.setAttribute('aria-current','page');aside.append(a);});
    study.append(main,aside);host.append(study);
    if(selected.locked){main.append(el('h2',selected.title),el('p','Bài học này cần mở khóa. Xem thông tin đổi khóa ở phía trên.'));return;}
    const lesson=await api.get('/api/v1/courses/'+encodeURIComponent(c.id)+'/lessons/'+encodeURIComponent(selected.id));
    main.append(el('p',lesson.section),el('h2',lesson.title),el('p','Mục tiêu: '+lesson.goal));
    if(lesson.video){
      const player=el('video');player.controls=true;player.preload='metadata';player.className='course-video';player.setAttribute('aria-label','Video thực hành Mai Hoa Dịch Số có giọng đọc');main.append(player);
      const msg=el('p','Đang tải video…');main.append(msg);
      const res=await fetch('/backend/api/v1/courses/'+encodeURIComponent(c.id)+'/lessons/'+encodeURIComponent(lesson.id)+'/video',{headers:{Authorization:'Bearer '+api.getToken()}});
      if(res.ok){videoUrl=URL.createObjectURL(await res.blob());player.src=videoUrl;msg.remove();}else{msg.textContent='Không tải được video. Vui lòng tải lại trang hoặc kiểm tra quyền truy cập.';}
    }
    const body=el('div',lesson.body);body.className='course-body';main.append(body,el('h3','Tự thực hành'),el('p',lesson.exercise));
    const answer=el('details');answer.append(el('summary','Xem đáp án và giải thích'),el('p',lesson.answer));main.append(answer);
    const actions=el('div');actions.className='course-tabs';const done=el('button',selected.completed?'Đã hoàn thành ✓':'Đánh dấu đã học');done.className='course-action';done.disabled=selected.completed;
    done.onclick=async()=>{done.disabled=true;try{await api.api('PUT','/api/v1/courses/'+encodeURIComponent(c.id)+'/lessons/'+encodeURIComponent(lesson.id)+'/progress',{completed:true});done.textContent='Đã hoàn thành ✓';selected.completed=true;updateProgress();const current=aside.querySelector('[aria-current="page"]');if(current)current.textContent='✓ '+selected.title+(selected.trial?' • Học thử':'');state.textContent='Đã lưu tiến độ học.';}catch(e){done.disabled=false;state.textContent=e.message;}};
    actions.append(done);const index=c.lessons.findIndex(l=>l.id===selected.id);if(index>0)actions.append(link('← Bài trước',url(c.id,c.lessons[index-1].id)));if(index<c.lessons.length-1)actions.append(link('Bài tiếp theo →',url(c.id,c.lessons[index+1].id)));main.append(actions);
  }
  window.addEventListener('pagehide',()=>{if(videoUrl)URL.revokeObjectURL(videoUrl);});
  (courseId?detail():catalog()).catch(e=>{state.textContent=e.message;state.classList.add('course-error');});
})();
