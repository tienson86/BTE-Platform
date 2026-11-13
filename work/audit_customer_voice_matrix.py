"""Deterministic real-chart coverage audit; never persists analysis snapshots."""
from pathlib import Path
import json, re, html, copy, time, shutil, sys
from collections import Counter
from docx import Document
from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.result_identity import stamp_customer_result_identity
from applications.api.services.customer_report_input import build_customer_report_input
from applications.api.services.customer_export import _render_modern_report_html, _render_modern_report_docx, export_customer_file
from applications.api.services.bazi_analysis_contract import build_bazi_analysis_result, build_ten_gods_four_layer_view
WINTER='--winter' in sys.argv
SEASONAL='--seasonal' in sys.argv or WINTER
OUT=Path('artifacts/customer-voice-winter-20261113' if WINTER else 'artifacts/customer-voice-seasonal-20261113' if SEASONAL else 'artifacts/customer-voice-matrix-20261113');OUT.mkdir(parents=True,exist_ok=True)
BANNED=['trong h\u01b0\u1edbng lu\u1eadn hi\u1ec7n t\u1ea1i','h\u1ee3p logic','n\u1ec1n th\u1ef1c thi','\u0111\u1ed9 thu\u1ea7n','Nguy\u1ec5n Ti\u1ebfn S\u01a1n','V\u0169 Quang Tr\u01b0\u1eddng','L\u01b0\u01a1ng Ng\u1ecdc Hu\u1ef3nh','kh\u00f4ng \u0111\u1ed3ng nh\u1ea5t hai can','\u0111\u00e2y l\u00e0 c\u00e1c l\u1edbp \u0111\u1ec3 h\u1ecfi']
BANNED += ['T\u1ef7/Ki\u1ebfp hi\u1ec7n c\u00f9ng T\u00e0i','Theo h\u01b0\u1edbng lu\u1eadn n\u00e0y']
LABELS={'year':'n\u0103m','month':'th\u00e1ng','day':'ng\u00e0y','hour':'gi\u1edd'}
def norm(s):return ' '.join(s.split())
results=[]; started=time.time()
for cohort,year,month in ([('adult',1990,12)] if WINTER else [('adult',1990,m) for m in range(1,13)] if SEASONAL else [('child',2018,3),('adult',1990,7),('senior',1946,11)]):
 for gender in (('male' if month%2 else 'female',) if SEASONAL else ('male','female')):
  for day in (range(30,31) if WINTER else range(15,16) if SEASONAL else range(10,20)):
   slug=f'{cohort}-{gender}-{year}-{month:02}-{day:02}'
   birth=dict(full_name='Coverage '+slug,birth_place='Ha Noi',year=year,month=month,day=day,hour=10,minute=15,gender=gender,timezone='Asia/Bangkok')
   payload=OrchestratorService().analyze(**{k:birth[k] for k in ('year','month','day','hour','minute','gender','timezone')})
   payload=stamp_customer_result_identity(payload,'matrix-'+slug)
   canonical=build_bazi_analysis_result(payload)['customer_narrative']['report_chapters']
   paragraphs=[p for c in canonical for p in c['paragraphs']]
   prose='\n\n'.join(paragraphs)
   report=build_customer_report_input(analysis_id='matrix-'+slug,data=payload,birth_input=birth)
   markup=_render_modern_report_html(report)
   plain=norm(html.unescape(re.sub('<[^>]*>',' ',markup)))
   docpath=OUT/f'{slug}.docx';_render_modern_report_docx(report,docpath)
   word=norm('\n'.join(p.text for p in Document(docpath).paragraphs))
   missing_html=[p[-100:] for p in paragraphs if norm(p[-100:]) not in plain]
   missing_docx=[p[-100:] for p in paragraphs if norm(p[-100:]) not in word]
   layers=build_ten_gods_four_layer_view(payload)['layers']
   expected={(str(e.get('ten_god')),l['pillar']) for l in layers for mode in ('visible','hidden') for e in l.get(mode,[]) if e.get('ten_god') and str(e.get('ten_god')).lower()!='nh\u1eadt ch\u1ee7'}
   ten=next(c['paragraphs'] for c in canonical if c['id']=='ten_gods')
   missing_positions=[(g,p) for g,p in sorted(expected) if not any(t.startswith(g+' ') and 'tr\u1ee5 '+LABELS[p] in t.split(':',1)[0] for t in ten)]
   gods={g for g,p in expected}
   age_issues=[]
   if cohort in ('child','senior'):
    age_text=' '.join(p for c in canonical if c['id'] in ('life_domains','synthesis') for p in c['paragraphs'])
    career=' '.join(p for c in canonical if c['id']=='life_domains' for p in c['paragraphs'] if p.startswith('Quan v\u1eadn/Ngh\u1ec1 nghi\u1ec7p'))
    if 'doanh thu l\u1edbn' in age_text:age_issues.append('adult-revenue-in-age-scoped-domains')
    if 'chuy\u1ec3n ngh\u1ec1' in career:age_issues.append('career-change-in-age-scoped-career')
   pdf=None
   if gender=='female' and day==18:
    path,_,_=export_customer_file(report_input=report,fmt='pdf')
    target=OUT/f'{slug}.pdf';shutil.copy2(path,target);pdf={'path':str(target),'bytes':target.stat().st_size}
   result={'age_issues':age_issues,'pdf':pdf,'case':slug,'date':f'{year}-{month:02}-{day:02}','cohort':cohort,'gender':gender,'day_master':payload['bazi']['day_master'],'month_pillar':payload['bazi']['month_pillar'],'pattern':payload.get('pattern',{}),'strength_data':payload.get('strength',{}),'day_pillar':payload['bazi']['day_pillar'],'chapters':len(canonical),'empty_chapters':[c['id'] for c in canonical if not c['paragraphs']],'paragraphs':len(paragraphs),'leaks':[x for x in BANNED if x.lower() in prose.lower()],'html_missing':missing_html,'docx_missing':missing_docx,'missing_ten_god_positions':missing_positions,'ten_gods':sorted(gods),'wealth':{'direct':'Ch\u00ednh T\u00e0i' in gods,'indirect':'Thi\u00ean T\u00e0i' in gods},'favorable':payload.get('useful_god',{}).get('useful_display'),'strength':payload.get('strength',{}).get('label')}
   (OUT/f'{slug}-chapters.json').write_text(json.dumps(canonical,ensure_ascii=False,indent=2),encoding='utf-8')
   (OUT/f'{slug}.html').write_text(markup,encoding='utf-8')
   results.append(result)
   print(json.dumps({k:result[k] for k in ('case','day_master','chapters','leaks','html_missing','docx_missing','missing_ten_god_positions','wealth')},ensure_ascii=False),flush=True)
summary={'cases':len(results),'elapsed_seconds':round(time.time()-started,2),'day_masters':dict(Counter(r['day_master'] for r in results)),'cohort_gender_stems':{c+'-'+g:sorted({r['day_master'] for r in results if r['cohort']==c and r['gender']==g}) for c in ('child','adult','senior') for g in ('male','female')},'wealth_combinations':dict(Counter(str(r['wealth']) for r in results)),'day_branches':sorted({r['day_pillar']['branch'] for r in results}),'failures':[r['case'] for r in results if r['chapters']!=11 or any(r[k] for k in ('empty_chapters','leaks','age_issues','html_missing','docx_missing','missing_ten_god_positions'))]}
(OUT/'matrix-results.json').write_text(json.dumps({'summary':summary,'results':results},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
if summary['failures']: raise SystemExit(1)
