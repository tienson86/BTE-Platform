(function(){
  const root=document.querySelector('[data-knowledge="reader"]');if(!root)return;
  const api=window.BtePortal,K=window.BteKnowledge,$=id=>document.getElementById(id),state=$('libraryState');
  if(location.pathname.startsWith('/knowledge/lesson/'))root.classList.add('knowledge-reading-page');
  const params=new URLSearchParams(location.search),search=$('librarySearch');
  search.elements.q.value=(params.get('q')||'').slice(0,120);
  search.onsubmit=event=>{event.preventDefault();const q=search.elements.q.value.trim();location.href=q?'/knowledge?q='+encodeURIComponent(q):'/knowledge';};
  function link(text,url,cls){const item=K.node('a',text,cls);item.href=url;return item;}
  function breadcrumbs(parts){const list=$('libraryBreadcrumbs');list.replaceChildren(link('Kiến thức phong thủy','/knowledge'));parts.forEach(part=>{list.append(K.node('span','›'));list.append(part.url?link(part.text,part.url):K.node('span',part.text));});}
  function show(id){$('libraryWorkspace').hidden=false;$(id).hidden=false;state.textContent='';}
  async function home(){
    const data=await api.get('/api/v1/knowledge/catalog');breadcrumbs([]);
    data.categories.forEach((category,index)=>{
      const card=link('',K.categoryUrl(category.id),'library-category-card');card.append(K.node('span',String(index+1).padStart(2,'0'),'library-card-number'),K.node('h3',category.title),K.node('p',category.description),K.node('small',category.groups.length+' nhóm bài · '+category.article_count+' bài đã đăng'),K.node('span','Khám phá chuyên mục →','library-card-open'));$('libraryCategories').append(card);
    });
    if(!data.categories.length)$('libraryCategories').append(K.node('p','Các chuyên mục đang được chuẩn bị.'));
    if(!data.latest.length)$('libraryLatest').append(K.node('p','Chưa có bài mới. Nội dung sẽ được bổ sung vào từng chuyên mục.','muted'));
    data.latest.forEach(article=>$('libraryLatest').append(K.articleCard(article)));show('libraryHome');
  }
  async function category(identifier){
    const data=await api.get('/api/v1/knowledge/categories/'+encodeURIComponent(identifier)),item=data.category;
    breadcrumbs([{text:item.title}]);$('libraryCategoryTitle').textContent=item.title;$('libraryCategoryDescription').textContent=item.description;$('libraryCategoryCount').textContent=item.groups.length+' nhóm bài · '+item.article_count+' bài đã đăng';
    item.groups.forEach((group,index)=>{
      const details=K.node('details',undefined,'library-group'),summary=K.node('summary',(index+1)+'. '+group.title),content=K.node('div',undefined,'library-group-content');
      summary.append(K.node('small',group.articles.length+' bài'));details.append(summary,content);
      if(group.description)content.append(K.node('p',group.description,'muted'));
      if(!group.articles.length)content.append(K.node('p','Nhóm bài này đang được biên soạn.','muted'));
      group.articles.forEach(article=>content.append(K.articleCard(article)));$('libraryGroups').append(details);
    });show('libraryCategory');
  }
  async function results(query){
    const page=Math.max(1,Math.min(100000,Number.parseInt(params.get('page')||'1',10)||1));
    const data=await api.get('/api/v1/knowledge/search?q='+encodeURIComponent(query)+'&page='+page);
    breadcrumbs([{text:'Tìm kiếm'}]);$('libraryResultsTitle').textContent='Kết quả cho “'+query+'”';$('libraryResultsCount').textContent=data.total+' bài phù hợp';
    data.items.forEach(item=>$('libraryResultsList').append(K.articleCard(item)));
    if(!data.items.length)$('libraryResultsList').append(K.node('p','Chưa tìm thấy bài phù hợp. Bạn thử dùng từ khóa ngắn hơn hoặc mở một chuyên mục.'));
    if(page>1)$('librarySearchPages').append(link('← Trang trước','/knowledge?q='+encodeURIComponent(query)+'&page='+(page-1)));
    if(page*data.limit<data.total)$('librarySearchPages').append(link('Trang sau →','/knowledge?q='+encodeURIComponent(query)+'&page='+(page+1)));
    show('libraryResults');
  }
  async function lesson(identifier){
    const data=await api.get('/api/v1/knowledge/articles/'+encodeURIComponent(identifier)),article=data.article;
    breadcrumbs([{text:article.category_title,url:K.categoryUrl(article.category_id)},{text:article.group_title}]);
    $('libraryLessonTitle').textContent=article.title;$('libraryLessonGroup').textContent=article.group_title;
    $('libraryLessonMeta').textContent='Biên soạn: '+article.author_name+' · Cập nhật '+K.date(article.updated_at);
    $('libraryLessonSummary').textContent=article.summary;$('libraryLessonSummary').hidden=!article.summary;
    K.renderBody($('libraryLessonBody'),article.body);
    if(data.previous){const previous=link('',K.lessonUrl(data.previous.id),'library-article-card');previous.append(K.node('small','← Bài trước'),K.node('strong',data.previous.title));$('libraryLessonNavigation').append(previous);}
    if(data.next){const next=link('',K.lessonUrl(data.next.id),'library-article-card library-next-lesson');next.append(K.node('small','Bài tiếp theo →'),K.node('strong',data.next.title));$('libraryLessonNavigation').append(next);}
    show('libraryLesson');
  }
  (async()=>{
    state.textContent='Đang mở thư viện…';
    try{
      const user=await api.get('/api/v1/auth/me');
      if(user.role!=='ADMIN'&&!user.member_access)throw new Error('Mục này dành cho thành viên còn quyền sử dụng. Vui lòng xem trạng thái thành viên.');
      const prefix='/knowledge/lesson/';
      if(location.pathname.startsWith(prefix))await lesson(decodeURIComponent(location.pathname.slice(prefix.length)));
      else if(params.get('q')?.trim())await results(params.get('q').trim().slice(0,120));
      else if(params.get('category'))await category(params.get('category'));
      else await home();
    }catch(error){state.replaceChildren(K.node('span',error.message||'Chưa mở được nội dung. '),K.node('span',' '),link('Về thư viện','/knowledge'));}
  })();
})();
