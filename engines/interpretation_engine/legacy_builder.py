"""
Interpretation Builder
======================

Part 3

Chức năng:

- Nhận kết quả Rule Engine
- Chuẩn hóa Rule
- Tính trọng số
- Sắp xếp ưu tiên
- Gộp Rule
- Phân tích xung đột
- Tạo cấu trúc luận giải


Flow:

Rule Engine
      ↓
Interpretation Builder
      ↓
Sentence Generator
      ↓
Report Engine
"""


from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional




# =====================================================
# SECTION DATABASE
# =====================================================


INTERPRETATION_SECTIONS = [

    "tong_quan",

    "nguyen_cuc",

    "dung_than",

    "hy_than_ky_than",

    "tinh_cach",

    "suc_khoe",

    "tai_van",

    "su_nghiep",

    "hon_nhan",

    "tu_tuc",

    "dai_van",

    "luu_nien",

]


# WP4 canonical English section keys (always seeded)
WP4_SECTIONS = [
    "summary",
    "strength",
    "weakness",
    "warning",
    "career",
    "wealth",
    "relationship",
    "health",
    "personality",
    "luck",
    "useful_god",
    "pattern",
    "conclusion",
]


SECTION_ALIAS = {
    "tong_quan": "summary",
    "summary": "summary",
    "nguyen_cuc": "pattern",
    "pattern": "pattern",
    "dung_than": "useful_god",
    "useful_god": "useful_god",
    "hy_than_ky_than": "useful_god",
    "tinh_cach": "personality",
    "personality": "personality",
    "suc_khoe": "health",
    "health": "health",
    "tai_van": "wealth",
    "wealth": "wealth",
    "su_nghiep": "career",
    "career": "career",
    "hon_nhan": "relationship",
    "relationship": "relationship",
    "tu_tuc": "relationship",
    "dai_van": "luck",
    "luu_nien": "luck",
    "luck": "luck",
    "strength": "strength",
    "weakness": "weakness",
    "warning": "warning",
    "conclusion": "conclusion",
    "general": "summary",
}




# =====================================================
# RULE WEIGHT DATABASE
# =====================================================


RULE_LAYER_WEIGHT = {


    "cach_cuc": 1.50,

    "dung_than": 1.45,

    "hy_than_ky_than": 1.35,


    "dai_van": 1.30,

    "luu_nien": 1.25,


    "su_nghiep": 1.15,

    "tai_van": 1.15,

    "hon_nhan": 1.10,

    "tu_tuc": 1.10,


    "suc_khoe": 1.05,


    "than_sat": 0.90,


    "mac_dinh": 1.00

}





RULE_DEFAULT_STRUCTURE = {


    "rule_id": "",

    "rule_name": "",

    "category": "",

    "layer": "mac_dinh",

    "section": "tong_quan",

    "score": 0,

    "polarity": "neutral",

    "description": "",

    "priority": 99

}





# =====================================================
# DATA MODEL
# =====================================================


@dataclass
class InterpretationSection:


    name: str


    rules: List[Dict[str, Any]] = field(
        default_factory=list
    )


    positive_rules: List[Dict[str, Any]] = field(
        default_factory=list
    )


    negative_rules: List[Dict[str, Any]] = field(
        default_factory=list
    )


    warnings: List[Dict[str, Any]] = field(
        default_factory=list
    )


    score: float = 0




@dataclass
class InterpretationResult:


    summary: str = ""


    sections: Dict[str, InterpretationSection] = field(
        default_factory=dict
    )


    rules_used: List[str] = field(
        default_factory=list
    )


    strengths: List[Dict] = field(
        default_factory=list
    )


    weaknesses: List[Dict] = field(
        default_factory=list
    )


    warnings: List[Dict] = field(
        default_factory=list
    )


    confidence: float = 0

    # WP4 metrics (optional, backward-compatible defaults)
    sentences: List[Dict[str, Any]] = field(default_factory=list)
    matched_rule_count: int = 0
    sentence_count: int = 0
    section_count: int = 0
    coverage: float = 0.0
    unused_rules: List[str] = field(default_factory=list)

    # WP5 Priority Resolution (Matched → Resolved → Discarded)
    priority_resolution: Dict[str, Any] = field(default_factory=dict)
    resolved_rule_count: int = 0
    discarded_rules: List[Dict[str, Any]] = field(default_factory=list)





# =====================================================
# BUILDER
# =====================================================


class InterpretationBuilder:



    def __init__(self):

        self.sections = INTERPRETATION_SECTIONS




    # =================================================
    # MAIN BUILD
    # =================================================


    def build(
        self,
        matched_rules,
        context=None
    ):


        rules = [

            self.normalize_rule(rule)

            for rule in matched_rules

        ]



        rules = self.apply_rule_weight(
            rules
        )



        rules = self.priority_sort(
            rules
        )



        conflict_result = self.resolve_conflict(
            rules
        )



        grouped = self.group_rules(
            conflict_result["rules"]
        )



        sections = self.seed_sections()



        for name, items in grouped.items():
            canonical = SECTION_ALIAS.get(str(name), str(name))
            if canonical not in sections:
                sections[canonical] = self.build_section(canonical, [])
            existing = sections[canonical]
            built = self.build_section(canonical, items)
            existing.rules.extend(built.rules)
            existing.positive_rules.extend(built.positive_rules)
            existing.negative_rules.extend(built.negative_rules)
            existing.warnings.extend(built.warnings)
            existing.score += built.score

        # Route polarity into strength / weakness / warning
        self._route_polarity_sections(sections, conflict_result)

        # Fill empty narrative slots from RuleContext signals (map only)
        self._enrich_from_context(sections, context)

        summary = self.create_summary(sections)
        if summary and not sections["summary"].rules:
            sections["summary"].rules.append({
                "rule_id": "CTX_SUMMARY",
                "rule_name": "summary",
                "section": "summary",
                "description": summary,
                "sentence": summary,
                "polarity": "neutral",
                "priority": 100,
                "confidence": 1.0,
                "score": 0,
            })

        sentences = self._collect_sentences(sections)

        return InterpretationResult(


            summary=summary,


            sections=sections,


            rules_used=[

                r.get("rule_id")

                for r in rules

            ],


            strengths=conflict_result["positive"],


            weaknesses=conflict_result["negative"],


            warnings=conflict_result["warnings"],


            confidence=self.calculate_confidence(
                rules
            ),

            sentences=sentences,
            matched_rule_count=len(rules),
            sentence_count=len(sentences),
            section_count=sum(1 for sec in sections.values() if sec.rules),
        )




    # =================================================
    # NORMALIZE
    # =================================================


    def normalize_rule(
        self,
        rule
    ):


        data = RULE_DEFAULT_STRUCTURE.copy()

        data.update(rule)

        return data




    # =================================================
    # WEIGHT
    # =================================================


    def apply_rule_weight(
        self,
        rules
    ):


        result=[]



        for rule in rules:


            weight = RULE_LAYER_WEIGHT.get(

                rule.get(

                    "layer",

                    "mac_dinh"

                ),

                1

            )



            new = rule.copy()



            new["layer_weight"] = weight


            new["final_score"] = (

                new["score"]

                *

                weight

            )



            result.append(new)



        return result




    # =================================================
    # SORT
    # =================================================


    def priority_sort(
        self,
        rules
    ):
        """WP4: priority DESC, confidence DESC (fallback final_score)."""

        def _key(rule):
            try:
                priority = float(rule.get("priority", 0) or 0)
            except (TypeError, ValueError):
                priority = 0.0
            try:
                confidence = float(
                    rule.get(
                        "confidence",
                        rule.get("final_score", rule.get("score", 0)),
                    )
                    or 0
                )
            except (TypeError, ValueError):
                confidence = 0.0
            return (priority, confidence)

        return sorted(rules, key=_key, reverse=True)




    # =================================================
    # CONFLICT RESOLVER
    # =================================================


    def resolve_conflict(
        self,
        rules
    ):
        """
        Classify polarity after WP5 Priority Engine already filtered conflicts.

        Does not re-introduce contradictory pairs in the same section.
        """
        # Prefer higher priority when residual polarity clash remains
        by_section: Dict[str, List[Dict[str, Any]]] = {}
        for rule in rules:
            sec = str(rule.get("section") or "summary")
            by_section.setdefault(sec, []).append(rule)

        kept: List[Dict[str, Any]] = []
        for sec, items in by_section.items():
            positives = [r for r in items if r.get("polarity") == "positive"]
            negatives = [r for r in items if r.get("polarity") == "negative"]
            others = [
                r
                for r in items
                if r.get("polarity") not in {"positive", "negative"}
            ]
            if positives and negatives:
                # Keep the polarity group with the stronger top priority
                def _top_pri(group: List[Dict[str, Any]]) -> float:
                    try:
                        return max(float(r.get("priority", 0) or 0) for r in group)
                    except (TypeError, ValueError):
                        return 0.0

                if _top_pri(positives) >= _top_pri(negatives):
                    kept.extend(positives)
                    kept.extend(others)
                else:
                    kept.extend(negatives)
                    kept.extend(others)
            else:
                kept.extend(items)

        positive = [r for r in kept if r.get("polarity") == "positive"]
        negative = [r for r in kept if r.get("polarity") == "negative"]
        warnings = [
            r
            for r in kept
            if r.get("polarity") in {"warning", "warn"}
        ]

        return {
            "rules": kept,
            "positive": positive,
            "negative": negative,
            "warnings": warnings,
        }




    # =================================================
    # GROUP
    # =================================================


    def group_rules(
        self,
        rules
    ):


        grouped={}



        for rule in rules:


            section = rule.get(

                "section",

                "tong_quan"

            )


            grouped.setdefault(

                section,

                []

            ).append(rule)



        return grouped




    # =================================================
    # BUILD SECTION
    # =================================================


    def build_section(
        self,
        name,
        rules
    ):


        section = InterpretationSection(

            name=name,

            rules=rules

        )


        for rule in rules:


            if rule.get(
                "polarity"
            )=="positive":

                section.positive_rules.append(rule)


            elif rule.get(
                "polarity"
            )=="negative":

                section.negative_rules.append(rule)



        section.score=sum(

            r.get(

                "final_score",

                0

            )

            for r in rules

        )



        return section




    # =================================================
    # WP4 SECTION HELPERS
    # =================================================

    def seed_sections(self) -> Dict[str, InterpretationSection]:
        """Always create canonical WP4 section slots."""
        return {
            name: InterpretationSection(name=name)
            for name in WP4_SECTIONS
        }

    def _route_polarity_sections(
        self,
        sections: Dict[str, InterpretationSection],
        conflict_result: Dict[str, Any],
    ) -> None:
        """Route polarity into strength/weakness without duplicating rule_ids."""
        existing_ids = {
            str(rule.get("rule_id"))
            for section in sections.values()
            for rule in section.rules
            if rule.get("rule_id") is not None
        }

        def _append(section_name: str, rule: Dict[str, Any], bucket: str) -> None:
            rule_id = str(rule.get("rule_id") or "")
            if rule_id and rule_id in existing_ids:
                return
            item = dict(rule)
            item.setdefault("sentence", item.get("description", ""))
            sections[section_name].rules.append(item)
            getattr(sections[section_name], bucket).append(item)
            if rule_id:
                existing_ids.add(rule_id)

        for rule in conflict_result.get("positive") or []:
            _append("strength", rule, "positive_rules")
        for rule in conflict_result.get("negative") or []:
            _append("weakness", rule, "negative_rules")
        for rule in conflict_result.get("warnings") or []:
            if not isinstance(rule, dict):
                continue
            if rule.get("type") == "conflict" and not rule.get("description"):
                continue
            _append("warning", rule, "warnings")

    def _enrich_from_context(
        self,
        sections: Dict[str, InterpretationSection],
        context: Any,
    ) -> None:
        """Map existing RuleContext signals into empty narrative sections."""
        if not isinstance(context, dict):
            return

        pattern = context.get("pattern") or {}
        strength = context.get("strength") or {}
        useful = context.get("useful_god") or {}
        score = context.get("score") or {}
        bazi = context.get("bazi") or {}

        def _ensure(section: str, rule_id: str, text: str, polarity: str = "neutral") -> None:
            if not text:
                return
            if any(r.get("rule_id") == rule_id for r in sections[section].rules):
                return
            item = {
                "rule_id": rule_id,
                "rule_name": rule_id,
                "section": section,
                "description": text,
                "sentence": text,
                "polarity": polarity,
                "priority": 90,
                "confidence": 0.8,
                "score": 10,
            }
            sections[section].rules.append(item)

        pattern_name = pattern.get("name") or pattern.get("main_pattern")
        pattern_key = str(pattern_name or "").lower().replace(" ", "_")
        if pattern_name:
            _ensure(
                "pattern",
                "CTX_PATTERN",
                f"Cách cục chính: {pattern_name} (status={pattern.get('status')}).",
                "positive" if pattern.get("status") == "SUCCESS" else "neutral",
            )
            _ensure(
                "summary",
                "CTX_PATTERN_SUMMARY",
                f"Tổng quan: Nhật Chủ {bazi.get('day_master')}, cách cục {pattern_name}.",
            )

        level = strength.get("level")
        if level and level != "unknown":
            polarity = "positive" if level == "strong" else (
                "negative" if level == "weak" else "neutral"
            )
            target = "strength" if polarity != "negative" else "weakness"
            _ensure(
                target,
                "CTX_STRENGTH",
                f"Thân vượng/nhược: {level} (month={strength.get('month_status')}, "
                f"root={strength.get('root_level')}).",
                polarity,
            )
            if strength.get("control_type"):
                _ensure(
                    "weakness",
                    "CTX_CONTROL",
                    f"Yếu tố hao/khắc: {strength.get('control_type')}.",
                    "negative",
                )

        useful_name = useful.get("name")
        if useful_name:
            _ensure(
                "useful_god",
                "CTX_USEFUL_GOD",
                f"Dụng thần: {useful_name} ({useful.get('status')}).",
                "positive",
            )

        grade = score.get("grade")
        total = score.get("total_score")
        if grade or total:
            _ensure(
                "conclusion",
                "CTX_SCORE",
                f"Điểm tổng hợp: {total} — hạng {grade or 'N/A'}.",
            )

        # Career / wealth / relationship from pattern + ten gods
        ten_gods = context.get("ten_gods") or {}
        unique = set(ten_gods.get("unique") or [])
        if pattern_key in {"chinh_quan", "that_sat"} or (
            {"Chính Quan", "Thất Sát"} & unique
        ):
            _ensure(
                "career",
                "CTX_CAREER",
                "Quan/Sát hoặc cách Quan — liên quan sự nghiệp và trách nhiệm.",
                "neutral",
            )
        if {"Chính Tài", "Thiên Tài"} & unique or pattern_key in {
            "chinh_tai",
            "thien_tai",
        }:
            _ensure(
                "wealth",
                "CTX_WEALTH",
                "Tài tinh hiện diện — liên quan tài vận và nguồn lực vật chất.",
                "positive",
            )
        if {"Thương Quan", "Thực Thần"} & unique or pattern_name:
            _ensure(
                "relationship",
                "CTX_RELATIONSHIP",
                "Quan hệ xã hội chịu ảnh hưởng bởi cấu trúc Thập thần / cách cục.",
                "neutral",
            )
        if unique:
            _ensure(
                "personality",
                "CTX_PERSONALITY",
                f"Tính cách phản ánh thập thần nổi: {', '.join(list(unique)[:4])}.",
                "neutral",
            )

        luck = context.get("luck") or {}
        if luck.get("available"):
            _ensure(
                "luck",
                "CTX_LUCK",
                f"Đại vận: {luck.get('status') or 'đã phân tích'}.",
                "neutral",
            )
        else:
            _ensure(
                "luck",
                "CTX_LUCK",
                "Đại vận: chưa có dữ liệu upstream (Luck Engine).",
                "warning",
            )

        shensha = context.get("shensha") or {}
        stars = shensha.get("stars") or []
        if stars:
            _ensure(
                "health",
                "CTX_SHENSHA",
                f"Thần sát hiện diện: {', '.join(stars[:5])}.",
                "neutral",
            )

    @staticmethod
    def _collect_sentences(
        sections: Dict[str, InterpretationSection],
    ) -> List[Dict[str, Any]]:
        """Collect sentences; drop duplicate text (WP5: no duplicate sentences)."""
        sentences: List[Dict[str, Any]] = []
        seen_text: set[str] = set()
        for name, section in sections.items():
            for rule in section.rules:
                text = (
                    rule.get("sentence")
                    or rule.get("description")
                    or rule.get("message")
                    or ""
                )
                if not text:
                    continue
                key = str(text).strip().lower()
                if key in seen_text:
                    continue
                seen_text.add(key)
                rule.setdefault("sentence", text)
                sentences.append(
                    {
                        "section": name,
                        "rule_id": rule.get("rule_id"),
                        "sentence": text,
                        "priority": rule.get("priority", 0),
                        "confidence": rule.get("confidence", 0),
                    }
                )
        return sentences

    # =================================================
    # SUMMARY
    # =================================================


    def create_summary(
        self,
        sections
    ):
        active = [
            name
            for name, section in sections.items()
            if getattr(section, "rules", None)
        ]
        if not active:
            return "Chua kich hoat nhom luan giai."
        return "Da kich hoat cac nhom luan giai: " + ", ".join(active)




    # =================================================
    # CONFIDENCE
    # =================================================


    def calculate_confidence(
        self,
        rules
    ):


        if not rules:

            return 0



        avg = sum(

            r.get(

                "final_score",

                0

            )

            for r in rules

        ) / len(rules)



        return round(

            min(avg/100,1),

            2

        )





# =====================================================
# SERVICE
# =====================================================


def build_interpretation(

    matched_rules,

    context=None

):


    builder = InterpretationBuilder()


    return builder.build(

        matched_rules,

        context

    )
