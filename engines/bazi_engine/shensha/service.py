"""
ShenSha Service — classical star detection for BaziChart.shensha.

Single calculation path: evaluate() returns structured matches.
calculate() projects canonical names from that result.
"""

from __future__ import annotations

from typing import Iterable

from engines.bazi_engine.shensha.catalog import (
    ID_HONG_LUAN,
    ID_HUA_GAI,
    ID_LU_SHEN,
    ID_TIAN_DE,
    ID_TIAN_XI,
    ID_TIAN_YI,
    ID_WEN_CHANG,
    ID_YANG_REN,
    ID_YUE_DE,
    LOCATION_BRANCH,
    LOCATION_STEM,
    PILLAR_KEYS,
    RULE_HONG_LUAN,
    RULE_HUA_GAI,
    RULE_LU_SHEN,
    RULE_TIAN_DE,
    RULE_TIAN_XI,
    RULE_TIAN_YI,
    RULE_WEN_CHANG,
    RULE_YANG_REN,
    RULE_YUE_DE,
    TARGET_BRANCH,
    TARGET_STEM,
    TARGET_STEM_OR_BRANCH,
    aliases_for,
    canonical_name_for,
)
from engines.bazi_engine.shensha.models import (
    ShenShaDetectionResult,
    ShenShaMatch,
    ShenShaOccurrence,
)
from engines.rule_contract import signal_maps as maps

_EMPTY = ShenShaDetectionResult()


class ShenShaService:
    """Detect classical Thần sát from visible stems and branches."""

    def calculate(
        self,
        year_branch: str | None = None,
        day_master: str | None = None,
        *,
        month_branch: str | None = None,
        day_branch: str | None = None,
        hour_branch: str | None = None,
        stems: Iterable[str] | None = None,
        branches: Iterable[str] | None = None,
    ) -> list[str]:
        """
        Legacy name projection from structured matches.

        Backward-compatible call styles:
        - ``calculate(year_branch, day_master)``
        - ``calculate(year_branch=..., day_master=...)``
        - ``calculate(day_master=..., year_branch=..., month_branch=..., ...)``
        """
        return self.evaluate(
            year_branch,
            day_master,
            month_branch=month_branch,
            day_branch=day_branch,
            hour_branch=hour_branch,
            stems=stems,
            branches=branches,
        ).canonical_names()

    def evaluate(
        self,
        year_branch: str | None = None,
        day_master: str | None = None,
        *,
        month_branch: str | None = None,
        day_branch: str | None = None,
        hour_branch: str | None = None,
        stems: Iterable[str] | None = None,
        branches: Iterable[str] | None = None,
    ) -> ShenShaDetectionResult:
        """Detect ShenSha with source, target, and pillar occurrences."""
        slots = _pillar_slots(
            year_branch=year_branch,
            month_branch=month_branch,
            day_branch=day_branch,
            hour_branch=hour_branch,
            stems=stems,
            branches=branches,
        )
        year_b, month_b, day_b, hour_b = (slot[2] for slot in slots)
        matches: list[ShenShaMatch] = []
        self._match_tian_yi(matches, day_master, slots)
        self._match_map_branch(
            matches,
            day_master,
            slots,
            maps.WEN_CHANG_BRANCH,
            ID_WEN_CHANG,
            RULE_WEN_CHANG,
        )
        self._match_map_branch(
            matches,
            day_master,
            slots,
            maps.LU_SHEN_BRANCH,
            ID_LU_SHEN,
            RULE_LU_SHEN,
        )
        self._match_year_target(
            matches,
            year_b,
            slots,
            maps.HONG_LUAN_OPPOSITE,
            ID_HONG_LUAN,
            RULE_HONG_LUAN,
        )
        self._match_year_target(
            matches,
            year_b,
            slots,
            maps.TIAN_XI_BRANCH,
            ID_TIAN_XI,
            RULE_TIAN_XI,
        )
        self._match_hua_gai(matches, day_b)
        self._match_map_branch(
            matches,
            day_master,
            slots,
            maps.YANG_REN_BRANCH,
            ID_YANG_REN,
            RULE_YANG_REN,
        )
        self._match_tian_de(matches, month_b, slots)
        self._match_yue_de(matches, month_b, slots)
        return ShenShaDetectionResult(matches=tuple(matches))

    def _match_tian_yi(
        self,
        matches: list[ShenShaMatch],
        day_master: str | None,
        slots: list[tuple[str, str | None, str | None]],
    ) -> None:
        if day_master not in maps.TIAN_YI_BRANCHES:
            return
        targets = maps.TIAN_YI_BRANCHES[day_master]
        occurrences = _branch_hits(slots, set(targets))
        _append_match(
            matches,
            star_id=ID_TIAN_YI,
            source_type="day_stem",
            source_value=day_master,
            target_type=TARGET_BRANCH,
            occurrences=occurrences,
            rule_source=RULE_TIAN_YI,
        )

    def _match_map_branch(
        self,
        matches: list[ShenShaMatch],
        day_master: str | None,
        slots: list[tuple[str, str | None, str | None]],
        table: dict[str, str],
        star_id: str,
        rule_source: str,
    ) -> None:
        if day_master not in table:
            return
        target = table[day_master]
        occurrences = _branch_hits(slots, {target})
        _append_match(
            matches,
            star_id=star_id,
            source_type="day_stem",
            source_value=day_master,
            target_type=TARGET_BRANCH,
            occurrences=occurrences,
            rule_source=rule_source,
            target_value=target,
        )

    def _match_year_target(
        self,
        matches: list[ShenShaMatch],
        year_branch: str | None,
        slots: list[tuple[str, str | None, str | None]],
        table: dict[str, str],
        star_id: str,
        rule_source: str,
    ) -> None:
        if not year_branch or year_branch not in table:
            return
        target = table[year_branch]
        occurrences = _branch_hits(slots, {target})
        _append_match(
            matches,
            star_id=star_id,
            source_type="year_branch",
            source_value=year_branch,
            target_type=TARGET_BRANCH,
            occurrences=occurrences,
            rule_source=rule_source,
            target_value=target,
        )

    def _match_hua_gai(
        self,
        matches: list[ShenShaMatch],
        day_branch: str | None,
    ) -> None:
        if day_branch not in maps.HUA_GAI_BRANCHES:
            return
        occurrences = (
            ShenShaOccurrence(
                pillar="day",
                location=LOCATION_BRANCH,
                target_value=day_branch,
            ),
        )
        _append_match(
            matches,
            star_id=ID_HUA_GAI,
            source_type="day_branch",
            source_value=day_branch,
            target_type=TARGET_BRANCH,
            occurrences=occurrences,
            rule_source=RULE_HUA_GAI,
            target_value=day_branch,
        )

    def _match_tian_de(
        self,
        matches: list[ShenShaMatch],
        month_branch: str | None,
        slots: list[tuple[str, str | None, str | None]],
    ) -> None:
        if month_branch not in maps.TIAN_DE_BRANCH:
            return
        token = maps.TIAN_DE_BRANCH[month_branch]
        occurrences = _stem_or_branch_hits(slots, token)
        _append_match(
            matches,
            star_id=ID_TIAN_DE,
            source_type="month_branch",
            source_value=month_branch,
            target_type=TARGET_STEM_OR_BRANCH,
            occurrences=occurrences,
            rule_source=RULE_TIAN_DE,
            target_value=token,
        )

    def _match_yue_de(
        self,
        matches: list[ShenShaMatch],
        month_branch: str | None,
        slots: list[tuple[str, str | None, str | None]],
    ) -> None:
        if month_branch not in maps.YUE_DE_STEM:
            return
        token = maps.YUE_DE_STEM[month_branch]
        occurrences = _stem_hits(slots, token)
        _append_match(
            matches,
            star_id=ID_YUE_DE,
            source_type="month_branch",
            source_value=month_branch,
            target_type=TARGET_STEM,
            occurrences=occurrences,
            rule_source=RULE_YUE_DE,
            target_value=token,
        )


def _pillar_slots(
    *,
    year_branch: str | None,
    month_branch: str | None,
    day_branch: str | None,
    hour_branch: str | None,
    stems: Iterable[str] | None,
    branches: Iterable[str] | None,
) -> list[tuple[str, str | None, str | None]]:
    """Build year→hour (pillar, stem, branch) slots."""
    stem_list = [None, None, None, None]
    branch_list = [year_branch, month_branch, day_branch, hour_branch]
    if stems is not None:
        for index, value in enumerate(list(stems)[:4]):
            stem_list[index] = value or stem_list[index]
    if branches is not None:
        for index, value in enumerate(list(branches)[:4]):
            if value:
                branch_list[index] = value
    named = (year_branch, month_branch, day_branch, hour_branch)
    for index, value in enumerate(named):
        if value:
            branch_list[index] = value
    return list(zip(PILLAR_KEYS, stem_list, branch_list))


def _branch_hits(
    slots: list[tuple[str, str | None, str | None]],
    targets: set[str],
) -> tuple[ShenShaOccurrence, ...]:
    """Collect visible branch matches without name-dedup of positions."""
    hits: list[ShenShaOccurrence] = []
    for pillar, _stem, branch in slots:
        if branch and branch in targets:
            hits.append(
                ShenShaOccurrence(
                    pillar=pillar,
                    location=LOCATION_BRANCH,
                    target_value=branch,
                )
            )
    return tuple(hits)


def _stem_hits(
    slots: list[tuple[str, str | None, str | None]],
    token: str,
) -> tuple[ShenShaOccurrence, ...]:
    """Collect visible stem matches."""
    hits: list[ShenShaOccurrence] = []
    for pillar, stem, _branch in slots:
        if stem and stem == token:
            hits.append(
                ShenShaOccurrence(
                    pillar=pillar,
                    location=LOCATION_STEM,
                    target_value=stem,
                )
            )
    return tuple(hits)


def _stem_or_branch_hits(
    slots: list[tuple[str, str | None, str | None]],
    token: str,
) -> tuple[ShenShaOccurrence, ...]:
    """Collect visible stem or branch matches for one token."""
    hits: list[ShenShaOccurrence] = []
    for pillar, stem, branch in slots:
        if stem and stem == token:
            hits.append(
                ShenShaOccurrence(
                    pillar=pillar,
                    location=LOCATION_STEM,
                    target_value=stem,
                )
            )
        if branch and branch == token:
            hits.append(
                ShenShaOccurrence(
                    pillar=pillar,
                    location=LOCATION_BRANCH,
                    target_value=branch,
                )
            )
    return tuple(hits)


def _append_match(
    matches: list[ShenShaMatch],
    *,
    star_id: str,
    source_type: str,
    source_value: str,
    target_type: str,
    occurrences: tuple[ShenShaOccurrence, ...],
    rule_source: str,
    target_value: str = "",
) -> None:
    """Publish one logical star when at least one occurrence exists."""
    if not occurrences:
        return
    resolved_target = target_value or "、".join(
        dict.fromkeys(item.target_value for item in occurrences)
    )
    matches.append(
        ShenShaMatch(
            id=star_id,
            canonical_name=canonical_name_for(star_id),
            aliases=aliases_for(star_id),
            source_type=source_type,
            source_value=source_value,
            target_type=target_type,
            target_value=resolved_target,
            occurrences=occurrences,
            rule_source=rule_source,
        )
    )
