from consulting.marriage.report.export import ConsultationExportDocument,export_consultation_file
from consulting.marriage.models.report import ReportBlock,ReportSection

def document(row):
    result=row['result'];profile=result['profile'];useful=profile['useful'];sections=[]
    for year in result['years']:
        blocks=[ReportBlock(block_id='year-'+str(year['year']),kind='paragraph',body=year['narrative'])]
        for month in year['months']:
            label=str(month['month'])+(' nhuận' if month['leap'] else '')
            blocks.append(ReportBlock(block_id=f"month-{year['year']}-{label}",kind='paragraph',
                title=f"Tháng {label} âm lịch · {month['ganzhi']} · {month['cung_phi']['relationship']}",
                body=f"{month['start']} – {month['end']}. {month['narrative']}"))
        sections.append(ReportSection(section_id='year-'+str(year['year']),title=f"Năm {year['year']} · {year['ganzhi']}",
            summary=f"Cung phi: {year['cung_phi']['relationship']}. Bát Tự: {year['bazi']['verdict']}.",blocks=blocks))
    return ConsultationExportDocument(title='Tính vận hạn — '+result['name'],heading='TÍNH VẬN HẠN',subtitle=result['name'],
        filename_stem='BTE_TinhVanHan_'+row['id'],
        summary_rows=[('Mã hồ sơ',row['id']),('Lá số nguồn',result['source_analysis_id']),('Người tạo',row['creator_display_name']+' · '+row['creator_username']),
                      ('Cung phi cá nhân',result['years'][0]['cung_phi']['personal']),('Dụng thần',useful['element']+' · '+str(useful.get('stem') or '')),
                      ('Hỷ thần',', '.join(useful['favorable'])),('Kỵ thần',', '.join(useful['unfavorable'])),
                      ('Khoảng năm',str(result['years'][0]['year'])+' – '+str(result['years'][-1]['year']))],
        sections=sections,notice=result['scope_note']+' Mốc đại vận theo độ chính xác của lá số nguồn. Tháng âm lịch Việt Nam UTC+7; tháng nhuận giữ Can Chi của tháng cùng số.')
def export_file(row,fmt,**kwargs):return export_consultation_file(document(row),row['id'],fmt,**kwargs)
