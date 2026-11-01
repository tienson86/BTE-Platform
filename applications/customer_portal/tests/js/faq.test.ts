import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {afterEach,expect,it,vi} from 'vitest';
const root=resolve(__dirname,'../..');
const read=(path:string)=>readFileSync(resolve(root,path),'utf8');
const script=(name:string)=>read('static/js/'+name+'.js');
const shared=read('templates/community.html').split('<!-- COMMUNITY_PANEL_START -->')[1].split('<!-- COMMUNITY_PANEL_END -->')[0];
const categories=[{id:'co-ban',title:'Phong thủy cơ bản'},{id:'nha-o',title:'Phong thủy nhà ở'}];
const initial={id:'q1',title:'Câu hỏi thử',body:'<script>bad()</script>',category_id:'co-ban',category_title:'Phong thủy cơ bản',author_name:'Thành viên',author_username:'member',author_id:'m1',status:'approved',revision:2,comment_count:0,can_edit:true,can_delete:false,can_moderate:false};
const form=()=>document.getElementById('knowledgeTopicForm') as HTMLFormElement;
function mount(admin=false){
  history.replaceState(null,'',admin?'/admin/community':'/knowledge?category=co-ban');
  document.body.innerHTML=admin?shared.replace('data-admin-mode="false"','data-admin-mode="true"'):read('templates/knowledge.html').replace('{{CATEGORY_COMMUNITY}}',shared).replace(/<script[\s\S]*?<\/script>/g,'');
  let question={...initial};
  const api={get:vi.fn(async(path:string)=>{
    if(path.endsWith('/auth/me'))return {user_id:'m1',role:admin?'ADMIN':'CUSTOMER',member_access:true};
    if(path.endsWith('/community/categories'))return {items:categories};
    if(path.includes('/knowledge/categories/'))return {category:{id:'co-ban',title:'Phong thủy cơ bản',description:'Nhập môn',article_count:1,groups:[{id:'co-ban-4',title:'Câu hỏi thường gặp',description:'',is_faq:true,articles:[{id:'lesson1',title:'Bài giải đáp cũ',category_title:'Phong thủy cơ bản',group_title:'Câu hỏi thường gặp'}]}]}};
    if(path.includes('/topics?'))return {items:[question],total:1,limit:30};
    if(path.includes('/comments?'))return {items:[],total:0,limit:50};
    if(path.endsWith('/topics/q1'))return {topic:question};
    throw new Error(path);
  }),post:vi.fn(async(path:string,payload:any)=>{
    if(path.endsWith('/moderate'))question={...question,status:'approved',revision:question.revision+1};
    else if(path.endsWith('/topics'))question={...question,...payload,status:'pending',revision:1};
    return {topic:question};
  }),api:vi.fn(async()=>({topic:question}))};
  vi.stubGlobal(admin?'BteAdmin':'BtePortal',api);new Function(script('knowledge_common'))();new Function(script('community'))();
  if(!admin)new Function(script('knowledge'))();return api;
}
async function expand(){
  await vi.waitFor(()=>expect(document.getElementById('libraryQuestions')).not.toBeNull());
  const group=document.getElementById('libraryQuestions') as HTMLDetailsElement;group.open=true;group.dispatchEvent(new Event('toggle'));
  await vi.waitFor(()=>expect(document.querySelector('.knowledge-topic')).not.toBeNull());return group;
}
afterEach(()=>{document.body.innerHTML='';vi.unstubAllGlobals();vi.restoreAllMocks();});

it('opens questions inside the FAQ group and preserves authored answers',async()=>{
  const api=mount();const group=await expand();
  expect(group.textContent).toContain('Bài giải đáp cũ');expect(group.textContent).toContain('Hỏi đáp cộng đồng');
  expect(api.get).toHaveBeenCalledWith('/api/v1/community/topics?scope=feed&page=1&category_id=co-ban');
  expect(document.getElementById('knowledgeCategoryFilterLabel')?.hidden).toBe(true);
});

it('sends the fixed category and shows pending status without opening comments',async()=>{
  const api=mount();await expand();(document.getElementById('newKnowledgeTopic') as HTMLElement).click();
  form().elements.namedItem('title').value='Câu hỏi của tôi';form().elements.namedItem('body').value='Xin giải đáp';
  form().dispatchEvent(new Event('submit',{cancelable:true}));
  await vi.waitFor(()=>expect(api.post).toHaveBeenCalledWith('/api/v1/community/topics',expect.objectContaining({category_id:'co-ban',title:'Câu hỏi của tôi'})));
  await vi.waitFor(()=>expect(document.getElementById('knowledgeState')?.textContent).toContain('chờ Admin duyệt'));
  expect(document.getElementById('knowledgeCommentForm')?.hidden).toBe(true);
});

it('opens the approved discussion in place and posts an answer to the same topic',async()=>{
  const api=mount();await expand();(document.querySelector('.knowledge-topic') as HTMLElement).click();
  await vi.waitFor(()=>expect(document.getElementById('knowledgeCommentForm')?.hidden).toBe(false));
  expect(document.getElementById('knowledgeDetailBody')?.querySelector('script')).toBeNull();
  const reply=document.getElementById('knowledgeCommentForm') as HTMLFormElement;reply.elements.namedItem('body').value='Cộng đồng trả lời';reply.dispatchEvent(new Event('submit',{cancelable:true}));
  await vi.waitFor(()=>expect(api.post).toHaveBeenCalledWith('/api/v1/community/topics/q1/comments',expect.objectContaining({body:'Cộng đồng trả lời'})));
  await vi.waitFor(()=>expect(document.getElementById('knowledgeState')?.textContent).toContain('Đã gửi bình luận'));
});

it('filters the shared Admin approval queue by category',async()=>{
  const api=mount(true);await vi.waitFor(()=>expect(document.querySelector('.knowledge-topic')).not.toBeNull());
  const select=document.getElementById('knowledgeCategoryFilter') as HTMLSelectElement;select.value='co-ban';select.dispatchEvent(new Event('change'));
  await vi.waitFor(()=>expect(api.get).toHaveBeenCalledWith('/api/v1/community/topics?scope=pending&page=1&category_id=co-ban'));
  expect(document.querySelector('.knowledge-topic')?.textContent).toContain('Phong thủy cơ bản');
});
