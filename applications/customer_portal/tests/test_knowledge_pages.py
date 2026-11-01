import pytest
from fastapi.testclient import TestClient
from applications.customer_portal.app import create_app
from applications.web_admin.app import create_app as admin_app


@pytest.mark.parametrize('path',['/knowledge','/knowledge/lesson/example'])
def test_member_library_shell_menu_and_assets(path):
    client=TestClient(create_app());page=client.get(path)
    assert page.status_code==200 and 'data-knowledge="reader"' in page.text
    assert 'class="member-sidebar__quick-link active" aria-current="page" href="/knowledge" data-forum-only hidden' in page.text
    assert 'id="libraryWorkspace" hidden' in page.text
    assert 'id="libraryLessonNavigation"' in page.text and 'id="librarySearch"' in page.text
    for asset in ('css/knowledge.css','js/knowledge_common.js','js/knowledge.js'):
        assert client.get('/static/'+asset).status_code==200
    assert '{{' not in page.text
    assert '<template id="libraryQuestionsTemplate">' in page.text
    assert 'category-faq-09' in page.text


def test_integrated_and_standalone_admin_share_the_same_authoring_form():
    for client,path,prefix in ((TestClient(create_app()),'/admin/knowledge','/admin/portal-static/'),(TestClient(admin_app()),'/knowledge','/portal-static/')):
        page=client.get(path)
        assert page.status_code==200 and 'data-knowledge="admin"' in page.text
        assert 'id="adminWorkspace" hidden' in page.text and 'id="libraryAdminWorkspace" hidden' in page.text
        assert 'name="status"' in page.text and 'value="draft"' in page.text
        assert 'id="libraryPreview"' in page.text and 'id="libraryStructureForm"' in page.text
        assert prefix+'js/knowledge_admin.js' in page.text and '{{' not in page.text
        assert client.get(prefix+'js/knowledge_admin.js').status_code==200
