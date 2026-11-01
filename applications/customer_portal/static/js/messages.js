(function () {
  const root=document.querySelector('[data-communications="messages"]');
  if(!root)return;
  const api=window.BteAdmin||window.BtePortal;
  const $=id=>document.getElementById(id);
  const state=$("messagesState"), list=$("conversationList"), form=$("newConversationForm"), reply=$("messageReplyForm"), messages=$("conversationMessages");
  let user,selected=null,page=1,total=0,before=null,hasMore=false,sending=false,sequence=0,listSequence=0;
  const drafts=new Map(), keys=new Map();
  const when=value=>value?new Date(value).toLocaleString("vi-VN"):"";
  function node(tag,text,cls){const element=document.createElement(tag);if(text!==undefined)element.textContent=String(text);if(cls)element.className=cls;return element;}
  function nonce(){return window.crypto?.randomUUID?.()||Date.now().toString(36)+"-"+Math.random().toString(36).slice(2);}
  function key(name,payload){const encoded=JSON.stringify(payload),old=keys.get(name);if(old?.encoded===encoded)return old.key;const value=nonce();keys.set(name,{encoded,key:value});return value;}
  function setBusy(value){sending=value;form.querySelector('button[type="submit"]').disabled=value;reply.querySelector('button[type="submit"]').disabled=value;}
  async function summary(){
    try{const data=await api.get("/api/v1/communications/summary");document.querySelectorAll("[data-message-unread]").forEach(badge=>{const count=data.unread_messages||0;badge.textContent=count>99?"99+":String(count);badge.hidden=count===0;});}catch(_){}
  }
  async function loadList(){
    const current=++listSequence;
    const data=await api.get("/api/v1/communications/threads?page="+page);
    if(current!==listSequence)return;
    total=data.total;list.replaceChildren();
    $("conversationCount").textContent=total+" cuộc trao đổi";
    if(!data.items.length)list.append(node("p","Chưa có cuộc trao đổi. Chọn “Trao đổi mới” để gửi tin."));
    data.items.forEach(thread=>{
      const button=node("button",undefined,"comm-thread");button.type="button";button.setAttribute("aria-current",String(selected===thread.id));
      button.append(node("strong",thread.subject));
      if(user.role==="ADMIN")button.append(node("small",thread.owner.display_name+" (@"+thread.owner.username+")"));
      button.append(node("small",when(thread.updated_at)));
      if(thread.unread)button.append(node("span",thread.unread+" chưa đọc","comm-unread"));
      button.onclick=()=>{if(!sending)void open(thread.id).catch(showError);};list.append(button);
    });
    $("conversationsPrevious").disabled=page===1;
    $("conversationsNext").disabled=page*data.limit>=total;
  }
  function renderMessage(message){
    const card=node("article",undefined,"comm-message"+(message.sender_id===user.user_id?" own":""));
    const heading=node("strong",message.sender_name||message.sender_username);
    if(message.sender_is_admin)heading.append(node("span","Admin","comm-admin-label"));
    card.append(heading,node("p",message.body),node("small",when(message.created_at)));return card;
  }
  async function open(identifier,older=false){
    if(sending)return;
    const previous=selected;
    if(!older&&previous!==identifier){if(previous)drafts.set(previous,reply.elements.message.value);reply.elements.message.value=drafts.get(identifier)||"";}
    selected=identifier;const current=++sequence;
    if(!older){reply.hidden=true;messages.replaceChildren(node("p","Đang tải tin nhắn…"));}
    const data=await api.get("/api/v1/communications/threads/"+encodeURIComponent(identifier)+"/messages"+(older&&before?"?before="+before:""));
    if(current!==sequence||selected!==identifier)return;
    const oldHeight=messages.scrollHeight;
    const fragment=document.createDocumentFragment();data.messages.forEach(message=>fragment.append(renderMessage(message)));
    if(older)messages.prepend(fragment);else messages.replaceChildren(fragment);
    before=data.before;hasMore=data.has_more;$("loadEarlierMessages").hidden=!hasMore;
    $("conversationTitle").textContent=data.thread.subject;
    $("conversationOwner").textContent=user.role==="ADMIN"?data.thread.owner.display_name+" (@"+data.thread.owner.username+")":"Trao đổi riêng với Admin";
    reply.hidden=false;$("messageReplyState").textContent="";
    messages.scrollTop=older?messages.scrollHeight-oldHeight:messages.scrollHeight;
    if(data.messages.length)await api.post("/api/v1/communications/threads/"+encodeURIComponent(identifier)+"/read",{last_message_id:data.messages[data.messages.length-1].id});
    await loadList();await summary();
  }
  function showError(error){state.textContent=error.message||"Chưa tải được tin nhắn.";}
  $("newConversation").onclick=()=>{form.hidden=false;$("newConversationState").textContent="";form.elements.subject.focus();};
  $("cancelConversation").onclick=()=>{if(!sending)form.hidden=true;};
  form.onsubmit=async event=>{
    event.preventDefault();if(sending||!form.reportValidity())return;
    const payload={subject:form.elements.subject.value.trim(),message:form.elements.message.value.trim()};
    if(user.role==="ADMIN")payload.recipient_user_id=form.elements.recipient_user_id.value;
    payload.client_key=key("new",payload);setBusy(true);$("newConversationState").textContent="Đang gửi…";
    try{const data=await api.post("/api/v1/communications/threads",payload);form.reset();keys.delete("new");form.hidden=true;state.textContent="Đã gửi tin nhắn và lưu lịch sử trao đổi.";setBusy(false);await open(data.thread.id);}
    catch(error){$("newConversationState").textContent=error.message;}
    finally{setBusy(false);}
  };
  reply.onsubmit=async event=>{
    event.preventDefault();if(sending||!selected||!reply.reportValidity())return;
    const identifier=selected,payload={message:reply.elements.message.value.trim()};payload.client_key=key("reply:"+identifier,payload);
    setBusy(true);$("messageReplyState").textContent="Đang gửi…";
    try{await api.post("/api/v1/communications/threads/"+encodeURIComponent(identifier)+"/messages",payload);keys.delete("reply:"+identifier);drafts.delete(identifier);reply.elements.message.value="";setBusy(false);await open(identifier);state.textContent="Đã gửi trả lời.";}
    catch(error){$("messageReplyState").textContent=error.message;}
    finally{setBusy(false);}
  };
  $("refreshConversations").onclick=()=>{if(sending)return;void (selected?open(selected):loadList()).catch(showError);};
  $("loadEarlierMessages").onclick=()=>{if(selected&&!sending)void open(selected,true).catch(showError);};
  $("conversationsPrevious").onclick=()=>{if(page>1&&!sending){page--;void loadList().catch(showError);}};
  $("conversationsNext").onclick=()=>{if(!sending){page++;void loadList().catch(showError);}};
  (async()=>{
    try{
      user=await api.get("/api/v1/auth/me");
      if(user.role==="ADMIN"){
        $("messagesTitle").textContent="Tin nhắn thành viên";$("recipientLabel").hidden=false;form.elements.recipient_user_id.required=true;
        const data=await api.get("/api/v1/communications/recipients");data.items.forEach(person=>{const option=node("option",person.display_name+" (@"+person.username+")");option.value=person.id;form.elements.recipient_user_id.append(option);});
      }
      $("messagesWorkspace").hidden=false;await loadList();await summary();
      const wanted=new URLSearchParams(location.search).get("thread");if(wanted)await open(wanted);
    }catch(error){showError(error);}
  })();
})();
