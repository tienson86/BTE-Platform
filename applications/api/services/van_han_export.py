from consulting.marriage.report.export import ConsultationExportDocument,export_consultation_file
from consulting.marriage.models.report import ReportBlock,ReportSection

def good_period_blocks(key, period):
    evidence = "\n".join("• " + entry["text"] for entry in period["bazi"]["evidence"])
    return [
        ReportBlock(block_id=key+"-palace",kind="paragraph",title="Cung Phi – Du Niên",body=period["cung_phi"]["note"]+" "+period["palace_assessment_label"]+"."),
        ReportBlock(block_id=key+"-assessment",kind="paragraph",title=f'Bát Tự · {period["bazi_assessment_label"]}',body=period["assessment"]),
        ReportBlock(block_id=key+"-evidence",kind="paragraph",title="Cơ sở Bát Tự",body=evidence),
    ]

def document(row):
    result=row['result'];profile=result['profile'];useful=profile['useful'];sections=[]
    good_years=result.get('kind')=='good_years'
    title='Tính các năm tốt' if good_years else 'Tính vận hạn'
    for year in result['years']:
        blocks=[ReportBlock(block_id='year-'+str(year['year']),kind='paragraph',body=year['narrative'])]
        if good_years:
            blocks.extend(good_period_blocks(f"year-{year['year']}", year))
        for month in year['months']:
            label=str(month['month'])+(' nhuận' if month['leap'] else '')
            key=f"month-{year['year']}-{label}"
            month_title=f"Tháng {label} âm lịch · {month['ganzhi']} · {month['cung_phi']['relationship']}"
            if good_years:
                month_title += " · " + month["assessment_label"]
            blocks.append(ReportBlock(block_id=key,kind='paragraph',title=month_title,
                body=f"{month['start']} – {month['end']}. {month['narrative']}"))
            if good_years:
                blocks.extend(good_period_blocks(key, month))
        year_status = year["assessment_label"] if good_years else ""
        sections.append(ReportSection(section_id='year-'+str(year['year']),title=f"Năm {year['year']} · {year['ganzhi']}"+(f" · {year_status}" if year_status else ""),
            summary=f"Cung phi: {year['cung_phi']['relationship']}. Bát Tự: {year['bazi']['verdict']}.",blocks=blocks))
    totals=[]
    if good_years:
        years=result["years"]
        months=[month for year in years for month in year["months"]]
        totals=[
            ("Cung Phi", f"{sum(y['cung_phi']['favorable'] for y in years)} năm thuận · {sum(m['cung_phi']['favorable'] for m in months)} tháng thuận"),
            ("Bát Tự (gồm thuận có lưu ý)", f"{sum(y['bazi_favorable'] for y in years)} năm thuận · {sum(m['bazi_favorable'] for m in months)} tháng thuận"),
        ]
    return ConsultationExportDocument(title=title+' — '+result['name'],heading=title.upper(),subtitle=result['name'],
        filename_stem=('BTE_TinhCacNamTot_' if good_years else 'BTE_TinhVanHan_')+row['id'],
        summary_rows=[('Mã hồ sơ',row['id']),('Lá số nguồn',result['source_analysis_id']),('Người tạo',row['creator_display_name']+' · '+row['creator_username']),
                      ('Cung phi cá nhân',result['years'][0]['cung_phi']['personal']),('Dụng thần',useful['element']+' · '+str(useful.get('stem') or '')),
                      ('Hỷ thần',', '.join(useful['favorable'])),('Kỵ thần',', '.join(useful['unfavorable'])),
                      ('Khoảng năm',str(result['years'][0]['year'])+' – '+str(result['years'][-1]['year']))]+totals,
        sections=sections,notice=result['scope_note']+' Mốc đại vận theo độ chính xác của lá số nguồn. Tháng âm lịch Việt Nam UTC+7; tháng nhuận giữ Can Chi của tháng cùng số.')
def export_file(row,fmt,**kwargs):return export_consultation_file(document(row),row['id'],fmt,**kwargs)
