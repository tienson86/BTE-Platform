"""Reviewable first draft. Uses BTE canon; does not change existing chart calculations."""
from datetime import date, timedelta
from functools import lru_cache
from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm as G
from engines.calendar_engine.lunar.converter import solar_to_lunar
from engines.calendar_engine.cung_phi import calculate_cung_phi, cung_for_ganzhi
from engines.calendar_engine.tam_nguyen import calculate_tam_nguyen
from engines.bazi_engine.engine import HIDDEN
from engines.bazi_engine.ten_god import stem_element, branch_element, ten_god_name
from consulting.canon.du_nien import load_matrix

VERSION = 'VAN-HAN-INITIAL-01'
ELEMENTS = {'Mộc', 'Hỏa', 'Thổ', 'Kim', 'Thủy'}
XUNG = {frozenset(pair) for pair in [('Tý','Ngọ'),('Sửu','Mùi'),('Dần','Thân'),('Mão','Dậu'),('Thìn','Tuất'),('Tỵ','Hợi')]}
HOP = {frozenset(pair) for pair in [('Tý','Sửu'),('Dần','Hợi'),('Mão','Tuất'),('Thìn','Dậu'),('Tỵ','Thân'),('Ngọ','Mùi')]}
PILLARS = {'year':'năm','month':'tháng','day':'ngày','hour':'giờ'}

def palace_pair(birth_year, gender, ganzhi, reference_year):
    personal = calculate_cung_phi(year=birth_year, gender=gender).cung_phi
    yuan = calculate_tam_nguyen(reference_year).tam_nguyen
    period = cung_for_ganzhi(ganzhi, tam_nguyen=yuan, reference_year=reference_year, gender='male')
    relation = load_matrix()[(personal,period)]
    return {'personal':personal,'period':period,'tam_nguyen':yuan,
            'relationship':relation.relationship_label,'relationship_id':relation.relationship_id,
            'favorable':relation.category == 'favorable',
            'note':f'Cung {personal} của bạn gặp cung {period} của thời điểm, tạo quan hệ {relation.relationship_label} theo bảng Du Niên.'}

@lru_cache(maxsize=64)
def lunar_months(year):
    """Inclusive solar date ranges, Vietnam UTC+7; leap month retains its numbered month's Can Chi."""
    if not 1900 <= year <= 2100:
        raise ValueError('Bản nháp giới hạn năm 1900–2100')
    rows=[];current=None;day=date(year,1,1);stop=date(year+1,3,1)
    ystem=G.STEM.index(G.year(year)['can'])
    while day<stop:
        lunar=solar_to_lunar(day.day,day.month,day.year,time_zone=7)
        if lunar.year==year:
            key=(lunar.month,lunar.leap)
            if current is None or current['key']!=key:
                if lunar.day!=1:raise ValueError('Lịch âm thiếu ngày đầu tháng')
                gz=G.month(ystem,lunar.month-1)
                current={'key':key,'month':lunar.month,'leap':lunar.leap,'ganzhi':gz['can']+' '+gz['chi'],
                         'start':day.isoformat(),'end':day.isoformat()}
                rows.append(current)
            else:current['end']=day.isoformat()
        day+=timedelta(days=1)
    for row in rows:row.pop('key')
    if len(rows) not in (12,13):raise ValueError('Số tháng âm lịch không hợp lệ')
    return tuple(rows)

def validate(profile):
    if profile.get('gender') not in ('male','female'):raise ValueError('Thiếu giới tính')
    if not profile.get('lunar_birth_year'):raise ValueError('Thiếu năm sinh âm lịch')
    for key in PILLARS:
        parts=str(profile.get('pillars',{}).get(key,'')).split()
        if len(parts)!=2 or parts[0] not in G.STEM or parts[1] not in G.BRANCH:
            raise ValueError('Thiếu hoặc sai Can Chi trụ '+PILLARS[key])
    useful=profile.get('useful') or {}
    if useful.get('element') not in ELEMENTS:raise ValueError('Thiếu Dụng thần có cấu trúc; không suy đoán từ văn luận')
    if useful.get('stem') and stem_element(useful['stem'])!=useful['element']:
        raise ValueError('Can Dụng thần không khớp ngũ hành')
    favorable=set(useful.get('favorable') or []);unfavorable=set(useful.get('unfavorable') or [])
    if not favorable|unfavorable <= ELEMENTS:raise ValueError('Hỷ/Kỵ thần có ngũ hành không hợp lệ')
    if (favorable|{useful['element']}) & unfavorable:raise ValueError('Dụng/Hỷ và Kỵ thần mâu thuẫn; cần kiểm tra hồ sơ nguồn')

def element_evidence(element, location, useful):
    if element==useful['element']:return {'type':'support','text':f'{location} mang hành {element}, cùng hành với Dụng thần của hồ sơ.'}
    if element in useful.get('favorable',[]):return {'type':'support','text':f'{location} mang hành {element}, thuộc Hỷ thần của hồ sơ.'}
    if element in useful.get('unfavorable',[]):return {'type':'pressure','text':f'{location} mang hành {element}, thuộc Kỵ thần của hồ sơ; cần xét mức độ tăng thêm khi phối hợp với mệnh gốc và đại vận.'}
    return {'type':'reference','text':f'{location} mang hành {element}; hồ sơ chưa xếp hành này vào Dụng/Hỷ/Kỵ thần.'}

def cycles_for(profile,year):
    return [c for c in profile.get('cycles',[]) if c.get('year_start') is not None and c.get('year_end') is not None
            and int(c['year_start'])<=year<=int(c['year_end'])]

def bazi_evidence(profile,ganzhi,year,year_ganzhi=None):
    stem,branch=ganzhi.split();dm=profile['pillars']['day'].split()[0];useful=profile['useful']
    god=ten_god_name(dm,stem)
    evidence=[element_evidence(stem_element(stem),f'Thiên can {stem}',useful),element_evidence(branch_element(branch),f'Địa chi {branch}',useful)]
    hidden=[{'stem':h,'element':stem_element(h),'ten_god':ten_god_name(dm,h)} for h in HIDDEN[branch]]
    exact=bool(useful.get('stem') and stem==useful['stem'])
    if useful.get('stem'):
        evidence.append({'type':'reference','text':f'{stem} là {god} đối với Nhật chủ {dm}. '+
                         (f'Thiên can thời điểm gặp đúng can Dụng thần {stem}.' if exact else
                          f'Can Dụng thần của hồ sơ là {useful["stem"]}; không đồng nhất hai thiên can chỉ vì cùng ngũ hành.')})
    for key,value in profile['pillars'].items():
        natal=value.split()[1];pair=frozenset((branch,natal))
        if branch==natal:
            evidence.append({'type':'reference','text':f'Chi {branch} lặp lại chi trụ {PILLARS[key]}; đây là điểm cần đối chiếu thêm, chưa tự kết luận thành hạn.'})
        elif pair in XUNG:
            evidence.append({'type':'interaction','text':f'{branch} xung {natal} ở trụ {PILLARS[key]}; cần xem sự thay đổi tác động vào đâu và có yếu tố trợ lực nào.'})
        elif pair in HOP:
            evidence.append({'type':'interaction','text':f'{branch} hợp {natal} ở trụ {PILLARS[key]}; ghi nhận quan hệ hợp, không mặc định đã hóa thành hành khác.'})
    cycles=cycles_for(profile,year)
    gaps=[]
    if not cycles:gaps.append('Chưa có đại vận tương ứng từ hồ sơ nguồn, nên chưa kết luận mức thuận/nghịch tổng hợp.')
    if len(cycles)>1:gaps.append('Năm nằm ở ranh giới hai đại vận; cần thời điểm chuyển vận chính xác để chia giai đoạn.')
    if profile.get('cycle_precision') == 'year_level' and any(year == c.get('year_start') for c in cycles):
        gaps.append('Đây là năm chuyển đại vận theo mốc năm của hồ sơ; cần thời điểm chuyển vận cụ thể để phân chia trong năm.')
    for cycle in cycles:
        label=cycle.get('gan_zhi') or ''
        parts=label.split()
        if len(parts)!=2 or parts[0] not in G.STEM or parts[1] not in G.BRANCH:
            gaps.append('Đại vận thiếu Can Chi hợp lệ.');continue
        for element,where in [(stem_element(parts[0]),'Can đại vận '+label),(branch_element(parts[1]),'Chi đại vận '+label)]:
            evidence.append(element_evidence(element,where,useful))
    if year_ganzhi:
        parts=year_ganzhi.split()
        evidence.append(element_evidence(stem_element(parts[0]),'Can của năm '+year_ganzhi,useful))
        evidence.append(element_evidence(branch_element(parts[1]),'Chi của năm '+year_ganzhi,useful))
    support=any(e['type']=='support' for e in evidence);pressure=any(e['type']=='pressure' for e in evidence)
    interaction=any(e['type']=='interaction' for e in evidence)
    if gaps:verdict='Chưa đủ căn cứ kết luận tổng hợp'
    elif support and pressure:verdict='Thuận/nghịch đan xen'
    elif pressure:verdict='Cần thận trọng'
    elif support and interaction:verdict='Có trợ lực, cần xét thêm tương tác'
    elif support:verdict='Có trợ lực theo Dụng/Hỷ thần'
    else:verdict='Chưa có dấu hiệu nổi trội theo Dụng/Hỷ/Kỵ thần'
    return {'day_master':dm,'ten_god':god,'hidden_stems':hidden,'exact_useful_stem':exact,
            'evidence':evidence,'cycles':cycles,'missing_context':gaps,'verdict':verdict,
            'coverage':'Dụng/Hỷ/Kỵ, lục hợp và lục xung sơ bộ; chưa chấm trọng số tàng can, hình/hại/phá hoặc điều kiện hợp hóa.'}

def period(profile,ganzhi,year,year_ganzhi=None):
    cung=palace_pair(profile['lunar_birth_year'],profile['gender'],ganzhi,year)
    bazi=bazi_evidence(profile,ganzhi,year,year_ganzhi)
    bad=cung['relationship_id'] in ('tuyet_menh','ngu_quy','luc_sat','hoa_hai')
    pressure=any(e['type']=='pressure' for e in bazi['evidence'])
    candidate=bad or pressure
    narrative=cung['note']+' '+('Thời điểm này được đưa vào danh sách cần lưu ý theo cung phi. ' if bad else 'Theo cung phi, thời điểm này có quan hệ thuận. ')
    narrative+=f'Thiên can {ganzhi.split()[0]} mang vai trò {bazi["ten_god"]} đối với Nhật chủ {bazi["day_master"]}. '
    narrative+=' '.join(e['text'] for e in bazi['evidence'][:3])
    if bazi['missing_context']:narrative+=' '+ ' '.join(bazi['missing_context'])
    if bazi['cycles']:
        narrative+=' Đại vận đang đối chiếu là '+', '.join(c.get('gan_zhi','')+' ('+str(c.get('year_start'))+'–'+str(c.get('year_end'))+')' for c in bazi['cycles'])+'.'
    if any(e['type']=='pressure' for e in bazi['evidence']):
        narrative+=' Khi cả yếu tố hỗ trợ và áp lực cùng xuất hiện, bạn nên chia công việc thành từng bước, dành thời gian kiểm tra cam kết và giữ khoảng dự phòng thay vì tăng mọi việc cùng lúc.'
    else:
        narrative+=' Các yếu tố hỗ trợ là căn cứ để cân nhắc tiến công việc có chuẩn bị; hãy giữ quy trình và nhịp làm việc vừa sức.'
    return {'ganzhi':ganzhi,'cung_phi':cung,'bazi':bazi,'review_candidate':candidate,'narrative':narrative}

def build(profile,start,end):
    validate(profile)
    if start < profile['lunar_birth_year']:raise ValueError('Năm xét không được trước năm sinh âm lịch')
    if end<start or end-start>20:raise ValueError('Khoảng xét tối đa 21 năm')
    years=[]
    for year in range(start,end+1):
        gz=G.year(year);label=gz['can']+' '+gz['chi']
        row={'year':year,**period(profile,label,year)}
        row['months']=[]
        for month in lunar_months(year):
            item={**month,**period(profile,month['ganzhi'],year,label)}
            end_year=int(month['end'][:4])
            related=cycles_for(profile,int(month['start'][:4]))+cycles_for(profile,end_year)
            unique={str(c.get('index',c.get('gan_zhi'))):c for c in related}
            if len(unique)>1:
                note='Khoảng ngày dương của tháng chạm hai mốc đại vận; cần xác định thời điểm chuyển vận trước khi kết luận cho cả tháng.'
                item['bazi']['cycles']=list(unique.values());item['bazi']['missing_context'].append(note)
                item['bazi']['verdict']='Cần phân chia thời điểm chuyển đại vận';item['narrative']+=' '+note
            row['months'].append(item)
        years.append(row)
    return {'version':VERSION,'name':profile.get('name',''),'status':'DRAFT_FOR_REVIEW',
            'timezone':'Asia/Ho_Chi_Minh (UTC+7)', 'period_palace_basis':'Bảng cung thời điểm dùng cột quy chiếu nam của Tam Nguyên thời điểm, theo cách BTE đang áp dụng; cung cá nhân dùng giới tính thật.',
            'month_basis':'Can Chi tháng âm lịch theo Ngũ Hổ Độn; tháng nhuận giữ Can Chi của tháng cùng số. Đây là nhánh tháng âm lịch riêng, không thay thế lưu nguyệt theo tiết khí.',
            'years':years}
