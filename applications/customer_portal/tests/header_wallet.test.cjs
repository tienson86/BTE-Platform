const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const source=fs.readFileSync(path.join(__dirname,'../static/js/auth_gate.js'),'utf8');
const flush=()=>new Promise(resolve=>setImmediate(resolve));
function setup(readWallet){
  const handlers={},requests=[],timers=new Set();
  const badge={hidden:true,attrs:{},setAttribute(k,v){this.attrs[k]=v;}};
  const count={textContent:'—'};
  const document={hidden:false,readyState:'complete',body:{dataset:{}},getElementById:id=>({headerLinhThach:badge,headerLinhThachBalance:count}[id]||null),querySelectorAll:()=>[],querySelector:()=>null,addEventListener:(k,v)=>handlers[k]=v};
  const api={getToken:()=> 'test',setSession(){},clearSession(){handlers['bte:session-cleared']?.();},get:async p=>{
    requests.push(p);if(p==='/api/v1/auth/me')return {user_id:'one',username:'one',member_access:true,role:'CUSTOMER'};
    if(p.endsWith('/wallet-balance'))return readWallet();return {};
  }};
  const window={BtePortal:api,location:{pathname:'/membership',search:'',assign(){},replace(){}},addEventListener:(k,v)=>handlers[k]=v};
  vm.runInNewContext(source,{window,document,BtePortal:api,setInterval:fn=>{timers.add(fn);return fn;},clearInterval:fn=>timers.delete(fn)});
  return {badge,count,handlers,document,requests,timers};
}
test('shows actual balance including zero and refreshes on mutations',async()=>{
  let balance=0;const app=setup(async()=>({balance}));await flush();assert.equal(app.badge.hidden,false);assert.equal(app.count.textContent,'0');
  balance=13;await app.handlers['bte:wallet-changed']();assert.equal(app.count.textContent,'13');assert.match(app.badge.attrs['aria-label'],/13 Linh Thạch/);
});
test('logout clears the display and prevents an in-flight response from showing the old balance',async()=>{
  let resolve;const app=setup(()=>new Promise(r=>resolve=r));await flush();app.handlers['bte:session-cleared']();resolve({balance:99});await flush();
  assert.equal(app.badge.hidden,true);assert.equal(app.count.textContent,'—');assert.equal(app.timers.size,0);
});
test('network failure shows unavailable, never an invented zero',async()=>{
  const app=setup(async()=>{throw new Error('offline');});await flush();assert.equal(app.count.textContent,'—');assert.match(app.badge.title,/Chưa tải/);
});
test('a mutation during a pending balance read triggers a fresh read',async()=>{
  let resolve,calls=0;const app=setup(()=>++calls===1?new Promise(r=>resolve=r):Promise.resolve({balance:8}));await flush();
  app.handlers['bte:wallet-changed']();resolve({balance:3});await flush();await flush();assert.equal(calls,2);assert.equal(app.count.textContent,'8');
});
