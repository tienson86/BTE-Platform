from fastapi.testclient import TestClient
from applications.customer_portal.app import create_app as portal_app
from applications.web_admin.app import create_app as admin_app
from applications.web_admin.templates_util import render_page


def test_member_communications_pages_have_shared_navigation_and_no_admin_controls_visible():
    client=TestClient(portal_app())
    for path,marker in (("/messages",'data-communications="messages"'),("/community",'data-communications="community"')):
        response=client.get(path)
        assert response.status_code==200
        assert marker in response.text and "{{" not in response.text
        assert 'href="/messages"' in response.text and 'href="/community"' in response.text
        member_nav=response.text.split('data-customer-nav="member"',1)[1].split('</nav>',1)[0]
        public_nav=response.text.split('data-customer-nav="primary"',1)[1].split('</nav>',1)[0]
        assert member_nav.count('data-nav-id=')==7
        assert public_nav.count('data-nav-id=')==3
    assert 'id="recipientLabel" hidden' in client.get("/messages").text
    assert 'id="knowledgeModerationForm" class="comm-form comm-moderation" hidden' in client.get("/community").text


def test_integrated_and_standalone_admin_render_same_communications_screens():
    portal=TestClient(portal_app());standalone=TestClient(admin_app())
    for section in ("messages","community"):
        integrated=portal.get("/admin/"+section)
        separate=standalone.get("/"+section)
        assert integrated.status_code==separate.status_code==200
        for page in (integrated.text,separate.text):
            assert 'data-admin-mode="true"' in page and "{{" not in page
            assert 'id="adminWorkspace" hidden' in page
        assert f'/admin/portal-static/js/{section}.js' in integrated.text
        assert f'/portal-static/js/{section}.js' in separate.text
        assert portal.get(f'/admin/portal-static/js/{section}.js').status_code==200
        assert standalone.get(f'/portal-static/js/{section}.js').status_code==200


def test_admin_archive_keeps_internal_notes_separate_from_member_replies():
    client=TestClient(portal_app())
    script=client.get("/static/js/admin_archive.js").text
    assert "Ghi chú nội bộ (chỉ Admin)" in script
    assert "Mở tin nhắn và trả lời thành viên" in script
    assert "/communications/contacts/" in script
