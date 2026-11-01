import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {afterEach,expect,it,vi} from 'vitest';
const root=resolve(__dirname,'../..');
const script=(name:string)=>readFileSync(resolve(root,'static/js',name+'.js'),'utf8');
const html=(name:string)=>readFileSync(resolve(root,'templates',name+'.html'),'utf8').replace(/<script[\s\S]*?<\/script>/g,'');
const member={role:'CUSTOMER',member_access:true};
const article={id:'a1',category_id:'c1',category_title:'Chuyên mục',group_id:'g1',group_title:'Nhập môn',title:'<img src=x onerror=evil()>',summary:'Giới thiệu',body:'## Phần đầu\n\n<script>evil()</script>\n\n- Ý một\n- Ý hai',author_name:'Admin',status:'draft',revision:2,position:10};
const categories=[{id:'c1',title:'Phương pháp tính ngày giờ',description:'Từ nền tảng đến thực hành',position:10,revision:1,article_count:1,groups:[{id:'g1',category_id:'c1',title:'Nhập môn',description:'',position:10,revision:1,articles:[article]}]}];
function mount(path='/knowledge',admin=false,overrides:any={}){
  history.replaceState(null,'',path);document.body.innerHTML=html(admin?'knowledge_admin':'knowledge');new Function(script('knowledge_common'))();
  const api={portalSession:true,
    get:vi.fn(async(url:string)=>{
      if(url.endsWith('/auth/me'))return admin?{role:'ADMIN'}:member;
      if(url.endsWith('/catalog'))return {categories,latest:[article]};
      if(url.includes('/categories/'))return {category:categories[0]};
      if(url.includes('/articles/a1'))return {article,previous:null,next:{...article,id:'a2',title:'Bài tiếp'}};
      if(url.includes('/search?')||url.includes('/admin/knowledge/articles?'))return {items:[article],total:1,page:1,limit:20};
      throw new Error(url);
    }),post:vi.fn(async()=>({article})),api:vi.fn(async()=>({article:{...article,revision:3}})),...overrides};
  vi.stubGlobal(admin?'BteAdmin':'BtePortal',api);new Function(script(admin?'knowledge_admin':'knowledge'))();return api;
}
const element=(id:string)=>document.getElementById(id) as HTMLElement;
const form=(id:string)=>document.getElementById(id) as HTMLFormElement;
const submit=(id:string)=>form(id).dispatchEvent(new Event('submit',{cancelable:true}));
afterEach(()=>{document.body.innerHTML='';vi.unstubAllGlobals();vi.restoreAllMocks();});

it('renders category cards and a bounded latest list without treating text as HTML',async()=>{
  mount();await vi.waitFor(()=>expect(element('libraryHome').hidden).toBe(false));
  expect(document.querySelector('.library-category-card')?.getAttribute('href')).toBe('/knowledge?category=c1');
  expect(element('libraryLatest').textContent).toContain('<img');expect(element('libraryLatest').querySelector('img')).toBeNull();
});

it('starts all lesson groups collapsed and links to separate reading pages',async()=>{
  mount('/knowledge?category=c1');await vi.waitFor(()=>expect(element('libraryCategory').hidden).toBe(false));
  const details=document.querySelector('details') as HTMLDetailsElement;expect(details.open).toBe(false);
  expect(details.querySelector('a')?.getAttribute('href')).toBe('/knowledge/lesson/a1');
});

it('formats headings and lists safely and provides previous/next navigation',async()=>{
  mount('/knowledge/lesson/a1');await vi.waitFor(()=>expect(element('libraryLesson').hidden).toBe(false));
  expect(element('libraryLessonBody').querySelector('h2')?.textContent).toBe('Phần đầu');
  expect(element('libraryLessonBody').querySelectorAll('li')).toHaveLength(2);
  expect(element('libraryLessonBody').querySelector('script')).toBeNull();
  expect(element('libraryLessonBody').textContent).toContain('<script>evil()</script>');
  expect(element('libraryLessonNavigation').querySelector('a')?.getAttribute('href')).toBe('/knowledge/lesson/a2');
});

it('searches through the member API with the requested page',async()=>{
  const api=mount('/knowledge?q=ngay%20gio&page=2');await vi.waitFor(()=>expect(element('libraryResults').hidden).toBe(false));
  expect(api.get).toHaveBeenCalledWith('/api/v1/knowledge/search?q=ngay%20gio&page=2');
  expect(element('libraryResultsTitle').textContent).toContain('ngay gio');
});

it('keeps the reader workspace hidden when membership is not valid',async()=>{
  mount('/knowledge',false,{get:vi.fn(async()=>({role:'CUSTOMER',member_access:false}))});
  await vi.waitFor(()=>expect(element('libraryState').textContent).toContain('còn quyền sử dụng'));
  expect(element('libraryWorkspace').hidden).toBe(true);
});

it('does not load authoring data for a non-Admin account',async()=>{
  const get=vi.fn(async()=>member);mount('/admin/knowledge',true,{get});
  await vi.waitFor(()=>expect(element('libraryAdminState').textContent).toContain('Chỉ Admin'));
  expect(element('libraryAdminWorkspace').hidden).toBe(true);expect(get).toHaveBeenCalledTimes(1);
});

it('defaults new content to draft and uses the same nonce when retrying a failed save',async()=>{
  const post=vi.fn().mockRejectedValue(new Error('Try again'));mount('/admin/knowledge',true,{post});
  await vi.waitFor(()=>expect(element('libraryAdminWorkspace').hidden).toBe(false));element('libraryNewArticle').click();
  const editor=form('libraryArticleForm');editor.elements.namedItem('title').value='New lesson';editor.elements.namedItem('body').value='Body';
  expect(editor.elements.namedItem('status').value).toBe('draft');submit('libraryArticleForm');
  await vi.waitFor(()=>expect(element('libraryEditorState').textContent).toBe('Try again'));
  const key=post.mock.calls[0][1].client_key;submit('libraryArticleForm');await vi.waitFor(()=>expect(post).toHaveBeenCalledTimes(2));
  expect(post.mock.calls[1][1].client_key).toBe(key);expect(post.mock.calls[0][1].status).toBe('draft');
});

it('previews safely without publishing and sends edits with the current revision',async()=>{
  const api=mount('/admin/knowledge',true);await vi.waitFor(()=>expect(element('libraryAdminWorkspace').hidden).toBe(false));
  (document.querySelector('#libraryAdminArticles button') as HTMLElement).click();await vi.waitFor(()=>expect(element('libraryEditor').hidden).toBe(false));
  element('libraryPreviewButton').click();expect(element('libraryPreviewBody').querySelector('script')).toBeNull();expect(api.post).not.toHaveBeenCalled();
  submit('libraryArticleForm');await vi.waitFor(()=>expect(api.api).toHaveBeenCalledWith('PATCH','/api/v1/admin/knowledge/articles/a1',expect.objectContaining({expected_revision:2,status:'draft'})));
  await vi.waitFor(()=>expect(element('libraryAdminState').textContent).toContain('Đã lưu bản nháp'));
  expect((element('libraryAdminNext') as HTMLButtonElement).disabled).toBe(true);
});
