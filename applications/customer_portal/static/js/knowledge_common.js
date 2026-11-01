(function(){
  function node(tag,text,cls){const element=document.createElement(tag);if(text!==undefined)element.textContent=String(text);if(cls)element.className=cls;return element;}
  function lessonUrl(id){return '/knowledge/lesson/'+encodeURIComponent(id);}
  function categoryUrl(id){return '/knowledge?category='+encodeURIComponent(id);}
  function date(value){return value?new Date(value).toLocaleDateString('vi-VN'):'';}
  function renderBody(target,text){
    target.replaceChildren();let paragraph=[],list=null,listTag='';
    function flush(){if(paragraph.length){target.append(node('p',paragraph.join('\n')));paragraph=[];}list=null;listTag='';}
    for(const line of String(text||'').replace(/\r\n?/g,'\n').split('\n')){
      const heading=line.match(/^#{1,3}\s+(.+)$/),bullet=line.match(/^\s*[-*]\s+(.+)$/),numbered=line.match(/^\s*\d+[.)]\s+(.+)$/);
      if(!line.trim()){flush();continue;}
      if(heading){flush();target.append(node(line.startsWith('###')?'h3':'h2',heading[1]));continue;}
      if(bullet||numbered){
        if(paragraph.length)flush();const tag=bullet?'ul':'ol';
        if(!list||tag!==listTag){list=node(tag);listTag=tag;target.append(list);}
        list.append(node('li',(bullet||numbered)[1]));continue;
      }
      if(list)flush();paragraph.push(line);
    }
    flush();
  }
  function articleCard(article){
    const card=node('a',undefined,'library-article-card');card.href=lessonUrl(article.id);
    card.append(node('small',article.category_title+' · '+article.group_title),node('strong',article.title));
    if(article.summary)card.append(node('p',article.summary));
    card.append(node('small','Cập nhật '+date(article.updated_at)));return card;
  }
  window.BteKnowledge={node,lessonUrl,categoryUrl,date,renderBody,articleCard};
})();
