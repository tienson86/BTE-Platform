(function(){
  const root=document.querySelector('[data-knowledge="admin"]');if(!root)return;
  const api=window.BteAdmin,K=window.BteKnowledge,$=id=>document.getElementById(id),state=$('libraryAdminState');
  const form=$('libraryArticleForm'),structureForm=$('libraryStructureForm'),filters=$('libraryAdminFilters');
  let categories=[],editing=null,structureEditing=null,structureKind='category',page=1,busy=false,dirty=false,sequence=0,listSequence=0,saveNonce=null,canNext=false;
  function error(notice,failure){notice.textContent=failure.message||'Chưa hoàn tất thao tác. Vui lòng thử lại.';}
  function setBusy(value){busy=value;root.querySelectorAll('button,input,textarea,select').forEach(element=>element.disabled=value);if(!value){$('libraryAdminPrevious').disabled=page===1;$('libraryAdminNext').disabled=!canNext;}}
  function canDiscard(){return !dirty||window.confirm('Bài đang soạn có thay đổi chưa lưu. Bạn muốn bỏ thay đổi để tiếp tục?');}
  function option(value,text){const element=K.node('option',text);element.value=value;return element;}
  function fillCategories(select,allowAll=false){const chosen=select.value;select.replaceChildren();if(allowAll)select.append(option('','Tất cả chuyên mục'));categories.forEach(item=>select.append(option(item.id,item.title)));if([...select.options].some(item=>item.value===chosen))select.value=chosen;}
  function fillGroups(wanted){const category=categories.find(item=>item.id===form.elements.category_id.value),select=form.elements.group_id;const chosen=wanted||select.value;select.replaceChildren();(category?.groups||[]).forEach(item=>select.append(option(item.id,item.title)));if([...select.options].some(item=>item.value===chosen))select.value=chosen;}
  function renderStructure(){
    const tree=$('libraryStructureTree');tree.replaceChildren();
    categories.forEach(category=>{
      const section=K.node('section',undefined,'library-structure-category'),button=K.node('button',category.position+'. '+category.title);button.type='button';button.onclick=()=>{if(!busy)composeStructure('category',category);};section.append(button);
      category.groups.forEach(group=>{const edit=K.node('button',group.position+'. '+group.title,'secondary library-group-button');edit.type='button';edit.onclick=()=>{if(!busy)composeStructure('group',group);};section.append(edit);});tree.append(section);
    });
  }
  async function loadCatalog(){
    const data=await api.get('/api/v1/admin/knowledge/catalog');categories=data.categories;
    fillCategories(form.elements.category_id);fillGroups();fillCategories(filters.elements.category_id,true);fillCategories(structureForm.elements.category_id);renderStructure();
  }
  async function loadArticles(){
    const current=++listSequence,params=new URLSearchParams({page:String(page)});
    for(const name of ['category_id','status','q'])if(filters.elements[name].value.trim())params.set(name,filters.elements[name].value.trim());
    const data=await api.get('/api/v1/admin/knowledge/articles?'+params);
    if(current!==listSequence)return;
    const list=$('libraryAdminArticles');list.replaceChildren();$('libraryAdminCount').textContent=data.total+' bài viết';
    data.items.forEach(article=>{
      const button=K.node('button',undefined,'library-article-card');button.type='button';
      button.append(K.node('span',article.status==='published'?'Đã đăng':'Bản nháp','library-status'),K.node('strong',article.title),K.node('small',article.category_title+' · '+article.group_title+' · Thứ tự '+article.position),K.node('small','Cập nhật '+K.date(article.updated_at)));
      button.onclick=()=>{if(!busy&&canDiscard())void openArticle(article.id).catch(failure=>error(state,failure));};list.append(button);
    });
    if(!data.items.length)list.append(K.node('p','Chưa có bài trong nhóm này. Chọn “Soạn bài mới” để bắt đầu.','muted'));
    canNext=page*data.limit<data.total;$('libraryAdminPrevious').disabled=busy||page===1;$('libraryAdminNext').disabled=busy||!canNext;
  }
  function publishedLink(article){const link=$('libraryOpenPublished');link.hidden=article?.status!=='published'||api.portalSession===false;if(article?.id)link.href=K.lessonUrl(article.id);}
  function populate(article){
    editing=article;form.reset();fillCategories(form.elements.category_id);
    if(article){form.elements.category_id.value=article.category_id;fillGroups(article.group_id);for(const key of ['title','summary','body','position','status'])form.elements[key].value=article[key];}
    else{fillGroups();form.elements.position.value='10';}
    $('libraryEditorTitle').textContent=article?'Chỉnh sửa bài viết':'Soạn bài mới';$('libraryEditor').hidden=false;$('libraryPreview').hidden=true;$('libraryEditorState').textContent='';publishedLink(article);dirty=false;saveNonce=null;form.elements.title.focus();
    if(!form.elements.group_id.options.length)$('libraryEditorState').textContent='Thêm nhóm bài cho chuyên mục trước khi soạn bài.';
  }
  async function openArticle(identifier){
    const current=++sequence;setBusy(true);
    try{const response=await api.get('/api/v1/admin/knowledge/articles/'+encodeURIComponent(identifier));if(current===sequence)populate(response.article);}
    finally{setBusy(false);}
  }
  form.oninput=()=>{dirty=true;};
  form.elements.category_id.onchange=()=>{fillGroups();dirty=true;};
  $('libraryNewArticle').onclick=()=>{if(!busy&&canDiscard()){sequence++;populate(null);}};
  $('libraryCloseEditor').onclick=()=>{if(!busy&&canDiscard()){$('libraryEditor').hidden=true;sequence++;editing=null;dirty=false;}};
  $('libraryPreviewButton').onclick=()=>{
    $('libraryPreviewTitle').textContent=form.elements.title.value||'Tiêu đề bài';$('libraryPreviewSummary').textContent=form.elements.summary.value;$('libraryPreviewSummary').hidden=!form.elements.summary.value;
    K.renderBody($('libraryPreviewBody'),form.elements.body.value);$('libraryPreview').hidden=false;
  };
  root.querySelectorAll('[data-body-format]').forEach(button=>button.onclick=()=>{
    if(busy)return;const input=form.elements.body,start=input.selectionStart,end=input.selectionEnd,prefix=button.dataset.bodyFormat==='heading'?'## ':'- ';
    const selected=input.value.slice(start,end)||(prefix==='## '?'Tiêu đề nhỏ':'Ý cần trình bày');
    const before=start>0&&input.value[start-1]!=='\n'?'\n':'';
    input.setRangeText(before+selected.split('\n').map(line=>prefix+line).join('\n')+'\n',start,end,'select');input.focus();dirty=true;
  });
  form.onsubmit=async event=>{
    event.preventDefault();if(busy||!form.reportValidity())return;
    const payload={group_id:form.elements.group_id.value,title:form.elements.title.value.trim(),summary:form.elements.summary.value.trim(),body:form.elements.body.value.trim(),position:Number(form.elements.position.value),status:form.elements.status.value};
    if(editing)payload.expected_revision=editing.revision;
    else{const encoded=JSON.stringify(payload);if(saveNonce?.encoded!==encoded)saveNonce={encoded,key:window.crypto.randomUUID()};payload.client_key=saveNonce.key;}
    setBusy(true);$('libraryEditorState').textContent='';
    try{
      const response=editing?await api.api('PATCH','/api/v1/admin/knowledge/articles/'+encodeURIComponent(editing.id),payload):await api.post('/api/v1/admin/knowledge/articles',payload);
      editing=response.article;dirty=false;saveNonce=null;publishedLink(editing);$('libraryEditorTitle').textContent='Chỉnh sửa bài viết';
      await loadCatalog();await loadArticles();state.textContent=editing.status==='published'?'Đã đăng bài cho thành viên đọc.':'Đã lưu bản nháp. Thành viên chưa nhìn thấy bài này.';
    }catch(failure){error($('libraryEditorState'),failure);}finally{setBusy(false);$('libraryAdminPrevious').disabled=page===1;}
  };
  function composeStructure(kind,item){
    structureKind=kind;structureEditing=item||null;structureForm.reset();fillCategories(structureForm.elements.category_id);
    $('libraryStructureParentLabel').hidden=kind!=='group';structureForm.elements.category_id.required=kind==='group';
    for(const name of ['title','description','position'])structureForm.elements[name].value=item?item[name]:(name==='position'?'10':'');
    if(item?.category_id)structureForm.elements.category_id.value=item.category_id;
    $('libraryStructureFormTitle').textContent=(item?'Sửa ':'Thêm ')+(kind==='group'?'nhóm bài':'chuyên mục');$('libraryStructureState').textContent='';structureForm.hidden=false;structureForm.elements.title.focus();
  }
  $('libraryManageStructure').onclick=()=>{if(!busy)$('libraryStructure').hidden=!$('libraryStructure').hidden;};
  $('libraryNewCategory').onclick=()=>{if(!busy)composeStructure('category');};
  $('libraryNewGroup').onclick=()=>{if(!busy)composeStructure('group');};
  $('libraryCloseStructure').onclick=()=>{if(!busy)$('libraryStructure').hidden=true;};
  $('libraryCancelStructureEdit').onclick=()=>{if(!busy)structureForm.hidden=true;};
  structureForm.onsubmit=async event=>{
    event.preventDefault();if(busy||!structureForm.reportValidity())return;
    const payload={title:structureForm.elements.title.value.trim(),description:structureForm.elements.description.value.trim(),position:Number(structureForm.elements.position.value)};
    if(structureKind==='group')payload.category_id=structureForm.elements.category_id.value;
    if(structureEditing)payload.expected_revision=structureEditing.revision;
    const collection=structureKind==='group'?'groups':'categories';setBusy(true);$('libraryStructureState').textContent='';
    try{
      if(structureEditing)await api.api('PATCH','/api/v1/admin/knowledge/'+collection+'/'+encodeURIComponent(structureEditing.id),payload);else await api.post('/api/v1/admin/knowledge/'+collection,payload);
      await loadCatalog();await loadArticles();structureForm.hidden=true;state.textContent='Đã lưu chuyên mục / nhóm bài.';
    }catch(failure){error($('libraryStructureState'),failure);}finally{setBusy(false);}
  };
  filters.onsubmit=event=>{event.preventDefault();if(!busy){page=1;void loadArticles().catch(failure=>error(state,failure));}};
  $('libraryAdminPrevious').onclick=()=>{if(!busy&&page>1){page--;void loadArticles().catch(failure=>error(state,failure));}};
  $('libraryAdminNext').onclick=()=>{if(!busy){page++;void loadArticles().catch(failure=>error(state,failure));}};
  $('libraryAdminRefresh').onclick=async()=>{
    if(busy||!canDiscard())return;
    try{await loadCatalog();await loadArticles();if(editing)await openArticle(editing.id);else if(!$('libraryEditor').hidden)populate(null);state.textContent='Đã tải lại thư viện.';}catch(failure){error(state,failure);}
  };
  window.addEventListener('beforeunload',event=>{if(dirty){event.preventDefault();event.returnValue='';}});
  (async()=>{
    try{const user=await api.get('/api/v1/auth/me');if(user.role!=='ADMIN')throw new Error('Chỉ Admin được quản lý thư viện kiến thức.');await loadCatalog();await loadArticles();$('libraryAdminWorkspace').hidden=false;}
    catch(failure){error(state,failure);}
  })();
})();
