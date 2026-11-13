from pathlib import Path
import json, shutil, re
from docx import Document
from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.result_identity import stamp_customer_result_identity
from applications.api.services.customer_report_input import build_customer_report_input
from applications.api.services.customer_export import _render_modern_report_html, export_customer_file
from applications.api.services.bazi_analysis_contract import build_bazi_analysis_result

OUT=Path('artifacts/customer-voice-standard-20261113');OUT.mkdir(parents=True,exist_ok=True)
CASES=[('son','Nguyễn Tiến Sơn',1987,1,21,4,31,'male','Hà Nội'),('truong','Vũ Quang Trường',1982,2,22,4,31,'male','Bắc Ninh'),('huynh','Lương Ngọc Huỳnh',1966,9,24,4,15,'male','Hà Nội'),('ha','Lê Thúy Hà',1975,5,17,3,31,'female','Thanh Hóa')]
results=[]
for slug,name,y,m,d,h,minute,gender,place in CASES:
    birth=dict(full_name=name,birth_place=place,year=y,month=m,day=d,hour=h,minute=minute,gender=gender,timezone='Asia/Bangkok')
    payload=OrchestratorService().analyze(**{k:birth[k] for k in ('year','month','day','hour','minute','gender','timezone')})
    payload=stamp_customer_result_identity(payload,'voice-standard-'+slug)
    report=build_customer_report_input(analysis_id='voice-standard-'+slug,data=payload,birth_input=birth)
    html=_render_modern_report_html(report);(OUT/f'{slug}.html').write_text(html,encoding='utf-8')
    canonical=build_bazi_analysis_result(payload)['customer_narrative']['report_chapters']
    (OUT/f'{slug}-chapters.json').write_text(json.dumps(canonical,ensure_ascii=False,indent=2),encoding='utf-8')
    paragraphs=[p for c in canonical for p in c['paragraphs']]
    text='\n\n'.join(paragraphs);(OUT/f'{slug}-prose.txt').write_text(text,encoding='utf-8')
    banned=['trong hướng luận hiện tại','không đồng nhất hai can','đây là các lớp để hỏi','hợp logic','nền thực thi','độ thuần','Tù khí theo tháng -10']
    leaks=[x for x in banned if x in text]
    files={}
    for fmt in ('docx','pdf'):
        path,_,result=export_customer_file(report_input=report,fmt=fmt)
        target=OUT/f'{slug}.{fmt}';shutil.copy2(path,target);files[fmt]={'path':str(target),'bytes':target.stat().st_size}
    doc=Document(OUT/f'{slug}.docx');word='\n'.join(p.text for p in doc.paragraphs)
    # Long paragraph body tails are invariant under heading extraction in both exporters.
    missing=[p[-100:] for p in paragraphs if p[-100:] not in word]
    results.append({'case':slug,'chapters':len(canonical),'paragraphs':len(paragraphs),'characters':len(text),'leaks':leaks,'word_missing_tails':missing,'files':files,'day_master':payload['bazi']['day_master'],'useful':payload['useful_god'].get('useful_display')})
    print(json.dumps(results[-1],ensure_ascii=False),flush=True)
(OUT/'verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')