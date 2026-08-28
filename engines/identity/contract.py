"""Engine output → Identity field ownership. One owner per published field."""

from __future__ import annotations

# owner = engine/request field that already computes or supplies the value.
# identity = canonical identity path.
# analysis_result = published Analysis Result path.
# future_consumers = later sprints; not bound in BZ-ID-03.

IDENTITY_CONTRACT: tuple[dict[str, str], ...] = (
    {
        "owner": "BirthRequest.full_name",
        "identity": "person.full_name",
        "analysis_result": "identity.person.full_name",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "BirthRequest.gender",
        "identity": "person.gender",
        "analysis_result": "identity.person.gender",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "CalendarResult.solar_date",
        "identity": "person.solar_birth",
        "analysis_result": "identity.person.solar_birth",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "CalendarResult.lunar_date",
        "identity": "person.lunar_birth",
        "analysis_result": "identity.person.lunar_birth",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "CalendarResult.solar.hour+minute",
        "identity": "person.birth_time",
        "analysis_result": "identity.person.birth_time",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "BirthRequest.timezone",
        "identity": "person.timezone",
        "analysis_result": "identity.person.timezone",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "BirthRequest.birth_place",
        "identity": "person.birth_place",
        "analysis_result": "identity.person.birth_place",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "CalendarResult.solar_date",
        "identity": "calendar.solar_date",
        "analysis_result": "identity.calendar.solar_date",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "CalendarResult.lunar_date",
        "identity": "calendar.lunar_date",
        "analysis_result": "identity.calendar.lunar_date",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "CalendarResult.solar_term.name",
        "identity": "calendar.solar_term",
        "analysis_result": "identity.calendar.solar_term",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "BaziChart.year_pillar + pillar_contract",
        "identity": "four_pillars.year",
        "analysis_result": "identity.four_pillars.year",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "BaziChart.month_pillar + pillar_contract",
        "identity": "four_pillars.month",
        "analysis_result": "identity.four_pillars.month",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "BaziChart.day_pillar + pillar_contract",
        "identity": "four_pillars.day",
        "analysis_result": "identity.four_pillars.day",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "BaziChart.hour_pillar + pillar_contract",
        "identity": "four_pillars.hour",
        "analysis_result": "identity.four_pillars.hour",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "LuckContext.current_dayun",
        "identity": "luck.current_cycle",
        "analysis_result": "identity.luck.current_cycle",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "LuckContext.current_dayun.ganzhi",
        "identity": "luck.current_cycle_ganzhi",
        "analysis_result": "identity.luck.current_cycle_ganzhi",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "LuckContext.current_dayun.metadata.current_age_for_luck",
        "identity": "luck.current_cycle_age",
        "analysis_result": "identity.luck.current_cycle_age",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "LuckContext.current_dayun.index",
        "identity": "luck.cycle_index",
        "analysis_result": "identity.luck.cycle_index",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "LuckContext.current_dayun.metadata.reference_year",
        "identity": "luck.reference_year",
        "analysis_result": "identity.luck.reference_year",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "LuckContext.current_liunian.metadata.civil_year",
        "identity": "luck.current_year",
        "analysis_result": "identity.luck.current_year",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "LuckContext.current_liunian.ganzhi",
        "identity": "luck.current_liunian_ganzhi",
        "analysis_result": "identity.luck.current_liunian_ganzhi",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "LuckContext.current_liunian.year",
        "identity": "luck.current_liunian_year",
        "analysis_result": "identity.luck.current_liunian_year",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "narrative_result.sections[].id",
        "identity": "interpretation.section_keys",
        "analysis_result": "identity.interpretation.section_keys",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "narrative_result.sections[sec-conclusion]",
        "identity": "interpretation.conclusion",
        "analysis_result": "identity.interpretation.conclusion",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
    {
        "owner": "narrative_result.summary.next_action",
        "identity": "interpretation.action",
        "analysis_result": "identity.interpretation.action",
        "future_consumers": "Workspace / Report / PDF / DOCX",
    },
)

UNPUBLISHED: tuple[dict[str, str], ...] = (
    {
        "field": "identity.bone_weight.*",
        "reason": "No Bone Weight engine in the canonical analyze pipeline.",
    },
    {
        "field": "identity.calendar.weekday",
        "reason": "CalendarResult does not compute weekday.",
    },
    {
        "field": "identity.calendar.season",
        "reason": "CalendarResult does not expose season; Pattern/Temperature season is a different owner.",
    },
    {
        "field": "identity.luck.current_liuyue / current_liuri / current_liushi",
        "reason": "LuckEngine computes these periods; this sprint publishes Đại vận + Lưu niên identity only.",
    },
)
