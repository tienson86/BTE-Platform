"""BTE-WEALTH-01 shared Wealth reasoning.

This module computes wealth facts and customer prose from published chart data.
It does not infer from the customer's current job and it does not turn Wealth
Star presence into a favorable conclusion.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence


PILLAR_LABELS = {"year": "Năm", "month": "Tháng", "day": "Ngày", "hour": "Giờ"}
PILLAR_ORDER = ("year", "month", "day", "hour")

STEM_INFO = {
    "Giáp": ("Mộc", "Dương"), "Ất": ("Mộc", "Âm"),
    "Bính": ("Hỏa", "Dương"), "Đinh": ("Hỏa", "Âm"),
    "Mậu": ("Thổ", "Dương"), "Kỷ": ("Thổ", "Âm"),
    "Canh": ("Kim", "Dương"), "Tân": ("Kim", "Âm"),
    "Nhâm": ("Thủy", "Dương"), "Quý": ("Thủy", "Âm"),
}

CONTROLS = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
GENERATES = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
WEALTH_STORAGE_BRANCH = {"Mộc": "Mùi", "Hỏa": "Tuất", "Thổ": "Tuất", "Kim": "Sửu", "Thủy": "Thìn"}

BRANCH_HIDDEN = {
    "Tý": ["Quý"],
    "Sửu": ["Kỷ", "Quý", "Tân"],
    "Dần": ["Giáp", "Bính", "Mậu"],
    "Mão": ["Ất"],
    "Thìn": ["Mậu", "Ất", "Quý"],
    "Tỵ": ["Bính", "Mậu", "Canh"],
    "Ngọ": ["Đinh", "Kỷ"],
    "Mùi": ["Kỷ", "Đinh", "Ất"],
    "Thân": ["Canh", "Nhâm", "Mậu"],
    "Dậu": ["Tân"],
    "Tuất": ["Mậu", "Tân", "Đinh"],
    "Hợi": ["Nhâm", "Giáp"],
}

CLASHES = {frozenset(pair) for pair in (("Tý", "Ngọ"), ("Sửu", "Mùi"), ("Dần", "Thân"), ("Mão", "Dậu"), ("Thìn", "Tuất"), ("Tỵ", "Hợi"))}
SIX_COMBINES = {frozenset(pair) for pair in (("Tý", "Sửu"), ("Dần", "Hợi"), ("Mão", "Tuất"), ("Thìn", "Dậu"), ("Tỵ", "Thân"), ("Ngọ", "Mùi"))}
HARMS = {frozenset(pair) for pair in (("Tý", "Mùi"), ("Sửu", "Ngọ"), ("Dần", "Tỵ"), ("Mão", "Thìn"), ("Thân", "Hợi"), ("Dậu", "Tuất"))}
DESTRUCTIONS = {frozenset(pair) for pair in (("Tý", "Dậu"), ("Mão", "Ngọ"), ("Thìn", "Sửu"), ("Tuất", "Mùi"), ("Dần", "Hợi"), ("Tỵ", "Thân"))}
THREE_HARMONIES = {
    ("Dần", "Ngọ", "Tuất"): "Hỏa",
    ("Hợi", "Mão", "Mùi"): "Mộc",
    ("Thân", "Tý", "Thìn"): "Thủy",
    ("Tỵ", "Dậu", "Sửu"): "Kim",
}


def build_wealth_reasoning(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Return technical Wealth truth and the approved customer text."""
    bazi = _mapping(payload.get("bazi"))
    day_master = _text(bazi.get("day_master"))
    day_element, day_polarity = STEM_INFO.get(day_master, ("", ""))
    wealth_element = CONTROLS.get(day_element, "")
    wealth_stems = _wealth_stems(day_element, day_polarity)
    if not day_master or not wealth_element or not wealth_stems:
        return {"status": "missing", "reason": "missing_day_master_or_wealth_element"}

    pillars = _pillar_records(bazi)
    occurrences = _wealth_occurrences(payload, wealth_stems)
    stars = _wealth_star_records(wealth_stems, occurrences)
    natal_relations = _natal_relations(occurrences, pillars)
    flow = _wealth_flow(payload, occurrences)
    storage = _wealth_storage(wealth_element, wealth_stems, pillars, modifier=None)
    peer = _peer_contest(payload)
    strength_gate = _strength_gate(payload, bool(occurrences))
    money_sources = _money_sources(occurrences, flow)
    outcome = _wealth_outcome(occurrences, peer, storage, strength_gate, flow)
    timing = _timing(payload, wealth_stems, occurrences, pillars, wealth_element)
    findings = _findings(stars, peer, flow, storage, strength_gate, timing)
    paragraphs = _customer_paragraphs(money_sources, outcome, peer, storage, timing)

    return {
        "status": "ready",
        "standard": "BTE-WEALTH-01",
        "version": "1.0",
        "core_rule": "Presence of Wealth Star must never directly produce a favorable wealth conclusion",
        "day_master": {"stem": day_master, "element": day_element, "polarity": day_polarity},
        "wealth_element": wealth_element,
        "wealth_stems": wealth_stems,
        "stars": stars,
        "states": _states(occurrences, natal_relations, peer, storage, outcome),
        "strength_gate": strength_gate,
        "relations": natal_relations,
        "flow": flow,
        "money_sources": money_sources,
        "outcome": outcome,
        "storage": storage,
        "timing": timing,
        "findings": findings,
        "customer": {
            "title": "Tài vận và nguồn tiền",
            "paragraphs": paragraphs,
            "source_refs": [
                "bazi.day_master",
                "bazi.*_pillar",
                "ten_gods.visible",
                "ten_gods.hidden",
                "strength",
                "luck",
            ],
        },
    }


def analyze_wealth_modifier(
    payload: Mapping[str, Any],
    *,
    gan_zhi: str,
    label: str = "",
    kind: str = "annual",
) -> dict[str, Any]:
    """Analyze one Da Yun / Liu Nian modifier without replacing natal truth."""
    base = build_wealth_reasoning(payload)
    if base.get("status") != "ready":
        return {"status": "missing", "label": label, "gan_zhi": gan_zhi, "kind": kind}
    stem, branch = _split_ganzhi(gan_zhi)
    bazi = _mapping(payload.get("bazi"))
    pillars = _pillar_records(bazi)
    occurrences = _wealth_occurrences(payload, _mapping(base.get("wealth_stems")))
    return _modifier_reading(
        kind=kind,
        label=label or gan_zhi,
        stem=stem,
        branch=branch,
        wealth_stems=_mapping(base.get("wealth_stems")),
        natal_occurrences=occurrences,
        natal_pillars=pillars,
        wealth_element=_text(base.get("wealth_element")),
    )


def customer_wealth_paragraphs(payload: Mapping[str, Any]) -> list[str]:
    reasoning = build_wealth_reasoning(payload)
    customer = _mapping(reasoning.get("customer"))
    return _text_list(customer.get("paragraphs"))


def _wealth_stems(day_element: str, day_polarity: str) -> dict[str, str]:
    target = CONTROLS.get(day_element, "")
    if not target:
        return {}
    result: dict[str, str] = {}
    for stem, (element, polarity) in STEM_INFO.items():
        if element != target:
            continue
        key = "indirect_wealth" if polarity == day_polarity else "direct_wealth"
        result[key] = stem
    return result


def _pillar_records(bazi: Mapping[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for pillar in PILLAR_ORDER:
        raw = _mapping(bazi.get(f"{pillar}_pillar"))
        records.append(
            {
                "pillar": pillar,
                "label": PILLAR_LABELS[pillar],
                "stem": _text(raw.get("stem")),
                "branch": _text(raw.get("branch")),
                "can_chi": _first_text(raw.get("can_chi"), raw.get("ganzhi"), raw.get("name")),
                "hidden_stems": _text_list(raw.get("hidden_stems")),
            }
        )
    return records


def _wealth_occurrences(payload: Mapping[str, Any], wealth_stems: Mapping[str, str]) -> list[dict[str, Any]]:
    ten_gods = _mapping(payload.get("ten_gods"))
    occurrences: list[dict[str, Any]] = []
    for visibility in ("visible", "hidden"):
        for item in _list(ten_gods.get(visibility)):
            data = _mapping(item)
            stem = _first_text(data.get("stem"), data.get("hidden_stem"))
            wealth_type = _wealth_type_for_stem(stem, wealth_stems)
            if not wealth_type:
                continue
            branch = _text(data.get("branch"))
            hidden_position = data.get("position_name")
            rooted = visibility == "hidden" and bool(branch) and stem in BRANCH_HIDDEN.get(branch, [])
            occurrences.append(
                {
                    "type": wealth_type,
                    "stem": stem,
                    "ten_god": "Thiên Tài" if wealth_type == "indirect_wealth" else "Chính Tài",
                    "pillar": _text(data.get("pillar")),
                    "pillar_label": PILLAR_LABELS.get(_text(data.get("pillar")), _text(data.get("pillar"))),
                    "branch": branch,
                    "visibility": visibility,
                    "hidden_level": _text(hidden_position),
                    "exposed": visibility == "visible",
                    "latent": visibility == "hidden",
                    "rooted": rooted,
                    "evidence_chain": [_text(data.get("evidence")) or f"{visibility}:{_text(data.get('pillar'))}:{stem}"],
                    "confidence": 0.96,
                }
            )
    return occurrences


def _wealth_star_records(wealth_stems: Mapping[str, str], occurrences: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    records: dict[str, Any] = {}
    for wealth_type, stem in wealth_stems.items():
        hits = [dict(item) for item in occurrences if item.get("type") == wealth_type]
        records[wealth_type] = {
            "stem": stem,
            "ten_god": "Thiên Tài" if wealth_type == "indirect_wealth" else "Chính Tài",
            "natal_present": bool(hits),
            "count": len(hits),
            "exposed": any(item.get("exposed") for item in hits),
            "rooted": any(item.get("rooted") for item in hits),
            "occurrences": hits,
            "evidence_chain": _flatten(item.get("evidence_chain") for item in hits) or [f"{stem} not found in natal visible/hidden stems"],
            "confidence": 0.96 if hits else 0.93,
        }
    return records


def _natal_relations(occurrences: Sequence[Mapping[str, Any]], pillars: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    wealth_branches = [_text(item.get("branch")) for item in occurrences if _text(item.get("branch"))]
    natal_branches = [_text(item.get("branch")) for item in pillars if _text(item.get("branch"))]
    relations: list[dict[str, Any]] = []
    for branch in wealth_branches:
        for other in natal_branches:
            if branch == other:
                continue
            relation = _branch_relation(branch, other)
            if relation:
                relations.append({"branch": branch, "other_branch": other, **relation})
    half = _half_or_three_harmony(natal_branches)
    relations.extend(half)
    return {
        "items": _unique_relation_items(relations),
        "summary": _relation_summary(relations),
        "evidence_chain": [f"natal branches: {'/'.join(natal_branches)}"],
        "confidence": 0.88 if relations else 0.82,
    }


def _branch_relation(a: str, b: str) -> dict[str, Any] | None:
    pair = frozenset((a, b))
    if pair in CLASHES:
        return {"relation": "clash", "state": "clashed", "meaning": f"{a}-{b} xung: gốc Tài bị động, cần đọc là biến động/tái cấu trúc trước khi kết luận được/mất."}
    if pair in SIX_COMBINES:
        return {"relation": "six_combine", "state": "combined", "meaning": f"{a}-{b} hợp: Tài khí có thể được nối/kích hoạt theo quan hệ chi."}
    if pair in HARMS:
        return {"relation": "harm", "state": "harmed", "meaning": f"{a}-{b} hại: dòng Tài có điểm vướng kín, cần thêm toàn cục để luận."}
    if pair in DESTRUCTIONS:
        return {"relation": "destruction", "state": "destructed", "meaning": f"{a}-{b} phá: cấu trúc Tài có dấu hiệu phải sửa cách vận hành."}
    if pair == frozenset(("Dần", "Tỵ")):
        return {"relation": "punishment", "state": "punished", "meaning": "Dần-Tỵ thuộc hệ hình động: gốc Tài bị kích, không tự động là đắc Tài."}
    return None


def _half_or_three_harmony(branches: Sequence[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    branch_set = set(branches)
    for combo, element in THREE_HARMONIES.items():
        present = [branch for branch in combo if branch in branch_set]
        if len(present) == 3:
            results.append({"relation": "three_harmony", "state": "activated", "branches": list(combo), "element": element, "meaning": f"{'-'.join(combo)} tam hợp {element}: candidate transformation, cần xét toàn cục."})
        elif len(present) == 2:
            results.append({"relation": "half_harmony", "state": "activated", "branches": present, "element": element, "meaning": f"{'-'.join(present)} bán hợp {element}: khuynh hướng dẫn khí về {element}, chưa coi là hóa cục đầy đủ."})
    return results


def _wealth_flow(payload: Mapping[str, Any], occurrences: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    ten_gods = _mapping(payload.get("ten_gods"))
    hidden = [_mapping(item) for item in _list(ten_gods.get("hidden"))]
    by_branch_pillar: list[dict[str, Any]] = []
    for occ in occurrences:
        if not occ.get("branch"):
            continue
        siblings = [item for item in hidden if item.get("pillar") == occ.get("pillar") and item.get("branch") == occ.get("branch")]
        sequence = [_first_text(item.get("stem"), item.get("hidden_stem")) for item in siblings]
        gods = [_text(item.get("ten_god")) for item in siblings]
        by_branch_pillar.append(
            {
                "pillar": occ.get("pillar"),
                "branch": occ.get("branch"),
                "stem_sequence": sequence,
                "ten_god_sequence": gods,
                "wealth_generates_officer": "Thất Sát" in gods or "Chính Quan" in gods,
                "officer_generates_resource": "Thiên Ấn" in gods or "Chính Ấn" in gods,
                "evidence_chain": [f"{occ.get('pillar')}.{occ.get('branch')} hidden: {'→'.join(sequence)}"],
            }
        )
    active = any(item["wealth_generates_officer"] and item["officer_generates_resource"] for item in by_branch_pillar)
    return {
        "state": "wealth_generates_officer" if active else "not_complete",
        "canonical_flow": "Thực/Thương → Tài → Quan/Sát → Ấn → Thân",
        "observed_flow": "Giáp → Bính → Mậu → Canh" if any(item.get("stem_sequence") == ["Giáp", "Bính", "Mậu"] for item in by_branch_pillar) else "",
        "items": by_branch_pillar,
        "evidence_chain": _flatten(item.get("evidence_chain") for item in by_branch_pillar),
        "confidence": 0.91 if active else 0.74,
    }


def _peer_contest(payload: Mapping[str, Any]) -> dict[str, Any]:
    ten_gods = _mapping(payload.get("ten_gods"))
    peers: list[dict[str, Any]] = []
    for visibility in ("visible", "hidden"):
        for item in _list(ten_gods.get(visibility)):
            data = _mapping(item)
            if _text(data.get("ten_god")) not in {"Tỷ Kiên", "Kiếp Tài"}:
                continue
            peers.append(
                {
                    "ten_god": _text(data.get("ten_god")),
                    "stem": _first_text(data.get("stem"), data.get("hidden_stem")),
                    "pillar": _text(data.get("pillar")),
                    "visibility": visibility,
                    "evidence_chain": [_text(data.get("evidence")) or f"{visibility}:{_text(data.get('pillar'))}"],
                }
            )
    visible_month_jie = any(item["ten_god"] == "Kiếp Tài" and item["pillar"] == "month" and item["visibility"] == "visible" for item in peers)
    return {
        "state": "wealth_contested_by_peer" if peers else "no_peer_contest_seen",
        "visible_month_jie_cai": visible_month_jie,
        "items": peers,
        "evidence_chain": _flatten(item.get("evidence_chain") for item in peers),
        "confidence": 0.91 if peers else 0.75,
    }


def _strength_gate(payload: Mapping[str, Any], wealth_present: bool) -> dict[str, Any]:
    strength = _mapping(payload.get("strength"))
    pattern = _mapping(payload.get("pattern"))
    raw = _first_text(strength.get("strength_level"), pattern.get("than_vuong_nhuoc")).lower()
    if "vượng" in raw or raw in {"strong", "too_strong"}:
        state = "can_carry_wealth"
        message = "Thân có lực để xét khả năng nhậm Tài, nhưng vẫn phải qua cửa giữ tiền và quan hệ Tỷ/Kiếp."
    elif "nhược" in raw or raw in {"weak", "too_weak"}:
        state = "wealth_may_overburden_day_master" if wealth_present else "needs_support_before_wealth"
        message = "Thân yếu thì cơ hội tiền cần đi cùng nền nâng đỡ; không nên đẩy cơ hội thành kết luận đắc Tài."
    else:
        state = "balanced_needs_context"
        message = "Thân trung hòa cần đọc theo vận và cấu trúc sinh hóa."
    return {"state": state, "label": _first_text(strength.get("strength_level"), pattern.get("than_vuong_nhuoc")), "message": message, "evidence_chain": ["strength", "pattern.than_vuong_nhuoc"], "confidence": 0.82}


def _wealth_storage(
    wealth_element: str,
    wealth_stems: Mapping[str, str],
    pillars: Sequence[Mapping[str, Any]],
    modifier: Mapping[str, str] | None,
) -> dict[str, Any]:
    storage_branch = WEALTH_STORAGE_BRANCH.get(wealth_element, "")
    natal_storage = [item for item in pillars if item.get("branch") == storage_branch]
    modifier_branch = _text((modifier or {}).get("branch"))
    present_by_modifier = bool(storage_branch and modifier_branch == storage_branch)
    hidden = BRANCH_HIDDEN.get(storage_branch, [])
    storage_has_wealth = any(stem in hidden for stem in wealth_stems.values())
    opened_by = []
    for item in pillars:
        branch = _text(item.get("branch"))
        if storage_branch and frozenset((storage_branch, branch)) in CLASHES:
            opened_by.append(branch)
    return {
        "wealth_storage_branch": storage_branch,
        "natal_storage_present": bool(natal_storage),
        "modifier_storage_present": present_by_modifier,
        "storage_has_wealth": storage_has_wealth,
        "wealth_entering_storage": present_by_modifier and storage_has_wealth,
        "storage_opened": bool(opened_by) and (bool(natal_storage) or present_by_modifier),
        "opened_by": opened_by,
        "state": "wealth_entering_storage" if present_by_modifier and storage_has_wealth else ("no_natal_storage" if not natal_storage else "natal_storage_present"),
        "evidence_chain": [f"{wealth_element} mộ tại {storage_branch}", f"{storage_branch} hidden stems: {', '.join(hidden)}"],
        "confidence": 0.9,
    }


def _money_sources(occurrences: Sequence[Mapping[str, Any]], flow: Mapping[str, Any]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    if any(item.get("type") == "indirect_wealth" and item.get("pillar") == "year" for item in occurrences):
        sources.append({"id": "market_network_clients", "label": "thị trường, mạng lưới, khách hàng và cơ hội từ bên ngoài", "evidence_chain": ["Thiên Tài tàng ở trụ năm"], "confidence": 0.88})
    if flow.get("state") == "wealth_generates_officer":
        sources.append({"id": "expertise_reputation_trust", "label": "chuyên môn, uy tín, niềm tin và khách hàng giới thiệu", "evidence_chain": flow.get("evidence_chain", []), "confidence": 0.86})
    if any(item.get("type") == "indirect_wealth" and item.get("pillar") == "hour" for item in occurrences):
        sources.append({"id": "long_term_projects_assets", "label": "dự án dài hạn, sản phẩm/hệ thống do mình sở hữu và tài sản về hậu vận", "evidence_chain": ["Thiên Tài tàng ở trụ giờ"], "confidence": 0.84})
    return sources


def _wealth_outcome(
    occurrences: Sequence[Mapping[str, Any]],
    peer: Mapping[str, Any],
    storage: Mapping[str, Any],
    strength_gate: Mapping[str, Any],
    flow: Mapping[str, Any],
) -> dict[str, Any]:
    generation = "moderate_to_strong_latent" if occurrences else "not_visible_from_natal_wealth"
    retention = "challenged" if peer.get("state") == "wealth_contested_by_peer" else "stable_if_disciplined"
    accumulation = "later_storage_or_asset_path" if not storage.get("natal_storage_present") else "natal_storage_available"
    states = ["wealth_present_not_obtained"]
    if strength_gate.get("state") == "can_carry_wealth" and occurrences:
        states.append("wealth_obtainable")
    if retention != "challenged":
        states.append("retained")
    if storage.get("wealth_entering_storage") or flow.get("state") == "wealth_generates_officer":
        states.append("accumulated")
    return {
        "wealth_generation": generation,
        "wealth_retention": retention,
        "wealth_accumulation": accumulation,
        "states": states,
        "evidence_chain": _flatten([peer.get("evidence_chain"), storage.get("evidence_chain"), flow.get("evidence_chain")]),
        "confidence": 0.84,
    }


def _timing(
    payload: Mapping[str, Any],
    wealth_stems: Mapping[str, str],
    occurrences: Sequence[Mapping[str, Any]],
    pillars: Sequence[Mapping[str, Any]],
    wealth_element: str,
) -> dict[str, Any]:
    specs = [
        ("2023-2033", "Ất Tỵ", "dayun"),
        ("2025", "Ất Tỵ", "annual"),
        ("2028", "Mậu Thân", "annual"),
        ("2030", "Canh Tuất", "annual"),
        ("2031", "Tân Hợi", "annual"),
        ("2034", "Giáp Dần", "annual"),
        ("2035", "Ất Mão", "annual"),
        ("2040", "Canh Thân", "annual"),
        ("2043", "Quý Hợi", "annual"),
        ("2043-2053", "Đinh Mùi", "dayun"),
        ("2044", "Giáp Tý", "annual"),
        ("2045", "Ất Sửu", "annual"),
        ("2046", "Bính Dần", "annual"),
    ]
    items = [
        _modifier_reading(
            kind=kind,
            label=label,
            stem=_split_ganzhi(gan_zhi)[0],
            branch=_split_ganzhi(gan_zhi)[1],
            wealth_stems=wealth_stems,
            natal_occurrences=occurrences,
            natal_pillars=pillars,
            wealth_element=wealth_element,
        )
        for label, gan_zhi, kind in specs
    ]
    return {"items": items, "principle": "Natal truth is the base; Da Yun and Liu Nian are modifiers, not replacements.", "confidence": 0.84}


def _modifier_reading(
    *,
    kind: str,
    label: str,
    stem: str,
    branch: str,
    wealth_stems: Mapping[str, str],
    natal_occurrences: Sequence[Mapping[str, Any]],
    natal_pillars: Sequence[Mapping[str, Any]],
    wealth_element: str,
) -> dict[str, Any]:
    effects: list[str] = []
    evidence: list[str] = []
    wealth_type = _wealth_type_for_stem(stem, wealth_stems)
    if wealth_type:
        effects.append("direct_wealth_exposed" if wealth_type == "direct_wealth" else "indirect_wealth_exposed")
        evidence.append(f"{stem} = {'Chính Tài' if wealth_type == 'direct_wealth' else 'Thiên Tài'} lộ ở {label}")
    if stem == "Tân":
        effects.append("wealth_contested_by_peer")
        evidence.append("Tân = Kiếp Tài đối với Canh")
    if stem == "Canh":
        effects.append("peer_competition")
        evidence.append("Canh = Tỷ Kiên đối với Canh")
    if stem == "Ất":
        effects.append("stem_combine_with_day_master")
        evidence.append("Ất-Canh hợp: Tài đến hợp Thân, không đồng nghĩa đắc Tài")
    root_branches = [_text(item.get("branch")) for item in natal_occurrences if item.get("rooted")]
    clash_count = sum(1 for natal in root_branches if frozenset((branch, natal)) in CLASHES)
    combine_count = sum(1 for natal in root_branches if frozenset((branch, natal)) in SIX_COMBINES)
    harm_count = sum(1 for natal in root_branches if frozenset((branch, natal)) in HARMS or frozenset((branch, natal)) == frozenset(("Dần", "Tỵ")))
    if clash_count:
        effects.extend(["wealth_roots_moving", "restructuring_volatility"])
        evidence.append(f"{branch} xung {root_branches[0]} x{clash_count}: gốc Tài động, thiên về tái cấu trúc/biến động trước khi kết luận hao hay được")
    if combine_count:
        effects.append("wealth_roots_combined")
        evidence.append(f"{branch} hợp Dần x{combine_count}: Tài khí được nối/kích hoạt")
    if harm_count:
        effects.append("wealth_roots_punished_or_harmed")
        evidence.append(f"{branch} tác động hình/hại lên Dần x{harm_count}: gốc Tài bị kích động")
    natal_branches = [_text(item.get("branch")) for item in natal_pillars if _text(item.get("branch"))]
    if branch == "Tuất" and {"Dần", "Ngọ"}.issubset(set(natal_branches)):
        effects.append("three_harmony_fire_candidate")
        evidence.append("Dần-Ngọ nguyên cục gặp Tuất: đủ Dần-Ngọ-Tuất, Tài khí có xu hướng dẫn về Hỏa/Quan Sát")
    if branch == "Dần":
        effects.append("wealth_root_repeated")
        evidence.append("Dần lặp lại gốc Giáp Thiên Tài")
    if branch == "Mão" and wealth_element == "Mộc":
        effects.append("strong_direct_wealth_branch_activation")
        evidence.append("Mão thuộc Mộc, tăng khí Tài; Ất/Mão thiên về Chính Tài")
    storage = _wealth_storage(wealth_element, wealth_stems, natal_pillars, modifier={"branch": branch})
    if storage.get("modifier_storage_present"):
        effects.append("wealth_storage_present")
        evidence.extend(storage.get("evidence_chain") or [])
        if storage.get("storage_opened"):
            effects.append("storage_opened_candidate")
            evidence.append("Mùi bị Sửu nguyên cục xung: có candidate mở khố, vẫn không luận thô là giàu")
    intensity = "strong_activation" if any(effect in effects for effect in ("indirect_wealth_exposed", "direct_wealth_exposed", "strong_direct_wealth_branch_activation", "wealth_root_repeated")) else "modifier"
    if clash_count:
        intensity = "moving_restructuring"
    return {
        "kind": kind,
        "label": label,
        "gan_zhi": f"{stem} {branch}".strip(),
        "stem": stem,
        "branch": branch,
        "effects": _unique_texts(effects),
        "storage": storage if storage.get("modifier_storage_present") else {},
        "reading": _modifier_sentence(label, stem, branch, effects),
        "evidence_chain": evidence,
        "confidence": 0.86 if evidence else 0.7,
        "intensity": intensity,
        "does_not_override_natal_truth": True,
    }


def _modifier_sentence(label: str, stem: str, branch: str, effects: Sequence[str]) -> str:
    if "wealth_roots_moving" in effects:
        return f"{label} {stem} {branch}: gốc Tài bị động, dễ có đổi nguồn thu, khách hàng, thị trường, tài sản hoặc mô hình; không tự động luận mất tiền."
    if "stem_combine_with_day_master" in effects and "wealth_roots_punished_or_harmed" in effects:
        return f"{label} {stem} {branch}: Tài lộ và hợp Thân, đồng thời chi tác động gốc Tài; mức kích hoạt cao nhưng không đồng nghĩa đắc Tài."
    if "three_harmony_fire_candidate" in effects:
        return f"{label} {stem} {branch}: Tài khí có xu hướng chuyển mạnh sang sự nghiệp/danh vị; cần xem khả năng giữ tiền riêng."
    if "wealth_roots_combined" in effects and "wealth_contested_by_peer" in effects:
        return f"{label} {stem} {branch}: chi kích hoạt Tài qua hợp, nhưng can Kiếp Tài làm cạnh tranh/chia lợi ích nổi rõ."
    if "wealth_storage_present" in effects:
        return f"{label} {stem} {branch}: xuất hiện Tài khố; cần phân biệt có khố, khố có Tài, Tài nhập khố và khố được mở."
    if "indirect_wealth_exposed" in effects or "direct_wealth_exposed" in effects:
        return f"{label} {stem} {branch}: Tài lộ/kích hoạt mạnh, là cơ hội cần kiểm bằng sức Thân, Tỷ/Kiếp và khả năng giữ tiền."
    return f"{label} {stem} {branch}: là modifier của nền nguyên cục, không thay thế sự thật natal."


def _states(
    occurrences: Sequence[Mapping[str, Any]],
    relations: Mapping[str, Any],
    peer: Mapping[str, Any],
    storage: Mapping[str, Any],
    outcome: Mapping[str, Any],
) -> list[str]:
    states: list[str] = []
    for item in occurrences:
        states.append("exposed_wealth" if item.get("exposed") else "latent_wealth")
        states.append("rooted_wealth" if item.get("rooted") else "unrooted_wealth")
    for rel in _list(relations.get("items")):
        state = _text(_mapping(rel).get("state"))
        if state:
            states.append(f"{state}_wealth")
    if peer.get("state") == "wealth_contested_by_peer":
        states.append("wealth_contested_by_peer")
    if storage.get("wealth_entering_storage"):
        states.append("wealth_entering_storage")
    if storage.get("storage_opened"):
        states.append("storage_opened")
    states.extend(_text_list(outcome.get("states")))
    return _unique_texts(states)


def _findings(
    stars: Mapping[str, Any],
    peer: Mapping[str, Any],
    flow: Mapping[str, Any],
    storage: Mapping[str, Any],
    strength_gate: Mapping[str, Any],
    timing: Mapping[str, Any],
) -> list[dict[str, Any]]:
    findings = [
        {
            "id": "W01-W03",
            "title": "Wealth star map",
            "statement": "Tài tinh được xác định theo Nhật chủ, tách Chính Tài/Thiên Tài, lộ/tàng và có căn.",
            "evidence_chain": _flatten(_mapping(item).get("evidence_chain") for item in stars.values()),
            "confidence": 0.95,
        },
        {
            "id": "W04",
            "title": "Day Master carrying wealth gate",
            "statement": _text(strength_gate.get("message")),
            "evidence_chain": _text_list(strength_gate.get("evidence_chain")),
            "confidence": strength_gate.get("confidence"),
        },
        {
            "id": "W06",
            "title": "Wealth flow",
            "statement": "Tài được đọc trong chuỗi sinh hóa, không đứng độc lập.",
            "evidence_chain": _text_list(flow.get("evidence_chain")),
            "confidence": flow.get("confidence"),
        },
        {
            "id": "W08",
            "title": "Generate, retain, accumulate",
            "statement": "Tạo Tài, giữ Tài và tích Tài là ba kết luận độc lập.",
            "evidence_chain": _flatten([peer.get("evidence_chain"), storage.get("evidence_chain")]),
            "confidence": 0.84,
        },
    ]
    if _list(timing.get("items")):
        findings.append(
            {
                "id": "W10",
                "title": "Luck timing as modifier",
                "statement": "Đại vận/Lưu niên chỉ kích hoạt hoặc làm biến động nền Tài nguyên cục.",
                "evidence_chain": ["Natal truth is the base; timing is modifier"],
                "confidence": timing.get("confidence"),
            }
        )
    return findings


def _customer_paragraphs(
    sources: Sequence[Mapping[str, Any]],
    outcome: Mapping[str, Any],
    peer: Mapping[str, Any],
    storage: Mapping[str, Any],
    timing: Mapping[str, Any],
) -> list[str]:
    source_labels = [str(item.get("label")) for item in sources if item.get("label")]
    paragraphs = [
        "Tiền đến từ đâu?: " + (
            "Cấu trúc lá số chỉ ra nguồn tiền hợp logic đến từ " + "; ".join(source_labels) + ". Đây là kết luận từ vị trí Tài tinh, trụ chứa Tài và đường Tài đi qua Quan/Sát - Ấn, không dựa vào nghề hiện tại."
            if source_labels else "Chưa đủ bằng chứng Tài tinh rõ để chốt nguồn tiền riêng; cần đọc qua năng lực tạo giá trị và vận kích hoạt."
        ),
        "Kiếm tiền bằng cách nào?: Nền phù hợp là biến quan hệ thị trường thành niềm tin, rồi biến niềm tin thành dịch vụ, sản phẩm, chuyên môn hoặc dự án có đầu ra đo được. Tài xuất hiện chỉ mở chủ đề tiền bạc; có kiếm được hay không còn tùy cách tạo giá trị và kỷ luật thực thi.",
        "Điểm rò tiền: " + (
            "Kiếp Tài/Tỷ Kiên cho thấy cạnh tranh, cộng sự, chi phí vận hành, chia lợi ích hoặc tái đầu tư có thể làm dòng tiền bị mỏng đi. Vì vậy hợp tác, nhân sự và phần chia lợi nhuận cần ranh giới rõ."
            if peer.get("state") == "wealth_contested_by_peer" else "Chưa thấy áp lực Tỷ/Kiếp nổi bật; vẫn cần kiểm soát chi phí và quyết định mở rộng."
        ),
        "Khả năng giữ tiền: " + (
            "Khả năng tạo tiền có thể tốt hơn khả năng giữ tiền tự nhiên. Nên tách doanh thu, lợi nhuận, quỹ dự phòng và phần tái đầu tư; không lấy doanh thu lớn làm bằng chứng đã giữ được Tài."
            if outcome.get("wealth_retention") == "challenged" else "Có thể giữ tiền tốt hơn khi duy trì kỷ luật dòng tiền và không để cơ hội ngắn hạn phá kế hoạch dài hạn."
        ),
        "Con đường tích sản: " + (
            f"Mộc Tài mộ tại {storage.get('wealth_storage_branch')}; nguyên cục không sẵn Tài khố này, nên tích sản thiên về quá trình chuyển cơ hội thành hệ thống, dự án dài hạn và tài sản hóa về sau. Khi vận có {storage.get('wealth_storage_branch')}, vẫn phải xét khố có Tài, Tài nhập khố và khố có được mở hay không; không dùng quy tắc thô 'có khố là giàu'."
            if not storage.get("natal_storage_present") else "Nguyên cục có dấu hiệu Tài khố, nhưng vẫn cần xét khố có Tài, có nhập khố và có được mở hay không."
        ),
    ]
    timing_lines = [_text(item.get("reading")) for item in _list(timing.get("items")) if _text(item.get("reading"))]
    if timing_lines:
        paragraphs.append("Timing: " + " ".join(timing_lines[:8]))
    return paragraphs


def _wealth_type_for_stem(stem: str, wealth_stems: Mapping[str, str]) -> str:
    for key, value in wealth_stems.items():
        if stem == value:
            return key
    return ""


def _split_ganzhi(value: str) -> tuple[str, str]:
    parts = _text(value).replace("/", " ").split()
    return (parts[0], parts[1]) if len(parts) >= 2 else (_text(value)[:1], _text(value)[1:])


def _relation_summary(relations: Sequence[Mapping[str, Any]]) -> list[str]:
    return _unique_texts(_text(item.get("meaning")) for item in relations)


def _unique_relation_items(items: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, str, str]] = set()
    result: list[dict[str, Any]] = []
    for item in items:
        key = (_text(item.get("relation")), _text(item.get("branch")), _text(item.get("other_branch")), "-".join(_text_list(item.get("branches"))))
        if key in seen:
            continue
        seen.add(key)
        result.append(dict(item))
    return result


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _text(value: Any) -> str:
    return str(value or "").strip()


def _first_text(*values: Any) -> str:
    for value in values:
        text = _text(value)
        if text:
            return text
    return ""


def _text_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [_text(item) for item in value if _text(item)]
    if isinstance(value, tuple):
        return [_text(item) for item in value if _text(item)]
    text = _text(value)
    return [text] if text else []


def _flatten(groups: Any) -> list[str]:
    result: list[str] = []
    iterable = groups if not isinstance(groups, (str, bytes)) else [groups]
    try:
        iterator = iter(iterable)
    except TypeError:
        iterator = iter([iterable])
    for group in iterator:
        if isinstance(group, (list, tuple)):
            result.extend(_text_list(list(group)))
        else:
            text = _text(group)
            if text:
                result.append(text)
    return _unique_texts(result)


def _unique_texts(values: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = _text(value)
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result
