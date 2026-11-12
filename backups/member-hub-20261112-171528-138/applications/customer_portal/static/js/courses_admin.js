(function () {
  const api = window.BteAdmin;
  const host = document.getElementById('courseAdminContent');
  const state = document.getElementById('courseAdminState');
  if (!host || !api) return;
  function el(tag, text) { const n=document.createElement(tag); if(text!==undefined)n.textContent=text; return n; }
  function field(form, name, labelText, value, type='text') {
    const label=el('label',labelText), input=el(type==='textarea'?'textarea':'input');
    input.name=name; if(type!=='textarea')input.type=type; input.value=value??''; label.append(input); form.append(label); return input;
  }
  async function load() {
    state.textContent='Đang tải cấu hình…';
    try {
      await api.ready();
      const data=await api.get('/api/v1/admin/courses'); host.replaceChildren();
      data.courses.forEach(course=>{
        const card=el('section');card.className='course-card';card.style.marginTop='24px';
        card.append(el('h3',course.subject));
        const form=el('form');form.className='course-form';
        const title=field(form,'title','Tên khóa học',course.title); title.required=true;title.maxLength=160;
        const summary=field(form,'summary','Giới thiệu',course.summary,'textarea');summary.maxLength=1200;
        const price=field(form,'price','Giá mở khóa (Linh Thạch)',course.price,'number');price.required=true;price.min=0;price.max=1000000;price.step=1;
        const days=field(form,'access_days','Thời hạn truy cập (ngày)',course.access_days,'number');days.min=1;days.max=36500;days.step=1;
        const foreverLabel=el('label','Không giới hạn thời gian truy cập');foreverLabel.className='course-check course-wide';
        const forever=el('input');forever.type='checkbox';forever.checked=course.access_days===null;foreverLabel.prepend(forever);form.append(foreverLabel);
        function duration(){days.disabled=forever.checked;days.required=!forever.checked;} duration();forever.onchange=duration;
        const statusLabel=el('label','Trạng thái'), status=el('select');
        [['draft','Đang chuẩn bị'],['published','Mở đổi khóa học'],['paused','Tạm ngừng đổi mới']].forEach(([value,label])=>{const o=el('option',label);o.value=value;o.selected=course.status===value;if(value==='published'&&!course.ready)o.disabled=true;status.append(o);});
        statusLabel.append(status);form.append(statusLabel);
        form.append(el('p',course.ready?course.lesson_count+' bài. Bài đầu được học thử.':'Chưa có bài học. Có thể cấu hình trước, chưa mở đổi.'));
        const msg=el('p');msg.className='course-wide';msg.setAttribute('role','status');
        const save=el('button','Lưu cấu hình khóa học');save.type='submit';save.className='course-action';form.append(save,msg);
        let revision=course.revision;
        form.onsubmit=async e=>{e.preventDefault();save.disabled=true;msg.textContent='Đang lưu…';
          try {const next=await api.put('/api/v1/admin/courses/'+course.id,{title:title.value,summary:summary.value,price:Number(price.value),access_days:forever.checked?null:Number(days.value),status:status.value,expected_revision:revision});revision=next.revision;msg.textContent='Đã lưu. Quyền đã mở trước đây giữ nguyên.';}
          catch(err){msg.textContent=err.message;msg.classList.add('course-error');}
          finally{save.disabled=false;}
        };
        card.append(form);host.append(card);
      }); state.textContent='Giá và thời hạn của mỗi khóa được quản lý riêng.';
    } catch(err){state.textContent=err.message;}
  }
  document.getElementById('courseAdminReload').onclick=load;load();
})();
