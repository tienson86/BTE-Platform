"""HK-R1 audit dump. Temporary; not a product test."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.models import ProductionRequest
from engines.bazi_engine.engine import BaziChart, HIDDEN, Pillar
from engines.bazi_engine.ten_god import ten_god_name
from engines.pattern_engine.engine import PatternEngine
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.strength_engine.engine import StrengthEngine
from engines.strength_engine.utils.context_builder import build_strength_context
from engines.useful_god_engine.engine import UsefulGodEngine
from engines.useful_god_engine.utils.context_builder import build_useful_god_context

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "tests" / "golden_dataset" / "inputs"
OUT = ROOT / "release" / "gate_01" / "_hk_r1_dump.json"


def _parse_birth(raw: dict) -> dict:
    birth = raw["birth"]
    dt = datetime.fromisoformat(birth["solar_datetime"])
    return {
        "year": dt.year,
        "month": dt.month,
        "day": dt.day,
        "hour": dt.hour,
        "minute": dt.minute,
        "gender": birth.get("gender") or "male",
        "timezone": birth.get("timezone") or "Asia/Ho_Chi_Minh",
    }


def _classify(useful) -> dict:
    dung_tg = str(useful.useful_ten_god or useful.useful_god or "")
    dung_el = str(useful.useful_element or "")
    dung_st = str(useful.useful_stem or "")
    fav = list(useful.favorable_roles or [])
    exact = False
    same_el = False
    same_tg = False
    for role in fav:
        if (
            str(role.get("ten_god") or "") == dung_tg
            and str(role.get("stem") or "") == dung_st
            and str(role.get("element") or "") == dung_el
            and dung_tg
        ):
            exact = True
        if dung_el and str(role.get("element") or "") == dung_el:
            if not (
                str(role.get("stem") or "") == dung_st
                and str(role.get("ten_god") or "") == dung_tg
            ):
                same_el = True
        if dung_tg and str(role.get("ten_god") or "") == dung_tg and str(role.get("stem") or "") != dung_st:
            same_tg = True
    if exact and len(fav) == 1:
        relation = "exact_only"
    elif exact:
        relation = "exact_plus_others"
    elif same_el:
        relation = "same_element_diff_stem"
    else:
        relation = "not_repeated"
    return {
        "relation": relation,
        "exact": exact,
        "same_element_other": same_el,
        "same_ten_god_other_stem": same_tg,
        "hy_n": len(fav),
        "ky_n": len(useful.unfavorable_roles or []),
        "hy_set": tuple(useful.favorable_gods or []),
        "ky_set": tuple(useful.unfavorable_gods or []),
    }


def _row_from_output(label: str, out) -> dict:
    u = out.analysis.useful_god
    p = out.analysis.pattern
    s = out.analysis.strength
    b = out.analysis.bazi
    cls = _classify(u)
    pillars = ""
    if b is not None:
        pillars = " / ".join(
            f"{getattr(getattr(b, name, None), 'stem', '')} {getattr(getattr(b, name, None), 'branch', '')}"
            for name in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar")
        )
    return {
        "id": label,
        "pillars": pillars,
        "day_master": getattr(b, "day_master", None) if b else None,
        "strength": getattr(s, "strength_level", None) if s else None,
        "score": getattr(s, "strength_score", None) if s else None,
        "pattern": getattr(p, "pattern", None) if p else None,
        "rule": u.winning_rule_id if u else None,
        "group": u.winning_rule_group if u else None,
        "dung": u.useful_display if u else None,
        "dung_token": u.useful_god if u else None,
        "dung_tg": u.useful_ten_god if u else None,
        "dung_stem": u.useful_stem if u else None,
        "dung_el": u.useful_element if u else None,
        "hy": u.favorable_display if u else None,
        "ky": u.unfavorable_display if u else None,
        "hy_raw": list(u.favorable_gods or []) if u else [],
        "ky_raw": list(u.unfavorable_gods or []) if u else [],
        "climate": u.climate_display if u else None,
        "climate_rule": u.climate_rule_id if u else None,
        "reasoning": u.reasoning if u else None,
        **cls,
    }


def _chart_from_pillars(pillars: list[tuple[str, str]], gender: str) -> BaziChart:
    parts = [Pillar(stem=stem, branch=branch) for stem, branch in pillars]
    hidden = [stem for pillar in parts for stem in HIDDEN[pillar.branch]]
    dm = parts[2].stem
    ten_gods = [
        "Nhật Chủ" if pillar is parts[2] else ten_god_name(dm, pillar.stem)
        for pillar in parts
    ]
    return BaziChart(*parts, gender=gender, hidden_stems=hidden, ten_gods=ten_gods)


def _from_chart(label: str, chart: BaziChart) -> dict:
    strength = StrengthEngine().calculate(build_strength_context(chart))
    pctx = build_pattern_context(chart)
    pctx.strength_level = strength.strength_level
    pctx.strength_score = strength.strength_score
    pattern = PatternEngine().calculate(pctx)
    useful = UsefulGodEngine().calculate(build_useful_god_context(pctx, pattern))
    cls = _classify(useful)
    pillars = " / ".join(
        f"{p.stem} {p.branch}"
        for p in (chart.year_pillar, chart.month_pillar, chart.day_pillar, chart.hour_pillar)
    )
    return {
        "id": label,
        "pillars": pillars,
        "day_master": chart.day_pillar.stem,
        "strength": strength.strength_level,
        "score": strength.strength_score,
        "pattern": pattern.pattern,
        "rule": useful.winning_rule_id,
        "group": useful.winning_rule_group,
        "dung": useful.useful_display,
        "dung_token": useful.useful_god,
        "dung_tg": useful.useful_ten_god,
        "dung_stem": useful.useful_stem,
        "dung_el": useful.useful_element,
        "hy": useful.favorable_display,
        "ky": useful.unfavorable_display,
        "hy_raw": list(useful.favorable_gods or []),
        "ky_raw": list(useful.unfavorable_gods or []),
        "climate": useful.climate_display,
        "climate_rule": useful.climate_rule_id,
        "reasoning": useful.reasoning,
        "overall_ids": [str(x.get("rule_id")) for x in useful.overall_candidate_list],
        **cls,
    }


def main() -> None:
    runner = ProductionEngineRunner()
    rows = []
    files = sorted(INPUTS.glob("case_*.json"))
    for path in files:
        raw = json.loads(path.read_text(encoding="utf-8"))
        birth = _parse_birth(raw)
        req = ProductionRequest(
            case_id=path.stem,
            year=birth["year"],
            month=birth["month"],
            day=birth["day"],
            hour=birth["hour"],
            minute=birth["minute"],
            gender=birth["gender"],
            timezone=birth["timezone"],
        )
        out = runner.run(req)
        rows.append(_row_from_output(path.stem, out))

    named_births = [
        ("dung", 1985, 9, 18, 8, 0, "male", "Asia/Ho_Chi_Minh"),
        ("tuyen", 1984, 7, 13, 21, 1, "female", "Asia/Ho_Chi_Minh"),
        ("live_1989_0721", 1989, 7, 21, 15, 45, "male", "Asia/Ho_Chi_Minh"),
        ("live_1996_1129", 1996, 11, 29, 17, 20, "male", "Asia/Ho_Chi_Minh"),
        ("live_1987_0629", 1987, 6, 29, 6, 0, "male", "Asia/Ho_Chi_Minh"),
        ("live_1987_0907", 1987, 9, 7, 2, 0, "female", "Asia/Ho_Chi_Minh"),
        ("son", 1987, 1, 21, 4, 30, "male", "Asia/Bangkok"),
    ]
    named = {}
    for label, y, mo, d, h, mi, g, tz in named_births:
        req = ProductionRequest(
            case_id=label, year=y, month=mo, day=d, hour=h, minute=mi, gender=g, timezone=tz
        )
        named[label] = _row_from_output(label, runner.run(req))

    named["manh"] = _from_chart(
        "manh",
        _chart_from_pillars(
            [("Đinh", "Mão"), ("Đinh", "Mùi"), ("Kỷ", "Dậu"), ("Đinh", "Mão")],
            gender="male",
        ),
    )

    rel = Counter(r["relation"] for r in rows)
    by_rule = defaultdict(lambda: Counter())
    hy_sets = Counter()
    ky_sets = Counter()
    hy_n = []
    ky_n = []
    exact_n = 0
    same_el_n = 0
    not_rep = 0
    for r in rows:
        by_rule[r["rule"]][r["relation"]] += 1
        hy_sets[r["hy_set"]] += 1
        ky_sets[r["ky_set"]] += 1
        hy_n.append(r["hy_n"])
        ky_n.append(r["ky_n"])
        if r["exact"]:
            exact_n += 1
        if r["same_element_other"]:
            same_el_n += 1
        if r["relation"] == "not_repeated":
            not_rep += 1

    winners = Counter(r["rule"] for r in rows)
    payload = {
        "n": len(rows),
        "winners": dict(winners),
        "relation": dict(rel),
        "exact_dung_in_hy": exact_n,
        "same_element_other": same_el_n,
        "not_repeated": not_rep,
        "avg_hy": sum(hy_n) / len(hy_n) if hy_n else 0,
        "avg_ky": sum(ky_n) / len(ky_n) if ky_n else 0,
        "unique_hy_sets": len(hy_sets),
        "unique_ky_sets": len(ky_sets),
        "hy_sets": {str(k): v for k, v in hy_sets.most_common()},
        "ky_sets": {str(k): v for k, v in ky_sets.most_common()},
        "by_rule": {k: dict(v) for k, v in by_rule.items()},
        "named": named,
        "profile_hits": {
            "weak_nham_str001": [
                r["id"]
                for r in rows
                if r["day_master"] == "Nhâm"
                and r["strength"] == "weak"
                and r["rule"] == "str_001"
            ],
            "balanced_canh_str005": [
                r["id"]
                for r in rows
                if r["day_master"] == "Canh"
                and r["strength"] == "balanced"
                and r["rule"] == "str_005"
            ],
            "strong_ky_str004": [
                r["id"]
                for r in rows
                if r["day_master"] == "Kỷ"
                and r["strength"] == "strong"
                and r["rule"] == "str_004"
            ],
        },
        "rows": rows,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", OUT)
    print("n", payload["n"], "winners", payload["winners"])
    print("relation", payload["relation"])
    print("exact", exact_n, "same_el", same_el_n, "not_rep", not_rep)
    print("avg hy/ky", round(payload["avg_hy"], 2), round(payload["avg_ky"], 2))
    print("unique hy/ky sets", payload["unique_hy_sets"], payload["unique_ky_sets"])
    print("profiles", payload["profile_hits"])
    for key, row in named.items():
        print(
            key,
            row["pillars"],
            row["day_master"],
            row["strength"],
            row["score"],
            row["pattern"],
            row["rule"],
            row["dung"],
            "|",
            row["hy"],
            "|",
            row["ky"],
            "|",
            row["climate"],
        )


if __name__ == "__main__":
    main()
