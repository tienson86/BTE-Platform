import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {afterEach,expect,it,vi} from 'vitest';
const root=resolve(__dirname,'../..');
const html=(name:string)=>readFileSync(resolve(root,'templates',name+'.html'),'utf8').replace(/<script[\s\S]*?<\/script>/g,'');
const source=(name:string)=>readFileSync(resolve(root,'static/js',name+'.js'),'utf8');
const member={user_id:'m1',username:'member',role:'CUSTOMER',member_access:true};
const topic={id:'t1',title:'<img src=x onerror=alert(1)>',body:'<script>evil()</script>',author_name:'Member',author_username:'member',author_id:'m1',author_is_admin:false,created_at:'2026-11-01',revision:2,status:'approved',comment_count:1,can_edit:true,can_delete:false,can_moderate:false};
function mount(name:string,user:any=member,overrides:any={}){
  history.replaceState(null,'','/'+name);document.body.innerHTML=html(name);
  const api={
    get:vi.fn(async(path:string)=>{
      if(path.endsWith('/auth/me'))return user;
      if(path.endsWith('/summary'))return {unread_messages:1};
      if(path.endsWith('/recipients'))return {items:[{id:'m1',username:'member',display_name:'Member'}]};
      if(path.includes('/communications/threads?'))return {items:[{id:'c1',subject:'<b>Private</b>',owner:{display_name:'Member',username:'member'},unread:1}],total:1,limit:30};
      if(path.includes('/c1/messages'))return {thread:{id:'c1',subject:'<b>Private</b>',owner:{display_name:'Member',username:'member'}},messages:[{id:7,sender_id:'admin',sender_name:'Admin',sender_is_admin:true,body:'<img src=x onerror=evil()>'}],has_more:false,before:7};
      if(path.includes('/topics?'))return {items:[topic],total:1,limit:30};
      if(path.includes('/comments?'))return {items:[{id:'r1',body:'<img src=x>',author_name:'Member',author_username:'member',revision:3,can_edit:true,can_delete:true}],total:1,limit:50};
      if(path.endsWith('/topics/t1'))return {topic};
      throw new Error(path);
    }),
    post:vi.fn(async()=>({topic:{...topic,status:'pending'},thread:{id:'c1'}})),
    api:vi.fn(async()=>({comment:{}})),...overrides
  };
  vi.stubGlobal('BtePortal',api);new Function(source(name))();return api;
}
const click=(id:string)=>(document.getElementById(id) as HTMLElement).click();
const form=(id:string)=>document.getElementById(id) as HTMLFormElement;
const send=(id:string)=>form(id).dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}));
afterEach(()=>{document.body.innerHTML='';vi.unstubAllGlobals();vi.restoreAllMocks();});

it('renders private history as plain text and marks only the selected history read',async()=>{
  const api=mount('messages');
  await vi.waitFor(()=>expect(document.querySelector('.comm-thread')).not.toBeNull());
  (document.querySelector('.comm-thread') as HTMLElement).click();
  await vi.waitFor(()=>expect(document.querySelector('.comm-message')).not.toBeNull());
  expect(document.querySelector('#conversationMessages img')).toBeNull();
  expect(document.getElementById('conversationMessages')?.textContent).toContain('<img');
  await vi.waitFor(()=>expect(api.post).toHaveBeenCalledWith('/api/v1/communications/threads/c1/read',{last_message_id:7}));
  expect(document.getElementById('recipientLabel')?.hidden).toBe(true);
});

it('lets expired members read private support but blocks the knowledge area',async()=>{
  mount('messages',{...member,member_access:false});
  await vi.waitFor(()=>expect(document.getElementById('messagesWorkspace')?.hidden).toBe(false));
  document.body.innerHTML='';mount('community',{...member,member_access:false});
  await vi.waitFor(()=>expect(document.getElementById('knowledgeState')?.textContent).toContain('còn quyền sử dụng'));
  expect(document.getElementById('knowledgeWorkspace')?.hidden).toBe(true);
});

it('guards duplicate sends and retries with the same client key after failure',async()=>{
  let reject:(value:any)=>void=()=>{};
  const pending=new Promise((_,bad)=>reject=bad);
  const post=vi.fn().mockReturnValueOnce(pending).mockRejectedValue(new Error('Try again'));
  mount('messages',member,{post});
  await vi.waitFor(()=>expect(document.querySelector('.comm-thread')).not.toBeNull());
  click('newConversation');form('newConversationForm').elements.namedItem('subject').value='Support';
  form('newConversationForm').elements.namedItem('message').value='Help';
  send('newConversationForm');send('newConversationForm');
  expect(post).toHaveBeenCalledTimes(1);const key=post.mock.calls[0][1].client_key;
  reject(new Error('Try again'));await vi.waitFor(()=>expect(document.getElementById('newConversationState')?.textContent).toBe('Try again'));
  send('newConversationForm');await vi.waitFor(()=>expect(post).toHaveBeenCalledTimes(2));
  expect(post.mock.calls[1][1].client_key).toBe(key);
});

it('shows topic and comment text safely and sends edits with revision protection',async()=>{
  const api=mount('community');await vi.waitFor(()=>expect(document.querySelector('.knowledge-topic')).not.toBeNull());
  (document.querySelector('.knowledge-topic') as HTMLElement).click();
  await vi.waitFor(()=>expect(document.querySelector('.knowledge-comment')).not.toBeNull());
  expect(document.querySelector('#knowledgeDetail img')).toBeNull();
  expect(document.getElementById('knowledgeDetailBody')?.textContent).toBe('<script>evil()</script>');
  expect(form('knowledgeModerationForm').hidden).toBe(true);
  const edit=[...document.querySelectorAll('.knowledge-comment button')].find(el=>el.textContent==='Sửa bình luận của tôi') as HTMLElement;
  edit.click();const inline=document.querySelector('.knowledge-comment form') as HTMLFormElement;
  (inline.querySelector('textarea') as HTMLTextAreaElement).value='Edited';inline.dispatchEvent(new Event('submit',{cancelable:true}));
  await vi.waitFor(()=>expect(api.api).toHaveBeenCalledWith('PATCH','/api/v1/community/comments/r1',{body:'Edited',expected_revision:3}));
});

it('only submits moderation on an explicit approve or reject action',async()=>{
  const original={...topic};topic.can_moderate=true;topic.can_delete=true;topic.status='pending';
  const api=mount('community',{...member,role:'ADMIN'});
  await vi.waitFor(()=>expect(document.querySelector('.knowledge-topic')).not.toBeNull());
  (document.querySelector('.knowledge-topic') as HTMLElement).click();
  await vi.waitFor(()=>expect(form('knowledgeModerationForm').hidden).toBe(false));
  send('knowledgeModerationForm');expect(api.post).not.toHaveBeenCalled();
  const approve=form('knowledgeModerationForm').querySelector('[value="approve"]') as HTMLButtonElement;
  form('knowledgeModerationForm').dispatchEvent(new SubmitEvent('submit',{cancelable:true,submitter:approve}));
  await vi.waitFor(()=>expect(api.post).toHaveBeenCalledWith('/api/v1/community/topics/t1/moderate',{decision:'approve',expected_revision:2,note:''}));
  Object.assign(topic,original);
});
