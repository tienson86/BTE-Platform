"""Map AnalysisResult + InterpretationResult into ReportInputV1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from applications.api.models.analysis_result import (
    AnalysisResult,
    InterpretationSectionView,
    InterpretationView,
    PillarView,
)

from engines.interpretation_engine.foundation_constants import INTERPRETATION_VERSION
from engines.interpretation_engine.legacy_builder import InterpretationResult
from engines.report_engine.contracts.report_input_v1 import (
    REPORT_INPUT_VERSION,
    ReportCalendarV1,
    ReportDiagnosticsV1,
    ReportFiveElementsV1,
    ReportInputV1,
    ReportInterpretationSectionV1,
    ReportInterpretationV1,
    ReportLuckCycleV1,
    ReportLuckCyclesV1,
    ReportMetadataV1,
    ReportPatternV1,
    ReportPillarV1,
    ReportPillarsV1,
    ReportProfileV1,
    ReportShenShaItemV1,
    ReportStrengthV1,
    ReportTenGodsV1,
    ReportUsefulGodV1,
)
from engines.report_engine.foundation_constants import REPORT_VERSION
from engines.report_engine.interpretation_adapter import interpretation_to_dict
from applications.api.services.five_elements_truth import (
    ELEMENT_KEYS,
    normalize_element_key,
)
from applications.api.services.luck_truth import shape_luck_payload
from applications.api.services.ten_gods_truth import (
    TEN_GODS_NOTE,
    shape_ten_gods_payload,
)


@dataclass(slots=True)
class ReportInputV1Source:
    """Inputs for ReportInputV1Adapter."""

    analysis: AnalysisResult
    interpretation: InterpretationResult | None = None
    calendar: dict[str, Any] | None = None
    luck: dict[str, Any] | None = None
    five_elements: dict[str, Any] | None = None
    profile: ReportProfileV1 | None = None
    case_id: str = ""
    locale: str = "vi-VN"
    timezone: str = "Asia/Bangkok"
    knowledge_version: str = ""
    report_view: Mapping[str, Any] | None = None
    ten_gods_result: Any = None


def build_report_input_v1(source: ReportInputV1Source) -> ReportInputV1:
    """Build ReportInputV1 from runtime sources."""
    return ReportInputV1Adapter().build(source)


class ReportInputV1Adapter:
    """Adapter: runtime pipeline objects → ReportInputV1."""

    def build(self, source: ReportInputV1Source) -> ReportInputV1:
        """Produce a fully populated ReportInputV1 with diagnostics."""
        diagnostics = ReportDiagnosticsV1(
            source_contracts=[
                "applications.api.models.analysis_result.AnalysisResult",
                "engines.interpretation_engine.legacy_builder.InterpretationResult",
            ]
        )
        metadata = self._build_metadata(source, diagnostics)
        profile = self._build_profile(source, diagnostics)
        calendar = self._build_calendar(source, diagnostics)
        pillars = self._build_pillars(source.analysis, diagnostics)
        five_elements = self._build_five_elements(source, diagnostics)
        strength = self._build_strength(source.analysis, diagnostics)
        ten_gods = self._build_ten_gods(source, diagnostics)
        pattern = self._build_pattern(source.analysis, diagnostics)
        useful_god = self._build_useful_god(source.analysis, diagnostics)
        shensha = self._build_shensha(source.analysis, diagnostics)
        luck_cycles = self._build_luck_cycles(source, diagnostics)
        interpretation = self._build_interpretation(source, diagnostics)
        return ReportInputV1(
            metadata=metadata,
            profile=profile,
            calendar=calendar,
            pillars=pillars,
            five_elements=five_elements,
            strength=strength,
            ten_gods=ten_gods,
            pattern=pattern,
            useful_god=useful_god,
            shensha=shensha,
            luck_cycles=luck_cycles,
            interpretation=interpretation,
            diagnostics=diagnostics,
        )

    def _build_metadata(
        self,
        source: ReportInputV1Source,
        diagnostics: ReportDiagnosticsV1,
    ) -> ReportMetadataV1:
        knowledge_version = source.knowledge_version
        if not knowledge_version:
            diagnostics.missing_fields.append("metadata.knowledge_version")
        return ReportMetadataV1(
            report_version=REPORT_INPUT_VERSION,
            engine_version=REPORT_VERSION,
            knowledge_version=knowledge_version or INTERPRETATION_VERSION,
            case_id=source.case_id,
            locale=source.locale,
            timezone=source.timezone,
        )

    def _build_profile(
        self,
        source: ReportInputV1Source,
        diagnostics: ReportDiagnosticsV1,
    ) -> ReportProfileV1:
        if source.profile is not None:
            return source.profile
        diagnostics.fallbacks_used.append("profile.empty")
        diagnostics.missing_fields.append("profile")
        return ReportProfileV1(timezone=source.timezone)

    def _build_calendar(
        self,
        source: ReportInputV1Source,
        diagnostics: ReportDiagnosticsV1,
    ) -> ReportCalendarV1:
        payload = dict(source.calendar or {})
        if not payload:
            diagnostics.missing_fields.append("calendar")
            return ReportCalendarV1()
        lunar = payload.get("lunar") or {}
        if not isinstance(lunar, Mapping):
            lunar = {}
        lunar_year = lunar.get("year", payload.get("lunar_year"))
        lunar_month = lunar.get("month", payload.get("lunar_month"))
        lunar_day = lunar.get("day", payload.get("lunar_day"))
        leap = bool(
            lunar.get("is_leap_month")
            or lunar.get("leap")
            or payload.get("is_leap_month")
            or payload.get("leap_month")
        )
        lunar_date = str(payload.get("lunar_date") or "")
        if not lunar_date and lunar_day is not None and lunar_month is not None and lunar_year is not None:
            lunar_date = f"{int(lunar_day):02d}/{int(lunar_month):02d}/{int(lunar_year):04d}"
            if leap:
                lunar_date = f"{lunar_date} nhuận"
        solar_date = str(
            payload.get("solar_date")
            or payload.get("date")
            or ""
        )
        if not solar_date and isinstance(payload.get("solar"), Mapping):
            solar = payload["solar"]
            solar_date = (
                f"{int(solar.get('day') or 0):02d}/"
                f"{int(solar.get('month') or 0):02d}/"
                f"{int(solar.get('year') or 0):04d}"
            )
        if not solar_date and source.profile and source.profile.birth_date:
            solar_date = source.profile.birth_date
            diagnostics.fallbacks_used.append("calendar.solar_date.from_profile")
        solar_term_raw = payload.get("solar_term") or payload.get("jieqi") or ""
        if isinstance(solar_term_raw, Mapping):
            solar_term = str(solar_term_raw.get("name") or "")
        else:
            solar_term = str(solar_term_raw)
        timezone = ""
        tz_payload = payload.get("timezone")
        if isinstance(tz_payload, Mapping):
            timezone = str(tz_payload.get("name") or "")
        timezone = timezone or str(payload.get("timezone_name") or source.timezone or "")
        lunar_can_chi = payload.get("lunar_can_chi") if isinstance(payload.get("lunar_can_chi"), Mapping) else {}
        calendar = ReportCalendarV1(
            solar_date=solar_date,
            lunar_date=lunar_date,
            lunar_year=_as_int(lunar_year),
            lunar_month=_as_int(lunar_month),
            lunar_day=_as_int(lunar_day),
            leap_month=leap,
            lunar_year_can_chi=str(
                lunar_can_chi.get("year")
                or lunar.get("year_can_chi")
                or payload.get("lunar_year_can_chi")
                or ""
            ),
            solar_term=solar_term,
            solar_term_datetime=str(
                payload.get("solar_term_datetime") or payload.get("jieqi_datetime") or ""
            ),
            calendar_mode=str(payload.get("calendar_mode") or payload.get("mode") or "solar_utc7"),
            timezone=timezone,
            cung_phi=str(payload.get("cung_phi") or ""),
            menh_quai=str(payload.get("menh_quai") or ""),
            nhom_trach=str(payload.get("nhom_trach") or ""),
        )
        for field_name, value in (
            ("lunar_date", calendar.lunar_date),
            ("solar_term", calendar.solar_term),
        ):
            if not value:
                diagnostics.missing_fields.append(f"calendar.{field_name}")
        return calendar

    def _pillar_from_view(self, pillar: PillarView) -> ReportPillarV1:
        return ReportPillarV1(
            stem=pillar.stem,
            branch=pillar.branch,
            hidden_stems=list(pillar.hidden_stems),
            na_yin=pillar.nap_am,
            ten_god=pillar.ten_god,
            truong_sinh=pillar.truong_sinh,
        )

    def _build_pillars(
        self,
        analysis: AnalysisResult,
        diagnostics: ReportDiagnosticsV1,
    ) -> ReportPillarsV1:
        bazi = analysis.bazi
        return ReportPillarsV1(
            year=self._pillar_from_view(bazi.year_pillar),
            month=self._pillar_from_view(bazi.month_pillar),
            day=self._pillar_from_view(bazi.day_pillar),
            hour=self._pillar_from_view(bazi.hour_pillar),
        )

    def _build_five_elements(
        self,
        source: ReportInputV1Source,
        diagnostics: ReportDiagnosticsV1,
    ) -> ReportFiveElementsV1:
        raw: dict[str, Any] = {}
        published = source.five_elements or {}
        if published:
            counts = published.get("counts") if isinstance(published.get("counts"), Mapping) else {}
            for key in ELEMENT_KEYS:
                value = counts.get(key) if counts else None
                if value is None:
                    entry = published.get(key)
                    if isinstance(entry, Mapping):
                        value = entry.get("count")
                    elif isinstance(entry, (int, float)):
                        value = entry
                if value is not None:
                    raw[key] = value
            if raw:
                diagnostics.source_contracts.append("five_elements.analytical_counts")
        score = source.analysis.score
        if not raw and score is not None and score.wuxing_series:
            for item in score.wuxing_series:
                if not isinstance(item, Mapping):
                    continue
                element = normalize_element_key(
                    str(item.get("element") or item.get("name") or item.get("label") or "")
                )
                value = item.get("value", item.get("count"))
                if element and value is not None:
                    raw[element] = value
            if raw:
                diagnostics.source_contracts.append("AnalysisResult.score.wuxing_series")
        if not raw:
            diagnostics.missing_fields.append("five_elements")
        return ReportFiveElementsV1(
            wood=_as_float(raw.get("wood")),
            fire=_as_float(raw.get("fire")),
            earth=_as_float(raw.get("earth")),
            metal=_as_float(raw.get("metal")),
            water=_as_float(raw.get("water")),
            raw={key: raw.get(key) for key in ELEMENT_KEYS},
            normalized={},
            percentages={},
        )

    def _build_strength(
        self,
        analysis: AnalysisResult,
        diagnostics: ReportDiagnosticsV1,
    ) -> ReportStrengthV1:
        strength = analysis.strength
        bazi = analysis.bazi
        if strength is None:
            diagnostics.missing_fields.append("strength")
            return ReportStrengthV1(day_master=bazi.day_master)
        supporting: list[str] = []
        weakening: list[str] = []
        if strength.support_score:
            supporting.append(f"Hỗ trợ: {strength.support_score}")
        if strength.drain_score:
            weakening.append(f"Tiêu hao: {strength.drain_score}")
        if strength.control_score:
            weakening.append(f"Khắc chế: {strength.control_score}")
        return ReportStrengthV1(
            day_master=bazi.day_master,
            score=strength.strength_score,
            level=strength.strength_level,
            classification=strength.strength_level,
            seasonal_support=strength.season_score,
            root_support=strength.root_score,
            supporting_factors=supporting,
            weakening_factors=weakening,
            summary=strength.reasoning,
        )

    def _build_ten_gods(
        self,
        source: ReportInputV1Source,
        diagnostics: ReportDiagnosticsV1,
    ) -> ReportTenGodsV1:
        analysis = source.analysis
        bazi = analysis.bazi
        visible = list(bazi.ten_gods or bazi.pillar_ten_gods())
        hidden_stems = list(bazi.hidden_stems)
        score = analysis.score
        if score is not None and score.ten_god_series:
            diagnostics.source_contracts.append("AnalysisResult.score.ten_god_series")
        payload = self._canonical_ten_gods(source)
        visible_entries = [
            dict(item)
            for item in (payload.get("visible") or [])
            if isinstance(item, Mapping)
        ]
        hidden_entries = [
            dict(item)
            for item in (payload.get("hidden") or [])
            if isinstance(item, Mapping)
        ]
        if hidden_entries and not hidden_stems:
            hidden_stems = [
                str(item.get("hidden_stem") or item.get("stem") or "")
                for item in hidden_entries
                if item.get("hidden_stem") or item.get("stem")
            ]
        if not visible and not hidden_stems and not visible_entries:
            diagnostics.missing_fields.append("ten_gods")
        return ReportTenGodsV1(
            visible=visible,
            hidden=hidden_stems,
            summary=", ".join(visible) if visible else "",
            visible_entries=visible_entries,
            hidden_entries=hidden_entries,
            visible_summary=str(payload.get("visible_summary") or ""),
            hidden_summary=str(payload.get("hidden_summary") or ""),
            note=str(payload.get("note") or TEN_GODS_NOTE),
        )

    def _canonical_ten_gods(self, source: ReportInputV1Source) -> dict[str, Any]:
        """Prefer already-shaped TenGodsEngine output. Never recalculate."""
        candidate = source.ten_gods_result
        if candidate is None:
            candidate = getattr(source.analysis, "ten_gods_result", None)
        if candidate is None:
            return {}
        if hasattr(candidate, "to_dict"):
            return shape_ten_gods_payload(candidate)
        if not isinstance(candidate, Mapping):
            return {}
        hidden = candidate.get("hidden")
        if candidate.get("visible_labels") is not None or (
            isinstance(hidden, list)
            and hidden
            and isinstance(hidden[0], Mapping)
        ):
            return dict(candidate)
        if candidate.get("visible") or candidate.get("hidden"):
            return shape_ten_gods_payload(candidate)
        return {}

    def _build_pattern(
        self,
        analysis: AnalysisResult,
        diagnostics: ReportDiagnosticsV1,
    ) -> ReportPatternV1:
        pattern = analysis.pattern
        if pattern is None:
            diagnostics.missing_fields.append("pattern")
            return ReportPatternV1()
        secondary: list[str] = []
        if pattern.tong_cach:
            secondary.append(pattern.tong_cach)
        return ReportPatternV1(
            primary_pattern=pattern.cach_cuc or pattern.pattern,
            secondary_patterns=secondary,
            follow_pattern=pattern.dieu_hau,
            status="success" if pattern.success else "unknown",
            confidence=float(pattern.score) if pattern.score else None,
            explanation=pattern.than_vuong_nhuoc or pattern.than,
        )

    def _build_useful_god(
        self,
        analysis: AnalysisResult,
        diagnostics: ReportDiagnosticsV1,
    ) -> ReportUsefulGodV1:
        useful = analysis.useful_god
        pattern = analysis.pattern
        temperature = analysis.temperature
        if useful is None and pattern is None:
            diagnostics.missing_fields.append("useful_god")
            return ReportUsefulGodV1()
        return ReportUsefulGodV1(
            useful_god=(useful.useful_god if useful else "") or (pattern.dung_than if pattern else ""),
            favorable_gods=list(useful.favorable_gods if useful else []) or (
                [pattern.hy_than] if pattern and pattern.hy_than else []
            ),
            unfavorable_gods=list(useful.unfavorable_gods if useful else []) or (
                [pattern.ky_than] if pattern and pattern.ky_than else []
            ),
            neutral_gods=[],
            temperature_adjustment=(
                (temperature.climate_state if temperature else "")
                or (temperature.temperature_level if temperature else "")
            ),
            balancing_need=(temperature.balancing_need if temperature else ""),
            climate_evidence=(temperature.evidence_compact if temperature else ""),
            reasoning=(useful.reasoning if useful else "") or (pattern.dieu_hau if pattern else ""),
        )

    def _build_shensha(
        self,
        analysis: AnalysisResult,
        diagnostics: ReportDiagnosticsV1,
    ) -> list[ReportShenShaItemV1]:
        names = list(analysis.bazi.shensha or [])
        if not names:
            diagnostics.missing_fields.append("shensha")
            return []
        return [
            ReportShenShaItemV1(
                id=f"shensha_{index + 1}",
                name=name,
                category="shensha",
                present=True,
                evidence=name,
            )
            for index, name in enumerate(names)
        ]

    def _build_luck_cycles(
        self,
        source: ReportInputV1Source,
        diagnostics: ReportDiagnosticsV1,
    ) -> ReportLuckCyclesV1:
        payload = dict(source.luck or {})
        if not payload:
            diagnostics.missing_fields.append("luck_cycles")
            return ReportLuckCyclesV1()
        shaped = payload if "cycles" in payload else shape_luck_payload(payload)
        cycles_raw = shaped.get("cycles") or []
        cycles: list[ReportLuckCycleV1] = []
        if isinstance(cycles_raw, list):
            for item in cycles_raw:
                if not isinstance(item, Mapping):
                    continue
                cycles.append(
                    ReportLuckCycleV1(
                        index=int(item.get("index") or 0),
                        start_year=_as_int(item.get("year_start") or item.get("start_year")),
                        end_year=_as_int(item.get("year_end") or item.get("end_year")),
                        stem=str(item.get("stem") or item.get("heavenly_stem") or ""),
                        branch=str(item.get("branch") or item.get("earthly_branch") or ""),
                        age_start=_as_int(item.get("age_start") or item.get("start_age")),
                        age_end=_as_int(item.get("age_end") or item.get("end_age")),
                        summary=str(
                            item.get("gan_zhi")
                            or item.get("ganzhi")
                            or item.get("summary")
                            or ""
                        ),
                    )
                )
        if not cycles:
            diagnostics.missing_fields.append("luck_cycles.cycles")
        return ReportLuckCyclesV1(
            direction=str(shaped.get("direction") or ""),
            start_age=_as_int(shaped.get("start_age")),
            start_date=str(shaped.get("start_date") or ""),
            cycles=cycles,
        )

    def _build_interpretation(
        self,
        source: ReportInputV1Source,
        diagnostics: ReportDiagnosticsV1,
    ) -> ReportInterpretationV1:
        sections: list[ReportInterpretationSectionV1] = []
        executive_summary = ""
        conclusion = ""
        recommendations: list[str] = []
        warnings: list[str] = []
        confidence: float | None = None

        if source.analysis.interpretation is not None:
            diagnostics.source_contracts.append(
                "AnalysisResult.interpretation.InterpretationView"
            )
            view = source.analysis.interpretation
            sections.extend(self._sections_from_view(view))
            executive_summary = view.summary or executive_summary
            confidence = view.confidence if view.confidence else confidence
        elif source.interpretation is not None:
            diagnostics.source_contracts.append(
                "engines.interpretation_engine.legacy_builder.InterpretationResult"
            )
            data = _legacy_interpretation_payload(source.interpretation)
            executive_summary = str(data.get("summary") or "")
            confidence = _as_float(data.get("confidence"))
            sections.extend(self._sections_from_legacy_dict(data))
            for item in data.get("warnings") or []:
                if isinstance(item, Mapping):
                    warnings.append(str(item.get("message") or item.get("text") or item))
                else:
                    warnings.append(str(item))
            for item in data.get("strengths") or []:
                if isinstance(item, Mapping) and item.get("title"):
                    recommendations.append(str(item["title"]))
        else:
            diagnostics.missing_fields.append("interpretation")

        if source.report_view:
            diagnostics.fallbacks_used.append("interpretation.report_view_ignored")

        return ReportInterpretationV1(
            executive_summary=executive_summary,
            sections=sections,
            conclusion=conclusion,
            recommendations=recommendations,
            warnings=warnings,
            confidence=confidence,
        )

    def _sections_from_view(
        self,
        view: InterpretationView,
    ) -> list[ReportInterpretationSectionV1]:
        return [self._section_from_view(section) for section in view.sections]

    def _section_from_view(
        self,
        section: InterpretationSectionView,
    ) -> ReportInterpretationSectionV1:
        return ReportInterpretationSectionV1(
            id=section.id,
            title=section.title,
            content=section.body,
        )

    def _sections_from_legacy_dict(
        self,
        data: Mapping[str, Any],
    ) -> list[ReportInterpretationSectionV1]:
        sections: list[ReportInterpretationSectionV1] = []
        raw_sections = data.get("sections")
        if isinstance(raw_sections, Mapping):
            for index, (key, value) in enumerate(raw_sections.items()):
                if isinstance(value, Mapping):
                    content = str(
                        value.get("content")
                        or value.get("body")
                        or value.get("summary")
                        or ""
                    )
                    title = str(value.get("title") or value.get("name") or key)
                else:
                    content = str(value or "")
                    title = str(key)
                sections.append(
                    ReportInterpretationSectionV1(
                        id=str(key),
                        title=title,
                        content=content,
                        priority=index + 1,
                    )
                )
        elif isinstance(raw_sections, list):
            for index, item in enumerate(raw_sections):
                if isinstance(item, Mapping):
                    sections.append(
                        ReportInterpretationSectionV1(
                            id=str(item.get("id") or f"section_{index + 1}"),
                            title=str(item.get("title") or ""),
                            content=str(item.get("body") or item.get("content") or ""),
                            priority=index + 1,
                            confidence=_as_float(item.get("confidence")),
                        )
                    )
        sentences = data.get("sentences") or []
        if not sections and isinstance(sentences, list):
            grouped: dict[str, list[str]] = {}
            for sentence in sentences:
                if not isinstance(sentence, Mapping):
                    continue
                section_id = str(sentence.get("section") or "general")
                text = str(sentence.get("sentence") or sentence.get("text") or "").strip()
                if text:
                    grouped.setdefault(section_id, []).append(text)
            for index, (section_id, lines) in enumerate(grouped.items()):
                sections.append(
                    ReportInterpretationSectionV1(
                        id=section_id,
                        title=section_id,
                        content="\n\n".join(lines),
                        priority=index + 1,
                    )
                )
        return sections


def _as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _legacy_interpretation_payload(interpretation: InterpretationResult) -> dict[str, Any]:
    """Read legacy InterpretationResult without deep-copying unpicklable fields."""
    try:
        return interpretation_to_dict(interpretation)
    except TypeError:
        sections: dict[str, Any] = {}
        for key, section in (interpretation.sections or {}).items():
            if hasattr(section, "__dataclass_fields__"):
                from dataclasses import fields

                sections[str(key)] = {
                    field.name: getattr(section, field.name)
                    for field in fields(section)
                    if field.name != "luck_context"
                }
            elif isinstance(section, Mapping):
                sections[str(key)] = dict(section)
            else:
                sections[str(key)] = {
                    "name": getattr(section, "name", key),
                    "content": getattr(section, "content", ""),
                    "rules": list(getattr(section, "rules", []) or []),
                }
        return {
            "summary": interpretation.summary,
            "sections": sections,
            "sentences": list(interpretation.sentences or []),
            "confidence": interpretation.confidence,
            "warnings": list(interpretation.warnings or []),
            "strengths": list(interpretation.strengths or []),
            "weaknesses": list(interpretation.weaknesses or []),
        }
