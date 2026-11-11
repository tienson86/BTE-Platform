"""Server-render the published library through the same read-only API as the portal."""
from html import escape
import re
from urllib.parse import quote, urlencode

import httpx

TITLE = "Kiến thức phong thủy"


def link(label, href):
    return f'<a href="{escape(href)}">{escape(label)}</a>'


def lesson_url(article):
    return "/knowledge/lesson/" + quote(article.get("slug") or article["id"], safe="")


def category_url(identifier):
    return "/knowledge?" + urlencode({"category": identifier})


def article_cards(articles):
    return "".join(
        f'<a class="library-article-card" href="{lesson_url(a)}">'
        f'<small>{escape(a["category_title"])} · {escape(a["group_title"])}</small>'
        f'<strong>{escape(a["title"])}</strong><p>{escape(a["summary"])}</p></a>'
        for a in articles
    ) or '<p class="muted">Chưa có bài viết.</p>'


def prose(body):
    """Render the library's existing heading/list/plain-text format without raw HTML."""
    chunks, paragraph, list_tag = [], [], ""

    def flush():
        nonlocal list_tag
        if paragraph:
            chunks.append("<p>" + "<br>".join(escape(line) for line in paragraph) + "</p>")
            paragraph.clear()
        if list_tag:
            chunks.append(f"</{list_tag}>")
            list_tag = ""

    for line in body.splitlines():
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        bullet = re.match(r"^\s*([-*]|\d+[.)])\s+(.+)$", line)
        if not line.strip():
            flush()
        elif heading:
            flush()
            level = 3 if len(heading[1]) == 3 else 2
            chunks.append(f"<h{level}>{escape(heading[2])}</h{level}>")
        elif bullet:
            tag = "ul" if bullet[1] in ("-", "*") else "ol"
            if tag != list_tag:
                flush()
                chunks.append(f"<{tag}>")
                list_tag = tag
            chunks.append(f"<li>{escape(bullet[2])}</li>")
        else:
            if list_tag:
                flush()
            paragraph.append(line)
    flush()
    return "".join(chunks)


async def render_knowledge(params, identifier, api_base):
    query = params.get("q", "").strip()[:120]
    category_id = params.get("category", "")
    raw_page = params.get("page", "1")
    page = min(100000, max(1, int(raw_page))) if raw_page.isascii() and raw_page.isdigit() and len(raw_page) <= 6 else 1
    options = {}
    if identifier is not None:
        endpoint = "/articles/" + quote(identifier, safe="")
    elif query:
        endpoint = "/search"
        options = {"q": query, "page": page}
    elif category_id:
        endpoint = "/categories/" + quote(category_id, safe="")
    else:
        endpoint = "/catalog"
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(api_base.rstrip("/") + "/api/v1/knowledge" + endpoint, params=options)
        if response.status_code == 404:
            return ("Không tìm thấy nội dung | BTE", TITLE,
                    f'<h1>Không tìm thấy nội dung</h1>{link(TITLE, "/knowledge")}'), 404
        response.raise_for_status()
        data = response.json()
    except (httpx.HTTPError, ValueError):
        return ("Thư viện tạm thời gián đoạn | BTE", TITLE,
                f'<h1>{TITLE}</h1><p>Chưa tải được nội dung. Vui lòng thử lại sau.</p>'), 503

    search = (
        '<form action="/knowledge" method="get" class="panel library-search" role="search">'
        '<label for="libraryQuery">Tìm trong thư viện kiến thức</label><div class="library-search-row">'
        f'<input id="libraryQuery" type="search" name="q" maxlength="120" value="{escape(query if not identifier else "")}" />'
        '<button type="submit">Tìm kiếm</button></div></form>'
    )
    crumbs = f'<nav class="library-breadcrumbs" aria-label="Vị trí trong thư viện">{link(TITLE, "/knowledge")}</nav>'
    description = "Thư viện kiến thức phong thủy BTE với bài viết theo chuyên mục."
    title = TITLE
    if identifier is not None:
        a = data["article"]
        if a.get("slug") and identifier != a["slug"]:
            return lesson_url(a), 301
        title, description = a["title"], a["summary"] or " ".join(a["body"].split())[:160]
        nearby = []
        for key, label in (("previous", "Bài trước"), ("next", "Bài tiếp theo")):
            if item := data.get(key):
                nearby.append(link(f'{label} · {item["title"]}', lesson_url(item)))
        body = (
            f'<p>{link(a["category_title"], category_url(a["category_id"]))} · {escape(a["group_title"])}</p>'
            f'<article class="panel library-reading"><h1>{escape(title)}</h1>'
            f'<p class="muted">Biên soạn {escape(a["author_name"] or "BTE")}</p>'
            f'<p class="library-summary">{escape(a["summary"])}</p>'
            f'<div class="library-prose">{prose(a["body"])}</div></article>'
            f'<nav class="library-lesson-navigation" aria-label="Bài liên quan">{"".join(nearby)}</nav>'
        )
    elif query:
        title = "Tìm kiếm kiến thức phong thủy"
        def search_url(number):
            return "/knowledge?" + urlencode({"q": query, "page": number})
        paging = link("← Trang trước", search_url(page - 1)) if page > 1 else ""
        if page * data["limit"] < data["total"]:
            paging += link("Trang sau →", search_url(page + 1))
        body = f'<h1>Kết quả cho “{escape(query)}”</h1>{article_cards(data["items"])}<nav class="library-actions">{paging}</nav>'
    elif category_id:
        c = data["category"]
        title, description = c["title"], c["description"] or description
        groups = []
        for group in c["groups"]:
            content = article_cards(group["articles"])
            if group["is_faq"]:
                discussion = {"category": c["id"]}
                if params.get("question"):
                    discussion["topic"] = params["question"]
                content += link("Hỏi đáp chuyên mục dành cho thành viên", "/community?" + urlencode(discussion))
            groups.append(
                f'<details class="library-group"{" open" if group["articles"] or (group["is_faq"] and params.get("question")) else ""}>'
                f'<summary>{escape(group["title"])}</summary><div class="library-group-content">'
                f'<p>{escape(group["description"])}</p>{content}</div></details>'
            )
        body = f'<header class="panel library-category-intro"><h1>{escape(title)}</h1><p>{escape(description)}</p></header>' + "".join(groups)
    else:
        categories = "".join(
            f'<a class="library-category-card" href="{escape(category_url(c["id"]))}"><h3>{escape(c["title"])}</h3>'
            f'<p>{escape(c["description"])}</p><small>{c["article_count"]} bài đã đăng</small></a>'
            for c in data["categories"]
        )
        body = (
            f'<header class="knowledge-hero"><h1>{TITLE}</h1><p>{description}</p></header>'
            f'<h2>Chuyên mục</h2><div class="library-categories">{categories}</div>'
            f'<section class="library-latest"><h2>Mới cập nhật</h2><div class="library-article-grid">'
            f'{article_cards(data["latest"])}</div></section>'
        )
    return (title + " | BTE", description, search + crumbs + body), 200
