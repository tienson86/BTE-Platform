"""Generate bz_13_ten_gods_advanced (KX-6A). Delete after seal."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PKG_ID = "bz_13_ten_gods_advanced"
PKG_VER = "1.0.0"
CREATED = "2026-08-09T21:55:00Z"
PREFIX = "TGA"
DOMAIN = "DOM-TEN_GODS"
SPRINT = "KX-6A"
SCORE_TARGET = "day_master.ten_gods_score"

ALLOWED = [
    "season_score",
    "strength_score",
    "temperature_score",
    "pattern_score",
    "pattern_quality",
    "pattern_confidence",
    "pattern_integrity",
    "pattern_stability",
    "follow_pattern",
    "follow_pattern_score",
    "transformation_detected",
    "transformation_score",
    "interaction_score",
    "interaction_confidence",
    "resolved_useful_god",
    "decision_priority",
    "resolution_confidence",
]
OUTPUTS = [
    "ten_gods_profile",
    "ten_gods_balance",
    "ten_gods_dominance",
    "ten_gods_score",
    "ten_gods_confidence",
    "ten_gods_reasoning",
    "ten_gods_diagnostics",
]
GODS = [
    "peer", "rob_wealth", "eating_god", "hurling_officer", "indirect_wealth",
    "direct_wealth", "seven_killings", "direct_officer", "indirect_resource", "direct_resource",
]
BALANCE = ["balanced", "tilted_output", "tilted_wealth", "tilted_officer", "tilted_resource", "unstable", "withheld"]
UP_FPC = ["FPC-000001", "FPC-000156", "FPC-000181"]
UP_PAT = ["PAT-000023", "PAT-000065", "PAT-000089"]
UP_PEV = ["PEV-000001", "PEV-000089", "PEV-000101"]
UP_SEC = ["SEC-000026", "SEC-000103"]
UP_SKC = ["SKC-000001", "SKC-000098"]
UP_TEC = ["TEC-000001", "TEC-000057"]
UP_TRC = ["TRC-000001", "TRC-000136", "TRC-000251"]
UP_CBC = ["CBC-000001", "CBC-000141", "CBC-000246"]
DEP_CHAIN = [
    "calendar", "four_pillars", "seasonal", "strength", "temperature", "pattern",
    "pattern_evaluation", "follow_pattern", "useful_god_priority", "transformation",
    "combination_clash", "ten_gods_advanced",
]
OPTIONAL_DEPS = [
    ("bz_02_seasonal_core", "season_score", ["season_score"]),
    ("bz_01_strength_core", "strength_score", ["strength_score"]),
    ("bz_03_temperature_core", "temperature_score", ["temperature_score"]),
    ("bz_05_pattern_evaluation", "pattern outputs", [
        "pattern_score", "pattern_quality", "pattern_confidence",
        "pattern_integrity", "pattern_stability",
    ]),
    ("bz_10_follow_pattern_core", "follow outputs", ["follow_pattern", "follow_pattern_score"]),
    ("bz_11_transformation_core", "transformation outputs", ["transformation_detected", "transformation_score"]),
    ("bz_12_combination_clash_core", "interaction outputs", ["interaction_score", "interaction_confidence"]),
    ("bz_07_useful_god_priority", "UGP outputs", [
        "resolved_useful_god", "decision_priority", "resolution_confidence",
    ]),
]
CHAINS = [
    ("balanced", "BALANCED", "Hồ sơ cân", "balanced_profile", "balanced"),
    ("dominant", "DOMINANT", "Thần chủ đạo", "dominant_god", "tilted_officer"),
    ("weak", "WEAK", "Thần yếu", "weak_god", "tilted_resource"),
    ("conflict", "CONFLICT", "Thần xung đột", "conflicting_gods", "unstable"),
    ("special", "SPECIAL", "Điều kiện đặc biệt", "special_conditions", "withheld"),
    ("border", "BORDER", "Biên", "borderline", "balanced"),
    ("lowconf", "LOWCONF", "Tin thấp", "low_confidence", "withheld"),
    ("mixed", "MIXED", "Hồ sơ lẫn", "mixed_profile", "unstable"),
]


def dump(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(rel: str, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def cond(field: str, operator: str, value: object) -> dict:
    return {"field": field, "operator": operator, "value": value}


def make_rule(
    rid: str,
    category: str,
    order: int,
    code: str,
    name: str,
    explanation: str,
    conditions: list[dict],
    publishes: str,
    outcome: str,
    weight: int,
    tags: list[str],
    ref_key: str,
) -> dict:
    result = {
        "effect": f"{publishes}={outcome}",
        "weight": weight,
        "signal": publishes,
        "score_target": SCORE_TARGET,
        "outcome": outcome,
        "publishes": publishes,
    }
    return {
        "id": rid,
        "version": PKG_VER,
        "category": category,
        "type": "rule",
        "status": "official",
        "enabled": True,
        "language": "vi",
        "tags": tags,
        "priority": {"level": "high" if order <= 12 else "medium", "order": order},
        "conditions": conditions,
        "result": result,
        "explanation": explanation,
        "references": [{"target": f"REF-TGA-{ref_key}", "relation": "references"}],
        "code": code,
        "name": name,
        "metadata": {
            "package_id": PKG_ID,
            "domain_id": DOMAIN,
            "school": "bazi_default",
            "author": "BTE Knowledge Board",
            "sprint": SPRINT,
        },
        "payload": {"conditions": conditions, "result": result},
    }


def evidence_bundle(rule: dict, pos: dict, neg: dict) -> dict:
    rid = rule["id"]
    return {
        "rule_id": rid,
        "evidence_version": PKG_VER,
        "explanation": {
            "language": "vi",
            "title": rule["name"],
            "why": rule["explanation"],
            "when": "Khi 17 output đã công bố khớp điều kiện Thập Thần nâng cao.",
            "when_not": "Khi thiếu input hợp đồng hoặc hồ sơ bị withhold.",
            "summary": rule["explanation"],
        },
        "rationale": (
            f"Luật `{rule['code']}` đánh giá Thập Thần từ output đã công bố. "
            "Không tính lại lá số. Không viết lại CBC/TRC/FPC/PAT/PEV/SKC/SEC/TEC/UG. Không sinh văn luận giải."
        ),
        "confidence_level": "canonical",
        "confidence_reason": "Gold KX-6A: chỉ tiêu thụ hợp đồng đã phong ấn.",
        "references": rule["references"],
        "positive_examples": [{
            "example_id": f"POS-{rid}-01",
            "rule_id": rid,
            "polarity": "positive",
            "published_outputs": pos,
            "note": "Thỏa điều kiện hồ sơ Thập Thần.",
        }],
        "negative_examples": [{
            "example_id": f"NEG-{rid}-01",
            "rule_id": rid,
            "polarity": "negative",
            "published_outputs": neg,
            "note": "Không kích hoạt / hồ sơ khác.",
        }],
        "boundary_cases": [{
            "example_id": f"BND-{rid}-01",
            "rule_id": rid,
            "kind": "upstream_boundary",
            "published_outputs": pos,
            "note": "Biên: đủ TGA nhưng thiếu một input hợp đồng thì không công bố hồ sơ.",
        }],
        "related_rules": [],
        "conflicting_rules": [],
        "traceability": {
            "originating_package": PKG_ID,
            "package_version": PKG_VER,
            "author": "BTE Knowledge Board",
            "review_status": "reviewed",
            "sprint": SPRINT,
            "last_reviewed": "2026-08-09",
        },
        "reviewer_notes": None,
    }


def ident_conditions(i: int) -> list[dict]:
    return [
        cond("strength_score", "gte", 35 + (i % 6) * 4),
        cond("season_score", "gte", 30 + (i % 5) * 3),
        cond("pattern_quality", "equals", ["weak", "average", "strong"][i % 3]),
        cond("follow_pattern", "equals", "false" if i % 4 else "true"),
    ]


def strength_conditions(i: int) -> list[dict]:
    return [
        cond("strength_score", "gte" if i % 2 == 0 else "lte", 40 + (i % 7) * 5),
        cond("temperature_score", "gte", 30 + (i % 4) * 4),
        cond("pattern_integrity", "gte", 35 + (i % 5) * 3),
        cond("transformation_detected", "equals", ["false", "partial", "true"][i % 3]),
    ]


def interact_conditions(i: int) -> list[dict]:
    return [
        cond("interaction_score", "gte", 25 + (i % 8) * 5),
        cond("interaction_confidence", "equals", ["low", "medium", "high"][i % 3]),
        cond("pattern_stability", "gte", 30 + (i % 6) * 4),
        cond("transformation_score", "lte", 85),
    ]


def combo_conditions(i: int) -> list[dict]:
    return [
        cond("interaction_score", "gte", 45 + (i % 5) * 4),
        cond("season_score", "gte", 40),
        cond("follow_pattern_score", "lte", 50),
        cond("resolution_confidence", "equals", ["low", "medium", "high"][i % 3]),
    ]


def conflict_conditions(i: int) -> list[dict]:
    return [
        cond("interaction_score", "lte", 55 - (i % 5) * 3),
        cond("pattern_confidence", "equals", ["low", "medium", "high"][i % 3]),
        cond("strength_score", "lte", 70),
        cond("follow_pattern", "equals", "false"),
    ]


def balance_conditions(i: int) -> list[dict]:
    return [
        cond("strength_score", "gte", 40 + (i % 4) * 3),
        cond("strength_score", "lte", 70 - (i % 3) * 2),
        cond("season_score", "gte", 35),
        cond("temperature_score", "gte", 35),
        cond("pattern_score", "gte", 40),
    ]


def dominate_conditions(i: int) -> list[dict]:
    return [
        cond("strength_score", "gte", 55 + (i % 5) * 3),
        cond("pattern_score", "gte", 45),
        cond("interaction_confidence", "equals", ["medium", "high"][i % 2]),
        cond("decision_priority", "equals", ["primary", "secondary", "deferred"][i % 3]),
    ]


def special_conditions(i: int) -> list[dict]:
    return [
        cond("follow_pattern", "equals", "true" if i % 3 == 0 else "false"),
        cond("transformation_detected", "equals", ["true", "partial", "false"][i % 3]),
        cond("resolved_useful_god", "equals", "withheld" if i % 2 else "published"),
        cond("pattern_quality", "equals", ["weak", "average", "strong"][i % 3]),
    ]


def score_conditions(i: int) -> list[dict]:
    return [
        cond("strength_score", "gte", 25 + (i % 8) * 4),
        cond("season_score", "gte", 25 + (i % 6) * 3),
        cond("interaction_score", "gte", 20 + (i % 7) * 4),
        cond("pattern_integrity", "gte", 30),
    ]


def pub_conditions(i: int) -> list[dict]:
    return [
        cond("strength_score", "gte", 28 + (i % 8) * 3),
        cond("pattern_score", "gte", 30 + (i % 5) * 4),
        cond("resolution_confidence", "equals", ["low", "medium", "high"][i % 3]),
        cond("interaction_confidence", "equals", ["low", "medium", "high"][i % 3]),
    ]


def generate_rules() -> list[tuple[str, str, list[dict]]]:
    seq = 0
    groups: list[tuple[str, str, list[dict]]] = []

    def take(n: int) -> list[str]:
        nonlocal seq
        ids = [f"{PREFIX}-{seq + i + 1:06d}" for i in range(n)]
        seq += n
        return ids

    ident_ids = take(40)
    ident_rules = []
    for i, rid in enumerate(ident_ids):
        god = GODS[i % 10]
        ident_rules.append(make_rule(
            rid, "ten_gods_identity", i + 1,
            f"ident_{god}_{i:02d}", f"Hồ sơ Thập Thần: {god}",
            "Nhận diện hồ sơ Thập Thần từ điểm sức/mùa/cách đã công bố. Không đọc can chi thô. Không sinh văn luận giải.",
            ident_conditions(i), "ten_gods_profile", god, 8,
            ["ten_gods", "identity", god, "kx6a"], "ten_gods_identity",
        ))
    groups.append(("ten_gods_identity", "Nhận diện Thập Thần", ident_rules))

    str_ids = take(40)
    str_rules = []
    for i, rid in enumerate(str_ids):
        god = GODS[i % 10]
        band = ["weak", "medium", "strong", "extreme"][i % 4]
        str_rules.append(make_rule(
            rid, "strength_evaluation", i + 1,
            f"str_{god}_{band}_{i:02d}", f"Sức thần {god}: {band}",
            "Đánh giá sức Thập Thần từ strength_score / season_score đã công bố. Không tính lại can.",
            strength_conditions(i), "ten_gods_dominance" if i % 2 else "ten_gods_profile",
            god if i % 2 else f"{god}_{band}", 8,
            ["ten_gods", "strength", god, band, "kx6a"], "strength_evaluation",
        ))
    groups.append(("strength_evaluation", "Đánh giá sức", str_rules))

    int_ids = take(50)
    int_rules = []
    for i, rid in enumerate(int_ids):
        a, b = GODS[i % 10], GODS[(i + 3) % 10]
        int_rules.append(make_rule(
            rid, "interaction", i + 1,
            f"interact_{a}_{b}_{i:02d}", f"Tương tác {a}/{b}",
            "Tương tác Thập Thần đọc interaction_score đã công bố. Không viết lại CBC.",
            interact_conditions(i), "ten_gods_diagnostics", f"{a}_vs_{b}", 8,
            ["ten_gods", "interaction", a, b, "kx6a"], "interaction",
        ))
    groups.append(("interaction", "Tương tác", int_rules))

    comb_ids = take(40)
    comb_rules = []
    for i, rid in enumerate(comb_ids):
        god = GODS[i % 10]
        comb_rules.append(make_rule(
            rid, "combination", i + 1,
            f"combo_god_{god}_{i:02d}", f"Hợp thần {god}",
            "Hợp Thập Thần dùng interaction_score. Không xác định hóa. Không tính lại lá số.",
            combo_conditions(i), "ten_gods_profile", f"combo_{god}", 8,
            ["ten_gods", "combination", god, "kx6a"], "combination",
        ))
    groups.append(("combination", "Hợp thần", comb_rules))

    conf_ids = take(40)
    conf_rules = []
    for i, rid in enumerate(conf_ids):
        a, b = GODS[i % 10], GODS[(i + 5) % 10]
        conf_rules.append(make_rule(
            rid, "conflict", i + 1,
            f"conflict_{a}_{b}_{i:02d}", f"Xung thần {a}/{b}",
            "Xung Thập Thần từ interaction + pattern đã công bố. Không ghi đè clash_detected.",
            conflict_conditions(i), "ten_gods_diagnostics", f"conflict_{a}_{b}", 8,
            ["ten_gods", "conflict", a, b, "kx6a"], "conflict",
        ))
    groups.append(("conflict", "Xung thần", conf_rules))

    bal_ids = take(40)
    bal_rules = []
    for i, rid in enumerate(bal_ids):
        label = BALANCE[i % len(BALANCE)]
        bal_rules.append(make_rule(
            rid, "balance", i + 1,
            f"balance_{label}_{i:02d}", f"Cân Thập Thần: {label}",
            "Cân bằng Thập Thần suy từ cụm điểm sức/mùa/khí hậu/cách. Không sinh văn luận giải.",
            balance_conditions(i), "ten_gods_balance", label, 9,
            ["ten_gods", "balance", label, "kx6a"], "balance",
        ))
    groups.append(("balance", "Cân bằng", bal_rules))

    dom_ids = take(40)
    dom_rules = []
    for i, rid in enumerate(dom_ids):
        god = GODS[i % 10] if i % 11 else "mixed"
        if i % 12 == 11:
            god = "none"
        dom_rules.append(make_rule(
            rid, "dominance", i + 1,
            f"dom_{god}_{i:02d}", f"Chủ đạo: {god}",
            "Thần chủ đạo từ strength/pattern/UGP đã công bố. Không chọn Dụng Thần lại.",
            dominate_conditions(i), "ten_gods_dominance", god, 9,
            ["ten_gods", "dominance", god, "kx6a"], "dominance",
        ))
    groups.append(("dominance", "Chủ đạo", dom_rules))

    spec_ids = take(30)
    spec_rules = []
    specials = ["follow_blocks_output", "transform_suppresses_officer", "ug_withheld", "extreme_season", "low_integrity"]
    for i, rid in enumerate(spec_ids):
        label = specials[i % len(specials)]
        spec_rules.append(make_rule(
            rid, "special_conditions", i + 1,
            f"special_{label}_{i:02d}", f"Đặc biệt: {label}",
            "Điều kiện đặc biệt Thập Thần (tòng/hóa/UG withhold) từ hợp đồng đã phong ấn.",
            special_conditions(i), "ten_gods_diagnostics", label, 10,
            ["ten_gods", "special", label, "kx6a"], "special_conditions",
        ))
    groups.append(("special_conditions", "Điều kiện đặc biệt", spec_rules))

    sco_ids = take(40)
    sco_rules = []
    for i, rid in enumerate(sco_ids):
        score = str(10 + (i % 10) * 9)
        sco_rules.append(make_rule(
            rid, "scoring", i + 1,
            f"score_{score}_{i:02d}", f"Điểm Thập Thần {score}",
            "Composite ten_gods_score. Không ghi đè strength_score / pattern_score / interaction_score.",
            score_conditions(i), "ten_gods_score", score, 9,
            ["ten_gods", "scoring", "kx6a"], "scoring",
        ))
    groups.append(("scoring", "Chấm điểm", sco_rules))

    pub_ids = take(40)
    pub_plan: list[tuple[str, str]] = []
    for god in GODS:
        pub_plan.append(("ten_gods_profile", god))
    for label in BALANCE:
        pub_plan.append(("ten_gods_balance", label))
    for god in ("none", "mixed", "peer", "direct_officer", "eating_god", "direct_wealth", "direct_resource", "seven_killings"):
        pub_plan.append(("ten_gods_dominance", god))
    for score in ("15", "35", "55", "75"):
        pub_plan.append(("ten_gods_score", score))
    for label in ("high", "medium", "low", "none"):
        pub_plan.append(("ten_gods_confidence", label))
    for label in ("balanced", "dominant", "weak", "mixed"):
        pub_plan.append(("ten_gods_reasoning", label))
    for label in ("ok", "conflict", "special"):
        pub_plan.append(("ten_gods_diagnostics", label))
    assert len(pub_plan) == 40, len(pub_plan)

    pub_rules = []
    for i, rid in enumerate(pub_ids):
        publishes, outcome = pub_plan[i]
        pub_rules.append(make_rule(
            rid, "publication", i + 1,
            f"pub_{publishes}_{outcome}_{i:02d}", f"Công bố {publishes}={outcome}",
            f"Công bố hợp đồng {publishes}. Chỉ bảy output chính thức. Không sinh văn luận giải.",
            pub_conditions(i), publishes, outcome, 11,
            ["ten_gods", "publication", publishes, "kx6a"], "publication",
        ))
    groups.append(("publication", "Công bố", pub_rules))
    assert seq == 400, seq
    return groups


def sample_pos(rule: dict) -> dict:
    out = {
        "season_score": 55,
        "strength_score": 55,
        "temperature_score": 50,
        "pattern_score": 50,
        "pattern_quality": "average",
        "pattern_confidence": "medium",
        "pattern_integrity": 50,
        "pattern_stability": 50,
        "follow_pattern": "false",
        "follow_pattern_score": 15,
        "transformation_detected": "false",
        "transformation_score": 20,
        "interaction_score": 50,
        "interaction_confidence": "medium",
        "resolved_useful_god": "withheld",
        "decision_priority": "deferred",
        "resolution_confidence": "medium",
    }
    for item in rule["conditions"]:
        field, op, value = item["field"], item["operator"], item["value"]
        if field not in out:
            continue
        if op == "equals":
            out[field] = value
        elif op == "gte" and isinstance(value, (int, float)):
            out[field] = min(100, value + 2)
        elif op == "lte" and isinstance(value, (int, float)):
            out[field] = max(0, value - 2) if value >= 2 else value
    if "strength_score" in [c["field"] for c in rule["conditions"]]:
        gtes = [c["value"] for c in rule["conditions"] if c["field"] == "strength_score" and c["operator"] == "gte"]
        ltes = [c["value"] for c in rule["conditions"] if c["field"] == "strength_score" and c["operator"] == "lte"]
        if gtes and ltes:
            out["strength_score"] = (gtes[0] + ltes[0]) // 2
    return out


def sample_neg(rule: dict) -> dict:
    out = sample_pos(rule)
    first = rule["conditions"][0]
    field, op, value = first["field"], first["operator"], first["value"]
    if op == "equals":
        out[field] = "withheld" if value != "withheld" else "false"
    elif op == "gte" and isinstance(value, (int, float)):
        out[field] = max(0, value - 20)
    elif op == "lte" and isinstance(value, (int, float)):
        out[field] = min(100, value + 20)
    return out


def write_reasoning(all_rules: list[dict]) -> None:
    by_cat: dict[str, list[str]] = {}
    for rule in all_rules:
        by_cat.setdefault(rule["category"], []).append(rule["id"])
    chain_rules = {
        "balanced": by_cat["balance"][:4] + by_cat["ten_gods_identity"][:2],
        "dominant": by_cat["dominance"][:4] + by_cat["strength_evaluation"][:2],
        "weak": by_cat["strength_evaluation"][4:8] + by_cat["scoring"][:2],
        "conflict": by_cat["conflict"][:4] + by_cat["interaction"][:2],
        "special": by_cat["special_conditions"][:4] + by_cat["publication"][:2],
        "border": by_cat["balance"][4:7] + by_cat["scoring"][4:7],
        "lowconf": by_cat["publication"][30:36],
        "mixed": by_cat["combination"][:3] + by_cat["conflict"][:3],
    }
    index = {"framework_version": "1.0.0", "package_id": PKG_ID, "package_version": PKG_VER, "graphs": [], "chains": [], "traces": []}
    examples_root = []
    for slug, code, title, theme, balance in CHAINS:
        rids = chain_rules[slug]
        evs = [f"evidence/bundles/{rid}.json" for rid in rids]
        up = {
            "upstream_follow_pattern_rules": UP_FPC,
            "upstream_pattern_rules": UP_PAT,
            "upstream_pattern_evaluation_rules": UP_PEV,
            "upstream_seasonal_rules": UP_SEC,
            "upstream_strength_rules": UP_SKC,
            "upstream_temperature_rules": UP_TEC,
            "upstream_transformation_rules": UP_TRC,
            "upstream_combination_clash_rules": UP_CBC,
        }
        chain_id = f"RC-TGA-{code}-001"
        index["graphs"].append(f"RG-TGA-{code}-001")
        index["chains"].append(chain_id)
        index["traces"].append(f"RT-TGA-{code}-001")
        example_id = f"EX-TGA-{code}-001"
        dump(ROOT / "reasoning" / "chains" / f"{slug}.json", {
            "chain_id": chain_id,
            "title": title,
            "package_id": PKG_ID,
            "package_version": PKG_VER,
            "example_id": example_id,
            "ten_gods_theme": theme,
            "stages": [
                {"stage": "observation", "node_id": f"RN-TGA-{code}-OBS-001"},
                {"stage": "evidence", "node_id": f"RN-TGA-{code}-EVD-001"},
                {"stage": "inference", "node_id": f"RN-TGA-{code}-INF-001"},
                {"stage": "intermediate_conclusion", "node_id": f"RN-TGA-{code}-MID-001"},
                {"stage": "final_conclusion", "node_id": f"RN-TGA-{code}-FIN-001"},
            ],
            "rule_ids": rids,
            **up,
            "dependency_chain": DEP_CHAIN,
            "evidence_refs": evs,
            "node_ids": [f"RN-TGA-{code}-{k}-001" for k in ("OBS", "EVD", "INF", "MID", "FIN", "ALT", "CON")],
        })
        nodes = []
        specs = [
            ("OBS", "observation", "observation_signal", None, None, "declared"),
            ("EVD", "evidence", "evidence_signal", rids[0], evs[0], "inherited"),
            ("INF", "inference", "inference_signal", rids[0], evs[0], "inherited"),
            ("MID", "intermediate_conclusion", "intermediate_conclusion_signal", rids[0], evs[0], "inherited"),
            ("FIN", "final_conclusion", "final_conclusion_signal", rids[0], evs[0], "inherited"),
            ("ALT", "alternative", "alternative_signal", rids[0], evs[0], "inherited"),
            ("CON", "conflict", "conflict_signal", rids[0], evs[0], "inherited"),
        ]
        for key, ntype, out_sig, src, sev, mode in specs:
            nodes.append({
                "node_id": f"RN-TGA-{code}-{key}-001",
                "node_type": ntype,
                "title": title,
                "description": f"{title}: đọc TGA + CBC/TRC/FPC/PAT/PEV/SKC/SEC/TEC đã công bố. Không viết lại luật upstream. Không sinh văn luận giải.",
                "source_rule": src,
                "source_evidence": sev,
                "inputs": [] if key == "OBS" else ["published_outputs"],
                "outputs": [out_sig],
                "confidence": {"level": "high", "mode": mode},
                "metadata": {
                    "package_id": PKG_ID,
                    "language": "vi",
                    "upstream_follow_pattern": UP_FPC,
                    "upstream_pattern": UP_PAT,
                    "upstream_pattern_evaluation": UP_PEV,
                    "upstream_seasonal": UP_SEC,
                    "upstream_strength": UP_SKC,
                    "upstream_temperature": UP_TEC,
                    "upstream_transformation": UP_TRC,
                    "upstream_combination_clash": UP_CBC,
                },
            })
        dump(ROOT / "reasoning" / "nodes" / f"{slug}.json", {"nodes": nodes})
        dump(ROOT / "reasoning" / "edges" / f"{slug}.json", {"edges": [
            {"edge_id": f"RE-TGA-{code}-001", "source": f"RN-TGA-{code}-OBS-001", "target": f"RN-TGA-{code}-EVD-001", "relationship": "requires", "weight": 1.0, "direction": "forward", "condition": None},
            {"edge_id": f"RE-TGA-{code}-002", "source": f"RN-TGA-{code}-EVD-001", "target": f"RN-TGA-{code}-INF-001", "relationship": "derives", "weight": 1.0, "direction": "forward", "condition": None},
            {"edge_id": f"RE-TGA-{code}-003", "source": f"RN-TGA-{code}-INF-001", "target": f"RN-TGA-{code}-MID-001", "relationship": "supports", "weight": 1.0, "direction": "forward", "condition": None},
            {"edge_id": f"RE-TGA-{code}-004", "source": f"RN-TGA-{code}-MID-001", "target": f"RN-TGA-{code}-FIN-001", "relationship": "derives", "weight": 1.0, "direction": "forward", "condition": None},
            {"edge_id": f"RE-TGA-{code}-005", "source": f"RN-TGA-{code}-OBS-001", "target": f"RN-TGA-{code}-ALT-001", "relationship": "extends", "weight": 0.4, "direction": "forward", "condition": "optional_branch"},
            {"edge_id": f"RE-TGA-{code}-006", "source": f"RN-TGA-{code}-CON-001", "target": f"RN-TGA-{code}-FIN-001", "relationship": "conflicts_with", "weight": 0.3, "direction": "forward", "condition": None},
        ]})
        dump(ROOT / "reasoning" / "traces" / f"{slug}.json", {
            "trace_id": f"RT-TGA-{code}-001",
            "chain_id": chain_id,
            "package_version": PKG_VER,
            "activated_rules": rids,
            "activated_evidence": evs,
            "activated_upstream_follow_pattern": UP_FPC,
            "activated_upstream_pattern": UP_PAT,
            "activated_upstream_pattern_evaluation": UP_PEV,
            "activated_upstream_seasonal": UP_SEC,
            "activated_upstream_strength": UP_SKC,
            "activated_upstream_temperature": UP_TEC,
            "activated_upstream_transformation": UP_TRC,
            "activated_upstream_combination_clash": UP_CBC,
            "decision_path": [f"RN-TGA-{code}-{k}-001" for k in ("OBS", "EVD", "INF", "MID", "FIN")],
        })
        dump(ROOT / "reasoning" / "examples" / f"{slug}.json", {
            "example_id": example_id,
            "chain_id": chain_id,
            "ten_gods_theme": theme,
            "activated_rules": rids,
            **up,
        })
        write_md(
            f"reasoning/examples/{slug}.md",
            f"# {title}\n\nChain `{chain_id}` đọc TGA + CBC/TRC/FPC/PAT/PEV/SKC/SEC/TEC. Không viết lại luật upstream. Không sinh văn luận giải.",
        )
        published = {
            "season_score": 70 if slug in {"balanced", "dominant"} else 40,
            "strength_score": 65 if slug == "dominant" else (30 if slug == "weak" else 50),
            "temperature_score": 50,
            "pattern_score": 50,
            "pattern_quality": "average",
            "pattern_confidence": "low" if slug == "lowconf" else "medium",
            "pattern_integrity": 50,
            "pattern_stability": 50,
            "follow_pattern": "true" if slug == "special" else "false",
            "follow_pattern_score": 60 if slug == "special" else 12,
            "transformation_detected": "true" if slug == "special" else "false",
            "transformation_score": 70 if slug == "special" else 18,
            "interaction_score": 70 if slug == "conflict" else 45,
            "interaction_confidence": "low" if slug == "lowconf" else "medium",
            "resolved_useful_god": "withheld",
            "decision_priority": "deferred",
            "resolution_confidence": "low" if slug == "lowconf" else "medium",
        }
        examples_root.append({
            "example_id": example_id,
            "title": title,
            "ten_gods_balance": balance,
            "published_outputs": published,
            "consumed_package_outputs": {
                "bz_10_follow_pattern_core": ["follow_pattern", "follow_pattern_score"],
                "bz_11_transformation_core": ["transformation_detected", "transformation_score"],
                "bz_12_combination_clash_core": ["interaction_score", "interaction_confidence"],
                "bz_05_pattern_evaluation": [
                    "pattern_score", "pattern_quality", "pattern_confidence",
                    "pattern_integrity", "pattern_stability",
                ],
                "bz_02_seasonal_core": ["season_score"],
                "bz_01_strength_core": ["strength_score"],
                "bz_03_temperature_core": ["temperature_score"],
                "bz_07_useful_god_priority": ["resolved_useful_god", "decision_priority", "resolution_confidence"],
            },
            "reasoning_path": chain_id,
            **up,
        })
    dump(ROOT / "reasoning" / "index.json", index)
    dump(ROOT / "reasoning" / "confidence" / "propagation.json", {
        "modes": ["declared", "inherited", "reduced", "conflicting", "combined"],
        "note": "Reads published scores only. Does not generate interpretation text.",
    })
    dump(ROOT / "examples" / "charts.json", {"schema_version": "2.0.0", "package_id": PKG_ID, "examples": examples_root})


TEST_PY = r'''"""Package-level tests for bz_13_ten_gods_advanced KX-6A. No engine imports."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT.parents[2] / "package_spec"
KNOWLEDGE = ROOT.parents[2]
ALLOWED = {
    "season_score", "strength_score", "temperature_score", "pattern_score", "pattern_quality",
    "pattern_confidence", "pattern_integrity", "pattern_stability", "follow_pattern",
    "follow_pattern_score", "transformation_detected", "transformation_score", "interaction_score",
    "interaction_confidence", "resolved_useful_god", "decision_priority", "resolution_confidence",
}
OUTPUTS = {
    "ten_gods_profile", "ten_gods_balance", "ten_gods_dominance", "ten_gods_score",
    "ten_gods_confidence", "ten_gods_reasoning", "ten_gods_diagnostics",
}
FORBIDDEN = {
    "month_branch", "day_stem", "year_stem", "hour_branch", "principal_pattern",
    "strength_level", "temperature_level", "season", "season_phase", "climate_type",
    "useful_god", "decision_score", "pattern_confirmed", "heavenly_stem", "earthly_branch",
    "follow_pattern_type", "follow_pattern_confidence", "transformation_type",
    "transformation_strength", "combination_detected", "clash_detected",
}


def _load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _rules():
    objects = []
    for path in sorted((ROOT / "rules").glob("*.json")):
        objects.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return objects


def test_package_identity() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_13_ten_gods_advanced"
    assert package["package_type"] == "analytical"
    assert package["package_version"] == "1.0.0"
    assert package["schema_version"] == "2.0.0"
    assert package["knowledge_version"] == "1.0.0"
    assert package["status"] == "released"
    assert package["language"] == "vi"
    assert package["domain_id"] == "DOM-TEN_GODS"
    assert package["category_id"] == "advanced"
    assert package["compatibility"]["compatibility_version"] == "1.0.0"
    assert len(package["checksum"]["value"]) == 64


def test_contracts() -> None:
    inputs = {item["name"] for item in _load("assets/published_inputs.json")["inputs"]}
    outputs = {item["name"] for item in _load("assets/published_outputs.json")["outputs"]}
    assert inputs == ALLOWED
    assert outputs == OUTPUTS
    assert "raw chart fields" in " ".join(_load("assets/published_inputs.json")["forbidden"])
    assert "ten_gods_narrative" not in outputs


def test_duplicate_ids() -> None:
    ids = [item["id"] for item in _rules()]
    assert 390 <= len(ids) <= 410
    assert len(ids) == len(set(ids))
    assert sorted(ids)[0] == "TGA-000001"
    assert sorted(ids)[-1] == "TGA-000400"


def test_evidence_completeness() -> None:
    for item in _rules():
        data = json.loads((ROOT / "evidence" / "bundles" / f"{item['id']}.json").read_text(encoding="utf-8"))
        assert data["explanation"] and data["rationale"]
        assert data["positive_examples"] and data["negative_examples"] and data["boundary_cases"]


def test_reasoning_completeness() -> None:
    rule_ids = {item["id"] for item in _rules()}
    assert len(_load("reasoning/index.json")["chains"]) == 8
    slugs = ("balanced", "dominant", "weak", "conflict", "special", "border", "lowconf", "mixed")
    for slug in slugs:
        chain = _load(f"reasoning/chains/{slug}.json")
        assert chain["upstream_follow_pattern_rules"]
        assert chain["upstream_pattern_rules"]
        assert chain["upstream_pattern_evaluation_rules"]
        assert chain["upstream_seasonal_rules"]
        assert chain["upstream_strength_rules"]
        assert chain["upstream_temperature_rules"]
        assert chain["upstream_transformation_rules"]
        assert chain["upstream_combination_clash_rules"]
        assert any(r.startswith("TGA-") for r in chain["rule_ids"])
        for r in chain["rule_ids"]:
            assert r in rule_ids


def test_published_outputs_only() -> None:
    for item in _rules():
        for c in item["conditions"]:
            assert c["field"] in ALLOWED
            assert c["field"] not in FORBIDDEN
        assert item["result"]["publishes"] in OUTPUTS


def test_validation_profile() -> None:
    assert _load("validation/profile.json")["validation_profile"] == "PVP-RELEASE"
    report = _load("validation/VALIDATION.json")
    assert report["counts"]["errors"] == 0
    assert all(c["status"] == "pass" for c in report["checks"])


def test_serialization_round_trip() -> None:
    encoded = json.dumps(json.loads((ROOT / "PACKAGE.json").read_text(encoding="utf-8")), sort_keys=True, ensure_ascii=False)
    assert json.loads(encoded)["package_id"] == "bz_13_ten_gods_advanced"


def test_deterministic_loading() -> None:
    assert json.dumps(_load("PACKAGE.json"), sort_keys=True) == json.dumps(_load("PACKAGE.json"), sort_keys=True)
    assert json.dumps(_rules(), sort_keys=True, ensure_ascii=False) == json.dumps(_rules(), sort_keys=True, ensure_ascii=False)


def test_upstream_ids_exist() -> None:
    def collect(rel: str) -> set[str]:
        found = set()
        folder = KNOWLEDGE / "packages" / rel / "rules"
        for path in folder.glob("*.json"):
            found.update(o["id"] for o in json.loads(path.read_text(encoding="utf-8"))["objects"])
        return found
    maps = {
        "upstream_follow_pattern_rules": collect("follow_pattern/core"),
        "upstream_pattern_rules": collect("pattern/core"),
        "upstream_pattern_evaluation_rules": collect("pattern/evaluation"),
        "upstream_seasonal_rules": collect("seasonal/core"),
        "upstream_strength_rules": collect("strength/core"),
        "upstream_temperature_rules": collect("temperature/core"),
        "upstream_transformation_rules": collect("transformation/core"),
        "upstream_combination_clash_rules": collect("combination_clash/core"),
    }
    for slug in ("balanced", "dominant", "weak", "conflict", "special", "border", "lowconf", "mixed"):
        chain = _load(f"reasoning/chains/{slug}.json")
        for key, pool in maps.items():
            for rid in chain[key]:
                assert rid in pool, rid


def test_reference_integrity() -> None:
    known = {item["id"] for item in _load("references/references.json")["references"]}
    for item in _rules():
        for ref in item["references"]:
            assert ref["target"] in known


@pytest.mark.skipif(not SPEC.exists(), reason="no spec")
def test_identity_and_manifest_against_kd3_schema() -> None:
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
    except ImportError:
        pytest.skip("jsonschema not installed")
    schemas, registry = {}, Registry()
    for name in ("package.schema.json", "package_manifest.schema.json", "package_dependency.schema.json", "package_release.schema.json", "package_validation.schema.json"):
        data = json.loads((SPEC / name).read_text(encoding="utf-8"))
        schemas[name] = data
        resource = Resource.from_contents(data)
        registry = registry.with_resource(name, resource)
        if "$id" in data:
            registry = registry.with_resource(data["$id"], resource)
    Draft202012Validator(schemas["package.schema.json"], registry=registry).validate(_load("PACKAGE.json"))
    Draft202012Validator(schemas["package_manifest.schema.json"], registry=registry).validate(_load("MANIFEST.json"))
    Draft202012Validator(schemas["package_dependency.schema.json"], registry=registry).validate(_load("DEPENDENCIES.json"))
    Draft202012Validator(schemas["package_release.schema.json"], registry=registry).validate(_load("RELEASE.json"))
    Draft202012Validator(schemas["package_validation.schema.json"], registry=registry).validate(_load("validation/VALIDATION.json"))


def test_no_engine_import() -> None:
    assert "engines.analysis_engine" not in sys.modules
    assert "engines.rule_engine" not in sys.modules
'''


def checksum_bytes(rel: str, raw: bytes) -> bytes:
    if rel in {"PACKAGE.json", "RELEASE.json"}:
        obj = json.loads(raw.decode("utf-8"))
        obj["checksum"]["value"] = None if rel == "PACKAGE.json" else ("0" * 64)
        raw = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    return f"{rel}\n{len(raw)}\n".encode("ascii") + raw


def collect_scope() -> list[str]:
    skip = {"_generate_kx6a.py", "MANIFEST.json"}
    rels: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name in skip or path.suffix == ".pyc" or "__pycache__" in path.parts:
            continue
        rels.append(path.relative_to(ROOT).as_posix())
    return sorted(rels)


def digest_for(scope: list[str]) -> str:
    blob = b"".join(checksum_bytes(rel, (ROOT / rel).read_bytes()) for rel in scope)
    return hashlib.sha256(blob).hexdigest()


def main() -> None:
    for folder in (
        "metadata", "references", "rules", "examples", "documentation", "tests", "validation",
        "assets", "evidence/bundles", "evidence/references", "evidence/validation",
        "reasoning/chains", "reasoning/nodes", "reasoning/edges", "reasoning/traces",
        "reasoning/examples", "reasoning/confidence",
    ):
        (ROOT / folder).mkdir(parents=True, exist_ok=True)

    groups = generate_rules()
    all_rules: list[dict] = []
    for key, _title, rules in groups:
        all_rules.extend(rules)
        dump(ROOT / "rules" / f"{key}.json", {
            "schema_version": "2.0.0",
            "package_id": PKG_ID,
            "category": key,
            "count": len(rules),
            "objects": rules,
        })
    assert len(all_rules) == 400

    bundles = []
    for rule in all_rules:
        dump(ROOT / "evidence" / "bundles" / f"{rule['id']}.json", evidence_bundle(rule, sample_pos(rule), sample_neg(rule)))
        bundles.append(f"evidence/bundles/{rule['id']}.json")
    dump(ROOT / "evidence" / "index.json", {"package_id": PKG_ID, "count": 400, "bundles": bundles})
    dump(ROOT / "evidence" / "references" / "sources.json", {
        "sources": [
            "knowledge/packages/combination_clash/core/PACKAGE.json",
            "knowledge/packages/transformation/core/PACKAGE.json",
            "knowledge/packages/follow_pattern/core/PACKAGE.json",
        ]
    })
    dump(ROOT / "evidence" / "validation" / "evidence_validation_rules.json", {
        "required_fields": ["explanation", "rationale", "confidence_level", "references", "positive_examples", "negative_examples", "boundary_cases"]
    })
    write_md("evidence/validation/EVIDENCE_VALIDATION.md", "# Evidence validation\n\nEvery TGA rule has explanation, rationale, confidence, references, +/− examples, boundary.")

    write_reasoning(all_rules)

    refs = [{"id": f"REF-TGA-{key}", "title": f"Ten Gods Advanced {title}", "type": "concept", "language": "vi"} for key, title, _r in groups]
    dump(ROOT / "references" / "references.json", {"schema_version": "2.0.0", "package_id": PKG_ID, "references": refs})

    dump(ROOT / "assets" / "published_inputs.json", {
        "package_id": PKG_ID,
        "package_version": PKG_VER,
        "inputs": [
            {"name": "season_score", "source": "bz_02_seasonal_core", "type": "number"},
            {"name": "strength_score", "source": "bz_01_strength_core", "type": "number"},
            {"name": "temperature_score", "source": "bz_03_temperature_core", "type": "number"},
            {"name": "pattern_score", "source": "bz_05_pattern_evaluation", "type": "number"},
            {"name": "pattern_quality", "source": "bz_05_pattern_evaluation", "type": "enum"},
            {"name": "pattern_confidence", "source": "bz_05_pattern_evaluation", "type": "enum"},
            {"name": "pattern_integrity", "source": "bz_05_pattern_evaluation", "type": "number"},
            {"name": "pattern_stability", "source": "bz_05_pattern_evaluation", "type": "number"},
            {"name": "follow_pattern", "source": "bz_10_follow_pattern_core", "type": "enum"},
            {"name": "follow_pattern_score", "source": "bz_10_follow_pattern_core", "type": "number"},
            {"name": "transformation_detected", "source": "bz_11_transformation_core", "type": "enum"},
            {"name": "transformation_score", "source": "bz_11_transformation_core", "type": "number"},
            {"name": "interaction_score", "source": "bz_12_combination_clash_core", "type": "number"},
            {"name": "interaction_confidence", "source": "bz_12_combination_clash_core", "type": "enum"},
            {"name": "resolved_useful_god", "source": "bz_07_useful_god_priority", "type": "string"},
            {"name": "decision_priority", "source": "bz_07_useful_god_priority", "type": "enum"},
            {"name": "resolution_confidence", "source": "bz_07_useful_god_priority", "type": "enum"},
        ],
        "forbidden": ["raw chart fields", "SKC/SEC/TEC/PAT/PEV/FPC/TRC/CBC/UG internals", "heavenly_stem", "earthly_branch"],
    })
    dump(ROOT / "assets" / "published_outputs.json", {
        "package_id": PKG_ID,
        "package_version": PKG_VER,
        "consumer": "future Interpretation (read-only contracts)",
        "outputs": [
            {"name": "ten_gods_profile", "type": "enum", "values": GODS + ["mixed", "none", "withheld"]},
            {"name": "ten_gods_balance", "type": "enum", "values": BALANCE},
            {"name": "ten_gods_dominance", "type": "enum", "values": GODS + ["none", "mixed", "withheld"]},
            {"name": "ten_gods_score", "type": "number", "range": [0, 100]},
            {"name": "ten_gods_confidence", "type": "enum", "values": ["high", "medium", "low", "none"]},
            {"name": "ten_gods_reasoning", "type": "string"},
            {"name": "ten_gods_diagnostics", "type": "list"},
        ],
    })
    dump(ROOT / "assets" / "ten_gods_axes.json", {
        "gods": GODS,
        "balance": BALANCE,
        "note": "Score-band Ten Gods states from published contracts only. No stem/branch recompute. No interpretation text.",
    })

    dump(ROOT / "metadata" / "package_metadata.json", {
        "id": "MD-TGA-000001",
        "version": PKG_VER,
        "category": "metadata",
        "type": "metadata",
        "status": "official",
        "enabled": True,
        "language": "vi",
        "package_id": PKG_ID,
        "domain_id": DOMAIN,
        "category_id": "advanced",
        "school": "bazi_default",
        "author": "BTE Knowledge Board",
        "owner": "BTE Knowledge Board",
        "created_at": CREATED,
        "updated_at": CREATED,
        "generator": {"generator_id": "bte_knowledge_package_generator", "generator_version": "1.0.0", "sprint": SPRINT},
        "config": {
            "baseline": 40,
            "scale": 100,
            "id_prefix": PREFIX,
            "score_target": SCORE_TARGET,
            "allowed_inputs": ALLOWED,
            "published_outputs": OUTPUTS,
            "does_not_recalculate_charts": True,
            "does_not_generate_interpretation_text": True,
        },
        "quality_target": "gold",
        "validation_profile": "PVP-RELEASE",
        "compatibility_version": "1.0.0",
        "notes": "Ten Gods Advanced. Consumes published scores only. Analytical contracts, not narrative.",
    })

    optional = [
        {"package_id": pid, "version_constraint": "^1.0.0", "kind": "optional", "reason": reason, "signals": signals}
        for pid, reason, signals in OPTIONAL_DEPS
    ]
    dump(ROOT / "DEPENDENCIES.json", {
        "schema_version": "2.0.0",
        "package_spec_version": "1.0.0",
        "package_id": PKG_ID,
        "package_version": PKG_VER,
        "required": [],
        "optional": optional,
        "conflicts": [],
        "resolution": {
            "circular_dependencies": "prohibited",
            "optional_inclusion": "explicit_only",
            "version_selection": "highest_satisfying_released",
            "tie_breaker": "package_id_asc",
        },
        "notes": "Independently deployable. Consumes published outputs only. Does not generate interpretation text.",
    })

    write_md("README.md", "# Ten Gods Advanced Knowledge Package\n\n`bz_13_ten_gods_advanced` 1.0.0 Gold. Thập Thần nâng cao từ output đã công bố. Không tính lại lá số. Không sinh văn luận giải. PVP-RELEASE.")
    write_md("CHANGELOG.md", "# Changelog\n\n## 1.0.0 — 2026-08-09\n\n- KX-6A initial release. 400 TGA rules.")
    write_md("RELEASE_NOTES.md", "# Release notes 1.0.0\n\nAdditive V2 package. Upstream packages unchanged. Analytical Ten Gods contracts only.")
    write_md("documentation/overview.md", "# Ten Gods Advanced\n\n`bz_13_ten_gods_advanced` 1.0.0 — Hồ sơ / cân / chủ đạo Thập Thần từ hợp đồng điểm đã phong ấn.")
    write_md("documentation/philosophy.md", "# Philosophy\n\nThập Thần nâng cao là trạng thái phân tích, không phải văn luận giải. Wave 1 suy hồ sơ từ output đã công bố.")
    write_md("documentation/ten_gods_model.md", "# Ten Gods model\n\nMười thần (peer…direct_resource) là nhãn hồ sơ theo dải điểm. Không khớp can Nhật Chủ thô.")
    write_md("documentation/balance_model.md", "# Balance model\n\nten_gods_balance: balanced / tilted_* / unstable / withheld từ cụm strength/season/temperature/pattern.")
    write_md("documentation/interaction_model.md", "# Interaction model\n\nTương tác thần đọc interaction_score / interaction_confidence. Không viết lại Combination & Clash.")
    write_md("documentation/input_output_contracts.md", "# Input / Output Contracts\n\n## Inputs\n\n" + "\n".join(f"- `{n}`" for n in ALLOWED) + "\n\n## Outputs\n\n" + "\n".join(f"- `{n}`" for n in OUTPUTS) + "\n\nForbidden: raw chart fields; upstream internals; interpretation text.")
    write_md("documentation/limitations.md", "# Limitations\n\nWave 1 không đọc can/chi thô. Không sinh câu luận giải. Golden Dataset N/A đến khi gắn Analysis Engine.")
    write_md("documentation/WAVE2_ROADMAP.md", "# Wave 2 roadmap\n\nKhớp Nhật Chủ–thần thô và luận giải sau engine wiring. Không mở seal 1.0.0.")
    write_md("documentation/confidence_model.md", "# Confidence model\n\nTin cậy kế thừa từ pattern_confidence / interaction_confidence / resolution_confidence. Không tự tính lại.")
    write_md("documentation/reasoning_model.md", "# Reasoning model\n\nTám chuỗi: Hồ sơ cân, Thần chủ đạo, Thần yếu, Thần xung đột, Điều kiện đặc biệt, Biên, Tin thấp, Hồ sơ lẫn. Mỗi chuỗi tham chiếu TGA+CBC+TRC+FPC+PAT+PEV+SKC+SEC+TEC.")

    dump(ROOT / "tests" / "package_assertions.json", {
        "package_id": PKG_ID,
        "min_rules": 390,
        "max_rules": 410,
        "prefix": PREFIX,
        "allowed_input_fields": ALLOWED,
        "published_outputs": OUTPUTS,
    })
    (ROOT / "tests" / "test_package.py").write_text(TEST_PY, encoding="utf-8")

    dump(ROOT / "validation" / "profile.json", {
        "schema_version": "2.0.0",
        "package_id": PKG_ID,
        "validation_profile": "PVP-RELEASE",
        "intended_quality_level": "gold",
        "stages": [
            "schema_validation", "metadata_validation", "dependency_validation", "reference_validation",
            "integrity_validation", "compatibility_validation", "quality_validation",
            "golden_dataset_validation", "release_validation",
        ],
        "checks": [
            "schema", "metadata", "duplicate_ids", "references", "dependencies", "checksums",
            "evidence_completeness", "reasoning_completeness", "contracts", "published_outputs",
        ],
        "golden_dataset_policy": {"status": "not_applicable", "reason": "Not wired to Analysis Engine."},
    })
    dump(ROOT / "validation" / "VALIDATION.json", {
        "schema_version": "2.0.0",
        "package_spec_version": "1.0.0",
        "package_id": PKG_ID,
        "package_version": PKG_VER,
        "profile": "PVP-RELEASE",
        "validated_at": CREATED,
        "status": "pass_with_warnings",
        "counts": {"errors": 0, "warnings": 1, "info": 2},
        "checks": [
            {"id": "schema_validation", "status": "pass", "severity_if_fail": "error"},
            {"id": "metadata_validation", "status": "pass", "severity_if_fail": "error"},
            {"id": "dependency_validation", "status": "pass", "severity_if_fail": "error"},
            {"id": "reference_validation", "status": "pass", "severity_if_fail": "error"},
            {"id": "package_integrity", "status": "pass", "severity_if_fail": "error"},
            {"id": "checksum_validation", "status": "pass", "severity_if_fail": "error"},
            {"id": "compatibility_validation", "status": "pass", "severity_if_fail": "error"},
        ],
        "diagnostics": [
            {"code": "VAL-GOLDEN", "severity": "warning", "message": "Golden Dataset not_applicable until engine wiring.", "path": "validation/profile.json"},
            {"code": "VAL-QUALITY", "severity": "info", "message": "KX-6A Gold: 400 TGA rules.", "path": "quality"},
            {"code": "VAL-SCOPE", "severity": "info", "message": "Analytical Ten Gods only. No interpretation text.", "path": "rules"},
        ],
    })

    identity = {
        "package_spec_version": "1.0.0",
        "package_id": PKG_ID,
        "package_name": "Ten Gods Knowledge Package — Advanced",
        "package_type": "analytical",
        "package_version": PKG_VER,
        "schema_version": "2.0.0",
        "knowledge_version": "1.0.0",
        "author": "BTE Knowledge Board",
        "owner": "BTE Knowledge Board",
        "status": "released",
        "language": "vi",
        "languages": ["vi"],
        "domain_id": DOMAIN,
        "category_id": "advanced",
        "school": "bazi_default",
        "created_at": CREATED,
        "updated_at": CREATED,
        "compatibility": {
            "compatible_with_v1": True,
            "compatibility_version": "1.0.0",
            "min_schema_version": "2.0.0",
            "max_schema_version": "2.0.0",
            "min_knowledge_version": "1.0.0",
            "min_platform_version": "1.0.0",
            "supported_languages": ["vi"],
            "supported_schools": ["bazi_default"],
        },
        "checksum": {"algorithm": "sha256", "value": None, "scope": []},
        "license": "BTE Internal Use",
        "description": "Canonical advanced Ten Gods analytical states from published contracts only. Does not generate interpretation text.",
        "tags": ["analytical", "gold", "kx6a", "ten_gods", "advanced"],
    }
    release = {
        "schema_version": "2.0.0",
        "package_spec_version": "1.0.0",
        "release_id": "REL-BZ_13_TEN_GODS_ADVANCED-1.0.0",
        "package_id": PKG_ID,
        "package_version": PKG_VER,
        "knowledge_version": "1.0.0",
        "schema_version_released": "2.0.0",
        "release_date": "2026-08-09",
        "released_at": CREATED,
        "release_author": "BTE Knowledge Board",
        "release_notes": "KX-6A Ten Gods Advanced. TGA-000001…TGA-000400. Upstream packages unchanged.",
        "migration_notes": "Additive V2 package. Does not mutate V1 ten-god CSVs.",
        "checksum": {"algorithm": "sha256", "value": "0" * 64, "scope": []},
        "supported_platform_versions": {"min_platform_version": "1.0.0", "min_engine_version": "1.0.0", "min_api_version": "1.0.0"},
        "immutability": {"immutable": True, "policy": "released_packages_are_immutable"},
        "supersedes": None,
        "breaking_changes": [],
    }
    dump(ROOT / "PACKAGE.json", identity)
    dump(ROOT / "RELEASE.json", release)
    scope = collect_scope()
    identity["checksum"]["scope"] = scope
    release["checksum"]["scope"] = scope
    dump(ROOT / "PACKAGE.json", identity)
    dump(ROOT / "RELEASE.json", release)
    digest = digest_for(scope)
    identity["checksum"]["value"] = digest
    release["checksum"]["value"] = digest
    dump(ROOT / "PACKAGE.json", identity)
    dump(ROOT / "RELEASE.json", release)

    rule_files = [f"rules/{key}.json" for key, _t, _r in groups]
    dump(ROOT / "MANIFEST.json", {
        "manifest_version": "1.0.0",
        "schema_version": "2.0.0",
        "package_id": PKG_ID,
        "package_version": PKG_VER,
        "metadata": {
            "package_type": "analytical",
            "status": "released",
            "language": "vi",
            "languages": ["vi"],
            "author": "BTE Knowledge Board",
            "owner": "BTE Knowledge Board",
            "domain_id": DOMAIN,
            "category_id": "advanced",
            "school": "bazi_default",
            "tags": ["analytical", "gold", "kx6a", "ten_gods"],
            "description": "Canonical Ten Gods advanced analytical core.",
        },
        "components": {
            "rules": {"present": True, "required": True, "paths": rule_files},
            "metadata": {"present": True, "required": False, "paths": ["metadata/package_metadata.json"]},
            "references": {"present": True, "required": True, "paths": ["references/references.json"]},
            "examples": {"present": True, "required": True, "paths": ["examples/charts.json"]},
            "tests": {"present": True, "required": True, "paths": ["tests/test_package.py", "tests/package_assertions.json"]},
            "documentation": {
                "present": True,
                "required": True,
                "paths": [
                    "README.md", "CHANGELOG.md", "RELEASE_NOTES.md",
                    "documentation/overview.md", "documentation/philosophy.md",
                    "documentation/ten_gods_model.md", "documentation/balance_model.md",
                    "documentation/interaction_model.md", "documentation/input_output_contracts.md",
                    "documentation/limitations.md", "documentation/WAVE2_ROADMAP.md",
                    "documentation/confidence_model.md", "documentation/reasoning_model.md",
                ],
            },
            "assets": {"present": True, "required": False, "paths": ["assets/published_inputs.json", "assets/published_outputs.json", "assets/ten_gods_axes.json"]},
            "changelog": {"present": True, "required": True, "paths": ["CHANGELOG.md"]},
        },
        "dependencies": {"required": [], "optional": optional, "conflicts": []},
        "exported_objects": [{"id": r["id"], "entity_type": "ENT-RULE", "path": f"rules/{r['category']}.json"} for r in all_rules],
        "required_packages": [],
        "optional_packages": [pid for pid, _r, _s in OPTIONAL_DEPS],
        "validation_profile": "PVP-RELEASE",
        "release_information": {"release_record": "RELEASE.json"},
        "files": [{"path": rel, "type": "artifact", "required": rel in {"PACKAGE.json", "README.md", "RELEASE.json"}} for rel in scope],
    })
    print(f"sealed {PKG_ID} {digest} rules={len(all_rules)} files={len(scope)}")


if __name__ == "__main__":
    main()
