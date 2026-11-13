"""Regression checks for the approved customer writing standard."""
import copy
import pytest
from applications.api.services.customer_voice_standard import age_application, cycle_branch_context
from applications.api.services.approved_domains_luck_editorial import luck_cycle_prose, life_domain_prose, recommendation_prose
from applications.api.services.bazi_analysis_contract import _annual_branch_evidence, _annual_roadmap_paragraphs
from applications.api.services.wealth_reasoning import build_wealth_reasoning

@pytest.mark.parametrize('god', ['Thực Thần','Thương Quan','Thiên Tài','Chính Tài','Thất Sát','Chính Quan','Thiên Ấn','Chính Ấn','Tỷ Kiên','Kiếp Tài'])
def test_age_lens_changes_application_without_business_in_children_or_old_age(god):
    child, adult, senior = (age_application(god, age) for age in (7, 37, 77))
    assert len({child, adult, senior}) == 3
    assert 'tuổi đi học' in child or 'giai đoạn học tập' in child
    assert 'cao tuổi' in senior
    for text in (child, senior):
        assert 'đội ngũ' not in text and 'giá bán' not in text and 'tăng khách' not in text


def test_equal_counts_do_not_become_more_less_or_disease_prediction():
    payload={'bazi':{'day_master':'Quý','day_master_element':'Thủy'},'five_elements':{'counts':{k:2 for k in ('wood','fire','earth','metal','water')}}}
    original=copy.deepcopy(payload)
    text=' '.join(life_domain_prose('health',payload))
    assert 'nhiều và' not in text and 'ít nhất' not in text
    assert all(x in text for x in ('Mộc','Hỏa','Thổ','Kim','Thủy'))
    assert 'không phản ánh sức khỏe' in text
    assert payload==original


def test_cycle_relations_keep_both_positions_not_first_only():
    text=cycle_branch_context('Thân',{'year_pillar':{'branch':'Dần'},'hour_pillar':{'branch':'Dần'},'month_pillar':{'branch':'Tỵ'}})
    assert 'trụ năm' in text and 'trụ giờ' in text and 'trụ tháng' in text
    assert 'không tự xác định' in text


def test_missing_cycle_start_and_current_index_are_not_invented():
    text=' '.join(luck_cycle_prose({'bazi':{'day_master':'Quý'}},{'cycles':[{'stem':'Bính','branch':'Tuất'}], 'current_cycle':{'stem':'Bính'}}))
    assert 'None' not in text and 'Vận đang đi qua' not in text
    assert 'Chính Tài' in text


def test_hop_is_not_automatically_favorable():
    text=_annual_branch_evidence('Thân',['Tỵ','Dần','Dần'])
    assert 'Thân-Tỵ hợp' in text and 'Thân-Dần xung' in text
    assert 'thuận' not in text and text.count('Thân-Dần')==1


def test_annual_for_child_does_not_recommend_business():
    payload={'bazi':{'day_master':'Quý'}, 'luck':{'cycles':[{'year_start':2022,'year_end':2031,'age_start':5,'gan_zhi':'Bính Tuất'}], 'annual_identity':{'civil_year':2026,'nearby_years':[{'year':2026,'gan_zhi':'Bính Ngọ','branch':'Ngọ','ten_god':'Chính Tài'}]}}}
    text=' '.join(_annual_roadmap_paragraphs(payload))
    assert 'tuổi đi học' in text and 'giá bán' not in text


def test_advice_does_not_assume_everyone_sells_services():
    text=' '.join(recommendation_prose({'bazi':{'day_master':'Ất'},'pattern':{'cach_cuc':'Chính Ấn'}}))
    assert 'khách hàng' not in text and 'giao dịch vụ' not in text


def test_wealth_prose_does_not_change_with_known_profession():
    payload={'bazi':{'day_master':'Canh','year_pillar':{'stem':'Bính','branch':'Dần'},'month_pillar':{'stem':'Tân','branch':'Sửu'},'day_pillar':{'stem':'Canh','branch':'Ngọ'},'hour_pillar':{'stem':'Mậu','branch':'Dần'}}}
    a=build_wealth_reasoning(payload)['customer']['paragraphs']
    payload['occupation']='pháp sư'
    b=build_wealth_reasoning(payload)['customer']['paragraphs']
    assert a==b
    assert 'Không thấy Thiên Tài' in ' '.join(a)  # no hidden-stem facts were supplied

@pytest.mark.parametrize('stem', ['Giáp','Ất','Bính','Đinh','Mậu','Kỷ','Canh','Tân','Nhâm','Quý'])
@pytest.mark.parametrize('age', [8, 80])
def test_all_day_masters_use_life_stage_not_sample_business_copy(stem, age):
    from applications.api.services.customer_voice_standard import age_scoped_domain
    from applications.api.services.approved_domains_luck_editorial import synthesis_prose
    payload = {'bazi': {'day_master': stem, 'day_pillar': {'stem': stem, 'branch': 'Tý'}, 'hour_pillar': {'stem':'Giáp','branch':'Tý'}}, 'luck': {'current_age_for_luck': age}, 'pattern': {'cach_cuc': 'Chính Tài'}}
    before = copy.deepcopy(payload)
    for key in ('career','children','wealth'):
        text = ' '.join(age_scoped_domain(key, payload))
        assert text and 'khách hàng' not in text and 'vốn góp' not in text
    text = ' '.join(synthesis_prose(payload))
    assert stem in text and 'doanh thu lớn' not in text
    assert payload == before


def test_missing_age_is_not_guessed_from_day_master():
    from applications.api.services.customer_voice_standard import current_age, age_scoped_domain
    payload = {'bazi': {'day_master': 'Canh'}}
    assert current_age(payload) is None
    assert age_scoped_domain('career', payload) == []



def test_peer_presence_does_not_invent_absent_wealth():
    from applications.api.services.wealth_reasoning import _customer_paragraphs
    stars = {key: {'ten_god': name, 'stem': stem, 'occurrences': []} for key,name,stem in [('direct_wealth','Chính Tài','Nhâm'),('indirect_wealth','Thiên Tài','Quý')]}
    text = ' '.join(_customer_paragraphs([], {}, {'state':'wealth_contested_by_peer'}, {}, {}, stars))
    assert 'Không thấy Chính Tài' in text and 'Không thấy Thiên Tài' in text
    assert 'hiện cùng Tài' not in text and 'không tự xác nhận có Tài tinh' in text
