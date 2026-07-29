"""
ShenSha Service — classical star detection for BaziChart.shensha.

Uses the same lookup tables as RuleContextBuilder classical detection.
Does not invent stars; only maps day master / branches → known names.
"""

from __future__ import annotations

from typing import Iterable

from engines.rule_contract import signal_maps as maps


class ShenShaService:
    """Produce a list of Thần sát names for the production Bazi chart."""

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
        Detect classical Thần sát from pillars.

        Backward-compatible call styles:
        - ``calculate(year_branch, day_master)``
        - ``calculate(year_branch=..., day_master=...)``
        - ``calculate(day_master=..., year_branch=..., month_branch=..., ...)``
        """
        branch_list = [
            b
            for b in (
                list(branches)
                if branches is not None
                else [year_branch, month_branch, day_branch, hour_branch]
            )
            if b
        ]
        stem_list = [s for s in (list(stems) if stems is not None else []) if s]
        year_branch = year_branch or (branch_list[0] if branch_list else None)
        month_branch = month_branch or (
            branch_list[1] if len(branch_list) > 1 else None
        )
        day_branch = day_branch or (branch_list[2] if len(branch_list) > 2 else None)

        stars: list[str] = []

        if day_master in maps.TIAN_YI_BRANCHES:
            targets = maps.TIAN_YI_BRANCHES[day_master]
            if any(branch in targets for branch in branch_list):
                stars.append("Thiên Ất Quý Nhân")
                stars.append("Thiên Ất")

        if day_master in maps.WEN_CHANG_BRANCH:
            if maps.WEN_CHANG_BRANCH[day_master] in branch_list:
                stars.append("Văn Xương")

        if day_master in maps.LU_SHEN_BRANCH:
            if maps.LU_SHEN_BRANCH[day_master] in branch_list:
                stars.append("Lộc Thần")

        if year_branch and year_branch in maps.HONG_LUAN_OPPOSITE:
            target = maps.HONG_LUAN_OPPOSITE[year_branch]
            if target in branch_list:
                stars.append("Hồng Loan")
                stars.append("Thiên Hỷ")

        if day_branch in maps.HUA_GAI_BRANCHES:
            stars.append("Hoa Cái")

        if day_master in maps.YANG_REN_BRANCH:
            if maps.YANG_REN_BRANCH[day_master] in branch_list:
                stars.append("Dương Nhẫn")

        if month_branch in maps.TIAN_DE_BRANCH:
            token = maps.TIAN_DE_BRANCH[month_branch]
            if token in stem_list or token in branch_list:
                stars.append("Thiên Đức")
                stars.append("Thiên Đức Quý Nhân")

        if month_branch in maps.YUE_DE_STEM:
            token = maps.YUE_DE_STEM[month_branch]
            if token in stem_list:
                stars.append("Nguyệt Đức")
                stars.append("Nguyệt Đức Quý Nhân")

        return list(dict.fromkeys(stars))
