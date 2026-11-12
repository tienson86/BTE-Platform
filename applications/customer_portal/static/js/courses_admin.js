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
  function lessonEditor(endpoint, lesson, onSave) {
    const box = el('details');
    const heading = el('summary', lesson.title || 'Thêm bài học');
    const form = el('form');
    form.className = 'course-form';
    const specs = [
      ['title', 'Tên bài', 200, 'text', true],
      ['section', 'Tên mô-đun', 120, 'text', true],
      ['goal', 'Mục tiêu', 1000, 'textarea'],
      ['body', 'Nội dung bài giảng', 60000, 'textarea', true],
      ['exercise', 'Bài tập thực hành', 6000, 'textarea'],
      ['answer', 'Đáp án và giải thích', 6000, 'textarea'],
    ];
    for (const [name, caption, max, type, required] of specs) {
      const input = field(form, name, caption, lesson[name], type);
      input.maxLength = max;
      input.required = Boolean(required);
      if (type === 'textarea') {
        input.rows = name === 'body' ? 9 : 3;
        input.parentElement.classList.add('course-wide');
      }
    }
    const trialLabel = el('label', 'Cho phép học thử');
    trialLabel.className = 'course-check course-wide';
    const trial = el('input');
    trial.type = 'checkbox';
    trial.checked = Boolean(lesson.trial);
    trialLabel.prepend(trial);
    const save = el('button', 'Lưu bài học');
    const message = el('p');
    message.setAttribute('role', 'status');
    form.append(trialLabel, save, message);
    box.append(heading, form);
    form.onsubmit = async event => {
      event.preventDefault();
      save.disabled = true;
      message.textContent = 'Đang lưu…';
      try {
        const payload = {...Object.fromEntries(new FormData(form)), trial: trial.checked, expected_revision: lesson.revision || 0};
        if (lesson.id) {
          lesson = await api.put(endpoint + '/' + encodeURIComponent(lesson.id), payload);
          heading.textContent = lesson.title;
        } else {
          onSave(await api.post(endpoint, payload));
          form.reset();
        }
        message.textContent = 'Đã lưu bài học.';
      } catch (error) {
        message.textContent = error.message;
      } finally {
        save.disabled = false;
      }
    };
    return box;
  }
  function courseLessons(course, onAdd) {
    const box = el('details');
    const endpoint = '/api/v1/admin/courses/' + encodeURIComponent(course.id) + '/lessons';
    const content = el('div', 'Đang tải…');
    box.append(el('summary', 'Sửa nội dung và thêm mô-đun'), content);
    let loaded = false;
    box.ontoggle = async () => {
      if (!box.open || loaded) return;
      loaded = true;
      try {
        const lessons = await api.get(endpoint);
        const existing = el('div');
        for (const lesson of lessons) existing.append(lessonEditor(endpoint, lesson));
        content.replaceChildren(lessonEditor(endpoint, {}, lesson => {
          existing.append(lessonEditor(endpoint, lesson));
          onAdd();
        }), existing);
      } catch (error) {
        content.textContent = error.message + ' Đóng rồi mở lại để thử lại.';
        loaded = false;
      }
    };
    return box;
  }
  function createCourse() {
    const card = el('section');
    card.className = 'course-card';
    const form = el('form');
    form.className = 'course-form';
    const title = field(form, 'title', 'Tên khóa học mới');
    const subject = field(form, 'subject', 'Chủ đề');
    title.required = subject.required = true;
    title.maxLength = 160;
    subject.maxLength = 120;
    const button = el('button', 'Tạo khóa học');
    const message = el('p');
    message.setAttribute('role', 'status');
    form.append(button, message);
    card.append(el('h3', 'Tạo khóa học Online'), form);
    form.onsubmit = async event => {
      event.preventDefault();
      button.disabled = true;
      try {
        await api.post('/api/v1/admin/courses', {title: title.value, subject: subject.value});
        await load();
      } catch (error) {
        message.textContent = error.message;
        button.disabled = false;
      }
    };
    return card;
  }
  async function load() {
    state.textContent='Đang tải cấu hình…';
    try {
      await api.ready();
      const data=await api.get('/api/v1/admin/courses'); host.replaceChildren(createCourse());
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
        const count = el('p', course.ready ? course.lesson_count + ' bài học' : 'Thêm bài học trước khi mở đổi.');
        form.append(count);
        const msg=el('p');msg.className='course-wide';msg.setAttribute('role','status');
        const save=el('button','Lưu cấu hình khóa học');save.type='submit';
        const toggle=el('button');toggle.type='button';toggle.className='course-action';
        const actions=el('div');actions.className='course-tabs course-wide';actions.append(save,toggle);
        const badge=el('p');badge.className='course-wide';
        form.append(badge,actions,msg);
        const preview=el('a','Xem trang khóa học');
        preview.href='/khoa-hoc?course='+encodeURIComponent(course.id);
        form.append(preview);
        let revision=course.revision, persistedStatus=course.status;
        function showStatus() {
          const published=persistedStatus==='published';
          badge.textContent='Trạng thái trên trang thành viên: '+(published?'Đang mở đổi bằng Linh Thạch':persistedStatus==='paused'?'Tạm ngừng đổi mới':'Đang chuẩn bị');
          toggle.textContent=published?'Tạm ngừng đổi mới':'Mở đổi bằng Linh Thạch';
          toggle.disabled=!course.ready;
        }
        showStatus();
        async function persist(nextStatus){
          if(!form.reportValidity())return;
          save.disabled=toggle.disabled=true;msg.classList.remove('course-error');msg.textContent='Đang lưu…';
          try {
            const next=await api.put('/api/v1/admin/courses/'+course.id,{title:title.value,summary:summary.value,price:Number(price.value),access_days:forever.checked?null:Number(days.value),status:nextStatus,expected_revision:revision});
            revision=next.revision;persistedStatus=next.status;status.value=next.status;
            msg.textContent=next.status==='published'?'Đã mở đổi cho thành viên còn hiệu lực ở cả ba cấp.':'Đã lưu. Quyền đã mở trước đây vẫn được giữ.';
          } catch(err){msg.textContent=err.message;msg.classList.add('course-error');}
          finally{save.disabled=false;showStatus();}
        }
        form.onsubmit=e=>{e.preventDefault();void persist(status.value);};
        toggle.onclick=()=>persist(persistedStatus==='published'?'paused':'published');
        card.append(form, courseLessons(course, () => {
          course.ready = true;
          course.lesson_count += 1;
          count.textContent = course.lesson_count + ' bài học';
          status.querySelector('[value="published"]').disabled = false;
          showStatus();
        }));
        host.append(card);
      }); state.textContent='Giá và thời hạn của mỗi khóa được quản lý riêng.';
    } catch(err){state.textContent=err.message;}
  }
  document.getElementById('courseAdminReload').onclick=load;load();
})();
