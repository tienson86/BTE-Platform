(function () {
  const root=document.querySelector('[data-communications="community"]');if(!root)return;
  const api=window.BteAdmin||window.BtePortal,$=id=>document.getElementById(id);
  const state=$("knowledgeState"),topicForm=$("knowledgeTopicForm"),commentForm=$("knowledgeCommentForm"),moderationForm=$("knowledgeModerationForm");
  const statuses={pending:"Chờ Admin duyệt",approved:"Đã duyệt hiển thị",rejected:"Chưa được chấp thuận",deleted:"Chủ đề đã được gỡ"};
  const scopeTitles={feed:"Chủ đề đã duyệt",mine:"Chủ đề của tôi",pending:"Chờ Admin duyệt",all:"Tất cả chủ đề"};
  let user,scope="feed",page=1,topic=null,editing=null,commentPage=1,busy=false,detailSequence=0,listSequence=0;
  const keys=new Map();
  const when=value=>value?new Date(value).toLocaleString("vi-VN"):"";
  function node(tag,text,cls){const element=document.createElement(tag);if(text!==undefined)element.textContent=String(text);if(cls)element.className=cls;return element;}
  function key(name,payload){const encoded=JSON.stringify(payload),old=keys.get(name);if(old?.encoded===encoded)return old.value;const value=window.crypto?.randomUUID?.()||Date.now().toString(36)+"-"+Math.random().toString(36).slice(2);keys.set(name,{encoded,value});return value;}
  function showError(error){state.textContent=error.message||"Chưa hoàn tất thao tác. Vui lòng thử lại.";}
  function busyUI(value){busy=value;root.querySelectorAll('form button[type="submit"]').forEach(button=>button.disabled=value);}
  function updateTabs(){root.querySelectorAll("[data-topic-scope]").forEach(button=>button.setAttribute("aria-pressed",String(button.dataset.topicScope===scope)));$("knowledgeListTitle").textContent=scopeTitles[scope];}
  async function loadList(){
    const current=++listSequence;state.textContent="";updateTabs();
    const data=await api.get("/api/v1/community/topics?scope="+scope+"&page="+page);
    if(current!==listSequence)return;
    const list=$("knowledgeTopics");list.replaceChildren();$("knowledgeTopicCount").textContent=data.total+" chủ đề";
    if(!data.items.length)list.append(node("p",scope==="feed"?"Chưa có chủ đề đã được duyệt. Bạn có thể tạo câu hỏi để Admin xem xét.":"Chưa có chủ đề trong nhóm này."));
    data.items.forEach(item=>{
      const button=node("button",undefined,"knowledge-topic");button.type="button";button.append(node("strong",item.title));
      button.append(node("small",item.author_name+" (@"+item.author_username+")"+(item.author_is_admin?" · Admin":"")+" · "+when(item.created_at)));
      button.append(node("small",statuses[item.status]+" · "+item.comment_count+" bình luận"));
      button.onclick=()=>{if(!busy)void open(item.id).catch(showError);};list.append(button);
    });
    $("knowledgePrevious").disabled=page===1;$("knowledgeNext").disabled=page*data.limit>=data.total;
  }
  function renderComment(item){
    const article=node("article",undefined,"knowledge-comment"+(item.deleted?" deleted":""));
    if(item.deleted){article.append(node("p","Bình luận đã được xóa."));return article;}
    const author=node("strong",item.author_name+" (@"+item.author_username+")");if(item.author_is_admin)author.append(node("span","Admin","comm-admin-label"));
    article.append(author,node("p",when(item.created_at)+(item.revision>1?" · Đã chỉnh sửa":""),"muted"),node("div",item.body,"comm-body"));
    const actions=node("div",undefined,"comm-actions");
    if(item.can_edit){
      const edit=node("button","Sửa bình luận của tôi");edit.type="button";
      edit.onclick=()=>{
        if(busy||article.querySelector("form"))return;
        const form=node("form",undefined,"comm-form"),label=node("label","Nội dung chỉnh sửa"),input=node("textarea"),save=node("button","Lưu chỉnh sửa"),cancel=node("button","Hủy"),notice=node("p");
        input.value=item.body;input.maxLength=5000;input.required=true;input.rows=4;label.append(input);save.type="submit";cancel.type="button";cancel.className="secondary";notice.setAttribute("role","alert");
        const buttons=node("div",undefined,"comm-actions");buttons.append(save,cancel);form.append(label,buttons,notice);article.append(form);input.focus();
        cancel.onclick=()=>{if(!busy)form.remove();};
        form.onsubmit=async event=>{
          event.preventDefault();if(busy||!form.reportValidity())return;busyUI(true);
          try{await api.api("PATCH","/api/v1/community/comments/"+encodeURIComponent(item.id),{body:input.value.trim(),expected_revision:item.revision});await loadComments(false);state.textContent="Đã sửa bình luận của bạn.";}
          catch(error){notice.textContent=error.message;}finally{busyUI(false);}
        };
      };actions.append(edit);
    }
    if(item.can_delete){const remove=node("button",item.can_edit?"Xóa bình luận của tôi":"Gỡ bình luận");remove.type="button";remove.className="secondary";remove.onclick=async()=>{
      if(busy)return;busyUI(true);
      try{await api.api("DELETE","/api/v1/community/comments/"+encodeURIComponent(item.id),{expected_revision:item.revision});await loadComments(false);state.textContent="Đã xóa nội dung bình luận.";}catch(error){showError(error);}finally{busyUI(false);}
    };actions.append(remove);}
    article.append(actions);return article;
  }
  async function loadComments(append){
    if(!topic)return;const identifier=topic.id,revision=detailSequence;
    if(!append)commentPage=1;
    const data=await api.get("/api/v1/community/topics/"+encodeURIComponent(identifier)+"/comments?page="+commentPage);
    if(topic?.id!==identifier||revision!==detailSequence)return;
    const list=$("knowledgeComments");if(!append)list.replaceChildren();
    data.items.forEach(item=>list.append(renderComment(item)));
    if(data.total===0)list.append(node("p",topic.status==="approved"?"Chưa có bình luận. Hãy mở đầu cuộc trao đổi.":"Chủ đề sẽ mở bình luận sau khi được duyệt."));
    $("moreKnowledgeComments").hidden=commentPage*data.limit>=data.total;
  }
  async function open(identifier){
    const current=++detailSequence;state.textContent="";const data=await api.get("/api/v1/community/topics/"+encodeURIComponent(identifier));
    if(current!==detailSequence)return;
    topic=data.topic;$("knowledgeTopicList").hidden=true;$("knowledgeDetail").hidden=false;topicForm.hidden=true;
    $("knowledgeDetailTitle").textContent=topic.title;
    $("knowledgeDetailMeta").textContent=topic.author_name+" (@"+topic.author_username+")"+(topic.author_is_admin?" · Admin":"")+" · "+when(topic.created_at);
    $("knowledgeDetailBody").textContent=topic.body;$("knowledgeDetailStatus").textContent=statuses[topic.status];
    $("knowledgeModerationNote").textContent=topic.moderation_note?"Ghi chú duyệt: "+topic.moderation_note:"";
    $("editKnowledgeTopic").hidden=!topic.can_edit;$("removeKnowledgeTopic").hidden=!topic.can_delete;
    moderationForm.hidden=!topic.can_moderate;moderationForm.elements.note.value="";
    commentForm.hidden=topic.status!=="approved";$("knowledgeCommentState").textContent="";
    await loadComments(false);
  }
  function compose(item){
    editing=item;topicForm.elements.title.value=item?.title||"";topicForm.elements.body.value=item?.body||"";
    $("knowledgeFormTitle").textContent=item?"Sửa chủ đề và gửi duyệt lại":"Tạo chủ đề";
    $("knowledgeFormState").textContent="";topicForm.hidden=false;topicForm.elements.title.focus();
  }
  $("newKnowledgeTopic").onclick=()=>{if(!busy)compose(null);};
  $("editKnowledgeTopic").onclick=()=>{if(!busy&&topic)compose(topic);};
  $("cancelKnowledgeTopic").onclick=()=>{if(!busy)topicForm.hidden=true;};
  topicForm.onsubmit=async event=>{
    event.preventDefault();if(busy||!topicForm.reportValidity())return;
    const payload={title:topicForm.elements.title.value.trim(),body:topicForm.elements.body.value.trim()};
    if(editing)payload.expected_revision=editing.revision;else payload.client_key=key("topic",payload);
    busyUI(true);
    try{
      const response=editing?await api.api("PATCH","/api/v1/community/topics/"+encodeURIComponent(editing.id),payload):await api.post("/api/v1/community/topics",payload);
      keys.delete("topic");topicForm.hidden=true;topicForm.reset();editing=null;scope="mine";page=1;
      await loadList();await open(response.topic.id);state.textContent="Đã gửi chủ đề. Chủ đề đang chờ Admin duyệt trước khi hiển thị chung.";
    }catch(error){$("knowledgeFormState").textContent=error.message;}finally{busyUI(false);}
  };
  moderationForm.onsubmit=async event=>{
    event.preventDefault();const decision=event.submitter?.value;
    if(busy||!topic||!["approve","reject"].includes(decision))return;busyUI(true);
    try{const response=await api.post("/api/v1/community/topics/"+encodeURIComponent(topic.id)+"/moderate",{decision,expected_revision:topic.revision,note:moderationForm.elements.note.value.trim()});await loadList();await open(response.topic.id);state.textContent=decision==="approve"?"Đã duyệt chủ đề để các thành viên cùng trao đổi.":"Đã cập nhật kết quả duyệt chủ đề.";}
    catch(error){showError(error);}finally{busyUI(false);}
  };
  $("removeKnowledgeTopic").onclick=async()=>{
    if(busy||!topic)return;busyUI(true);
    try{await api.api("DELETE","/api/v1/community/topics/"+encodeURIComponent(topic.id),{expected_revision:topic.revision});topic=null;detailSequence++;$("knowledgeDetail").hidden=true;$("knowledgeTopicList").hidden=false;await loadList();state.textContent="Đã gỡ chủ đề khỏi mục trao đổi.";}
    catch(error){showError(error);}finally{busyUI(false);}
  };
  commentForm.onsubmit=async event=>{
    event.preventDefault();if(busy||!topic||!commentForm.reportValidity())return;
    const payload={body:commentForm.elements.body.value.trim()};payload.client_key=key("comment:"+topic.id,payload);busyUI(true);
    try{await api.post("/api/v1/community/topics/"+encodeURIComponent(topic.id)+"/comments",payload);keys.delete("comment:"+topic.id);commentForm.reset();await loadComments(false);state.textContent="Đã gửi bình luận.";}
    catch(error){$("knowledgeCommentState").textContent=error.message;}finally{busyUI(false);}
  };
  $("moreKnowledgeComments").onclick=()=>{if(!busy){commentPage++;void loadComments(true).catch(showError);}};
  $("backToKnowledge").onclick=()=>{if(!busy){topic=null;detailSequence++;$("knowledgeDetail").hidden=true;$("knowledgeTopicList").hidden=false;topicForm.hidden=true;void loadList().catch(showError);}};
  root.querySelectorAll("[data-topic-scope]").forEach(button=>button.onclick=()=>{if(busy)return;scope=button.dataset.topicScope;page=1;topic=null;detailSequence++;$("knowledgeDetail").hidden=true;$("knowledgeTopicList").hidden=false;void loadList().catch(showError);});
  $("knowledgePrevious").onclick=()=>{if(page>1&&!busy){page--;void loadList().catch(showError);}};
  $("knowledgeNext").onclick=()=>{if(!busy){page++;void loadList().catch(showError);}};
  $("refreshKnowledge").onclick=()=>{if(!busy)void(topic?open(topic.id):loadList()).catch(showError);};
  (async()=>{
    try{
      user=await api.get("/api/v1/auth/me");
      if(user.role!=="ADMIN"&&!user.member_access){state.replaceChildren(node("span","Mục này dành cho thành viên còn quyền sử dụng. "));const link=node("a","Xem trạng thái thành viên");link.href="/membership";state.append(link);return;}
      root.querySelectorAll("[data-moderator-only]").forEach(element=>element.hidden=user.role!=="ADMIN");
      if(user.role==="ADMIN"&&root.dataset.adminMode==="true")scope="pending";
      $("knowledgeWorkspace").hidden=false;await loadList();
      const wanted=new URLSearchParams(location.search).get("topic");if(wanted)await open(wanted);
    }catch(error){showError(error);}
  })();
})();
