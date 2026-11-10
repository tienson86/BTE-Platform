from fastapi.testclient import TestClient
from applications.customer_portal.app import create_app
from applications.web_admin.app import create_app as admin_app


def test_course_menu_is_private_and_member_page_and_assets_exist():
    client=TestClient(create_app())
    response=client.get('/khoa-hoc')
    assert response.status_code==200
    assert 'href="/khoa-hoc" data-forum-only hidden>Khóa học' in response.text
    assert 'id="coursesApp"' in response.text
    for asset in ('css/courses.css','js/courses.js','js/courses_admin.js'):
        assert client.get('/static/'+asset).status_code==200


def test_courses_admin_is_available_in_both_admin_shells():
    portal=TestClient(create_app()).get('/admin/courses')
    assert portal.status_code==200 and 'id="courseAdminContent"' in portal.text
    assert 'data-admin-session="portal"' in portal.text
    assert '/admin/portal-static/js/courses_admin.js' in portal.text
    standalone=TestClient(admin_app()).get('/courses')
    assert standalone.status_code==200 and 'id="courseAdminContent"' in standalone.text
    assert 'href="/courses"' in standalone.text
