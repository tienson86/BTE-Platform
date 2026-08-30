"""Render the internal Narrative Studio HTML. Read-only. Not customer Portal."""

from __future__ import annotations

import html
import json
from typing import Any

from applications.narrative_studio.approvals import StudioApproval
from applications.narrative_studio.catalog import StudioCase
from applications.narrative_studio.service import TRACE_STAGES, StudioReview

PANELS: tuple[tuple[str, str], ...] = (
    ("overview", "Overview"),
    ("consulting", "Consulting"),
    ("structured", "Structured"),
    ("trace", "Trace"),
    ("decision", "Decision"),
    ("knowledge", "Knowledge"),
    ("compare", "Compare"),
    ("contract", "Contract"),
    ("quality", "Quality"),
    ("golden", "Golden"),
    ("approval", "Approval"),
)


def render_studio(
    *,
    cases: tuple[StudioCase, ...],
    review: StudioReview,
    panel: str,
    approval: StudioApproval | None,
    history: list[StudioApproval],
    notice: str = "",
) -> str:
    """Return a complete HTML document for one case + panel."""
    active = panel if panel in {item[0] for item in PANELS} else "overview"
    body = _panel_html(review, active, approval, history)
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8" />
  <meta name="robots" content="noindex,nofollow" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Narrative Studio — {html.escape(review.case_id)} — INTERNAL</title>
  <link rel="stylesheet" href="/static/studio.css" />
</head>
<body data-studio="narrative-v2" data-panel="{html.escape(active)}">
  <header class="ns-banner">
    <p class="ns-kicker">INTERNAL · SHADOW MODE · NOT CUSTOMER PORTAL</p>
    <h1>Narrative Studio</h1>
    <p>Read-only review workspace. Does not modify Narrative or Knowledge.</p>
  </header>
  <div class="ns-shell">
    <aside class="ns-side">
      <h2>Case</h2>
      <form method="get" action="/studio">
        <input type="hidden" name="panel" value="{html.escape(active)}" />
        <select name="case" onchange="this.form.submit()" data-studio-case>
          {_case_options(cases, review.case_id)}
        </select>
      </form>
      <p class="ns-muted">{html.escape(review.full_name)}</p>
      <nav>
        {_nav(review.case_id, active)}
      </nav>
    </aside>
    <main class="ns-main">
      {f'<p class="ns-notice">{html.escape(notice)}</p>' if notice else ''}
      {body}
    </main>
  </div>
</body>
</html>
"""


def _case_options(cases: tuple[StudioCase, ...], current: str) -> str:
    rows = []
    for case in cases:
        selected = " selected" if case.case_id == current else ""
        rows.append(
            f'<option value="{html.escape(case.case_id)}"{selected}>{html.escape(case.case_id)}</option>'
        )
    return "\n".join(rows)


def _nav(case_id: str, active: str) -> str:
    links = []
    for key, label in PANELS:
        current = ' aria-current="page"' if key == active else ""
        links.append(
            f'<a href="/studio?case={html.escape(case_id)}&panel={key}"{current}>{html.escape(label)}</a>'
        )
    return "\n".join(links)


def _panel_html(
    review: StudioReview,
    panel: str,
    approval: StudioApproval | None,
    history: list[StudioApproval],
) -> str:
    if panel == "overview":
        return _overview(review)
    if panel == "consulting":
        return _consulting(review)
    if panel == "structured":
        return _structured(review)
    if panel == "trace":
        return _trace(review)
    if panel == "decision":
        return _decision(review)
    if panel == "knowledge":
        return _knowledge(review)
    if panel == "compare":
        return _compare(review)
    if panel == "contract":
        return _contract(review)
    if panel == "quality":
        return _quality(review)
    if panel == "golden":
        return _golden(review)
    return _approval(review, approval, history)


def _overview(review: StudioReview) -> str:
    pres = review.presentation or {}
    overview = pres.get("overview") if isinstance(pres.get("overview"), dict) else {}
    interpretation = pres.get("interpretation") if isinstance(pres.get("interpretation"), dict) else {}
    action = pres.get("action_plan") if isinstance(pres.get("action_plan"), dict) else {}
    meta = pres.get("metadata") if isinstance(pres.get("metadata"), dict) else {}
    return f"""
<section class="ns-card" data-studio-panel="overview">
  <h2>Overview</h2>
  <p>status: <strong>{_e(pres.get("status"))}</strong> · version: <strong>{_e(meta.get("version"))}</strong></p>
  <p>runtime: {_e(review.runtime_status)} · commercial: {_e(pres.get("commercial"))}</p>
  <h3>Summary</h3>
  <p>{_e(overview.get("headline"))}</p>
  <p>{_e(overview.get("summary"))}</p>
  <p class="ns-muted">identity: {_e(overview.get("identity"))} · balance: {_e(overview.get("balance"))} · conclusion: {_e(overview.get("conclusion"))}</p>
  <h3>Interpretation</h3>
  <p>{_e(interpretation.get("consulting_flow"))}</p>
  <h3>Action</h3>
  {_action_block(action)}
  <h3>Commercial</h3>
  <p class="ns-muted">null — Commercial Builder not implemented</p>
</section>
"""


def _consulting(review: StudioReview) -> str:
    return f"""
<section class="ns-card" data-studio-panel="consulting">
  <h2>Consulting View</h2>
  <p class="ns-muted">consulting_flow exactly as packaged. No rewrite.</p>
  <blockquote data-studio-consulting-flow>{_e(review.consulting_flow)}</blockquote>
</section>
"""


def _structured(review: StudioReview) -> str:
    rows = []
    for key in ("observation", "reasoning", "meaning", "impact", "recommendation", "closing"):
        rows.append(f"<h3>{html.escape(key.title())}</h3><p>{_e(review.structured.get(key))}</p>")
    return f"""
<section class="ns-card" data-studio-panel="structured">
  <h2>Structured View</h2>
  {''.join(rows)}
</section>
"""


def _trace(review: StudioReview) -> str:
    blocks = []
    for stage in TRACE_STAGES:
        rows = review.trace.get(stage) or []
        inner = _json_pre(rows)
        blocks.append(
            f'<details data-studio-trace="{html.escape(stage)}"><summary>{html.escape(stage.title())} ({len(rows)})</summary>{inner}</details>'
        )
    return f"""
<section class="ns-card" data-studio-panel="trace">
  <h2>Trace View</h2>
  <p class="ns-muted">Evidence → Reasoning → Knowledge → Rewrite → Conversation → Consulting → Presentation. Read only.</p>
  {''.join(blocks)}
</section>
"""


def _decision(review: StudioReview) -> str:
    decision_html = _json_pre(review.decisions)
    action_html = _json_pre(review.actions)
    return f"""
<section class="ns-card" data-studio-panel="decision">
  <h2>Decision View</h2>
  <p class="ns-muted">Decision → Priority → Actions. Trace each Action. Read only.</p>
  <h3>Decisions</h3>
  {decision_html}
  <h3>Priority and Actions</h3>
  {action_html}
</section>
"""


def _knowledge(review: StudioReview) -> str:
    return f"""
<section class="ns-card" data-studio-panel="knowledge">
  <h2>Knowledge View</h2>
  <p>status: {_e(review.knowledge.get("status"))}</p>
  <h3>Knowledge ids</h3>
  {_json_pre(review.knowledge.get("ids") or [])}
  <h3>Approved</h3>
  {_json_pre(review.knowledge.get("approved") or [])}
  <h3>Unresolved</h3>
  {_json_pre(review.knowledge.get("unresolved") or [])}
  <h3>Contract gaps</h3>
  {_json_pre(review.knowledge.get("contract_gaps") or [])}
</section>
"""


def _compare(review: StudioReview) -> str:
    overview = {}
    if isinstance(review.presentation, dict) and isinstance(review.presentation.get("overview"), dict):
        overview = review.presentation["overview"]
    headline = overview.get("headline") if isinstance(overview, dict) else None
    return f"""
<section class="ns-compare" data-studio-panel="compare">
  <article class="ns-card">
    <h2>Pack05</h2>
    {_json_pre(review.pack05)}
  </article>
  <article class="ns-card">
    <h2>Narrative V2</h2>
    <p>{_e(headline)}</p>
    <blockquote>{_e(review.consulting_flow)}</blockquote>
  </article>
</section>
"""


def _contract(review: StudioReview) -> str:
    return f"""
<section class="ns-card" data-studio-panel="contract">
  <h2>Contract View</h2>
  {_json_pre(review.contract)}
</section>
"""


def _quality(review: StudioReview) -> str:
    return f"""
<section class="ns-card" data-studio-panel="quality">
  <h2>Quality View</h2>
  {_json_pre(review.quality)}
</section>
"""


def _golden(review: StudioReview) -> str:
    note = (
        "Compared to frozen N-IMP-09A Presentation snapshot. Golden Dataset files are not modified."
        if review.golden_available
        else "No frozen V2 Presentation snapshot for this case. Golden Dataset was not created or edited."
    )
    return f"""
<section class="ns-card" data-studio-panel="golden">
  <h2>Golden View</h2>
  <p class="ns-muted">{html.escape(note)}</p>
  <p>differences: {len(review.golden_diffs)}</p>
  {_json_pre(review.golden_diffs)}
</section>
"""


def _approval(
    review: StudioReview,
    approval: StudioApproval | None,
    history: list[StudioApproval],
) -> str:
    current = (
        f"<p>Latest: <strong>{html.escape(approval.verdict)}</strong> · {html.escape(approval.reviewer)} · {html.escape(approval.timestamp)}</p><p>{html.escape(approval.comment)}</p>"
        if approval
        else "<p class='ns-muted'>No internal approval recorded.</p>"
    )
    past = "".join(
        f"<li>{html.escape(row.timestamp)} · {html.escape(row.verdict)} · {html.escape(row.reviewer)}</li>"
        for row in reversed(history)
    )
    return f"""
<section class="ns-card" data-studio-panel="approval">
  <h2>Approval Panel</h2>
  <p class="ns-muted">Internal only. Records studio review metadata. Does not change Narrative or Knowledge.</p>
  {current}
  <form method="post" action="/studio/approval" data-studio-approval>
    <input type="hidden" name="case" value="{html.escape(review.case_id)}" />
    <label>Verdict
      <select name="verdict">
        <option>PASS</option>
        <option>REVIEW</option>
        <option>REJECT</option>
      </select>
    </label>
    <label>Reviewer <input name="reviewer" value="product-owner" /></label>
    <label>Comment <textarea name="comment" rows="4"></textarea></label>
    <button type="submit">Record internal review</button>
  </form>
  <h3>History</h3>
  <ul>{past or '<li class="ns-muted">empty</li>'}</ul>
</section>
"""


def _action_block(action: dict[str, Any]) -> str:
    top = action.get("top_priority") if isinstance(action.get("top_priority"), dict) else {}
    title = top.get("title") if isinstance(top, dict) else None
    description = top.get("description") if isinstance(top, dict) else None
    return f"<p><strong>{_e(title)}</strong></p><p>{_e(description)}</p>"


def _json_pre(value: object) -> str:
    text = json.dumps(value, ensure_ascii=False, indent=2)
    return f'<pre>{html.escape(text)}</pre>'


def _e(value: object) -> str:
    if value is None:
        return "<em>null</em>"
    return html.escape(str(value))
