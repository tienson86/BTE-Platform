"""
Unified Bazi truth — single producer for AnalysisResult.bazi.

Enriches the compact BaziEngine chart once. API and downstream engines
must consume the same BaziView / synced BaziChart.
"""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path
from typing import Any

from engines.bazi_engine.engine import BaziChart, Pillar
from engines.bazi_engine.ten_god import (
    day_master_element,
    day_master_yin_yang,
    ten_god_name,
)

from applications.api.models.analysis_result import BaziView, PillarView

REPO_ROOT = Path(__file__).resolve().parents[3]

BRANCH_HIDDEN_COUNT: dict[str, int] = {
    "Tý": 1,
    "Sửu": 3,
    "Dần": 3,
    "Mão": 1,
    "Thìn": 3,
    "Tỵ": 3,
    "Ngọ": 2,
    "Mùi": 3,
    "Thân": 3,
    "Dậu": 1,
    "Tuất": 3,
    "Hợi": 2,
}

PILLAR_ATTRS = ("year_pillar", "month_pillar", "day_pillar", "hour_pillar")


@lru_cache(maxsize=1)
def _load_nayin_lookup() -> dict[tuple[str, str], str]:
    """Load Nap Am names indexed by (stem, branch)."""
    path = REPO_ROOT / "database" / "02_quan_he" / "luc_thap_hoa_giap" / "du_lieu.csv"
    lookup: dict[tuple[str, str], str] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = (
                str(row.get("thien_can") or "").strip(),
                str(row.get("dia_chi") or "").strip(),
            )
            value = str(row.get("ngu_hanh_nap_am") or "").strip()
            if key[0] and key[1] and value:
                lookup[key] = value
    return lookup


@lru_cache(maxsize=1)
def _load_truong_sinh_lookup() -> dict[tuple[str, str], str]:
    """Load Truong Sinh state indexed by (day master stem, branch)."""
    path = (
        REPO_ROOT
        / "database"
        / "05_phan_tich"
        / "03_than_vuong_than_nhuoc"
        / "truong_sinh_nhat_chu.csv"
    )
    lookup: dict[tuple[str, str], str] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = (
                str(row.get("nhat_chu") or "").strip(),
                str(row.get("dia_chi") or "").strip(),
            )
            value = str(row.get("truong_sinh") or "").strip()
            if key[0] and key[1] and value:
                lookup[key] = value
    return lookup


def _slice_hidden_stems(chart: BaziChart) -> list[list[str]]:
    """Split flat hidden stem list into per-pillar groups."""
    flat = list(chart.hidden_stems or [])
    pillars = chart.pillars
    groups: list[list[str]] = []
    offset = 0
    for pillar in pillars:
        count = BRANCH_HIDDEN_COUNT.get(pillar.branch, 0)
        if count <= 0:
            groups.append([])
            continue
        groups.append(flat[offset : offset + count])
        offset += count
    return groups


def _pillar_view(
    pillar: Pillar,
    hidden: list[str],
    day_master: str,
    is_day_pillar: bool,
    nayin_lookup: dict[tuple[str, str], str],
    truong_sinh_lookup: dict[tuple[str, str], str],
) -> PillarView:
    """Build one enriched pillar view."""
    stem = pillar.stem
    branch = pillar.branch
    ten_god = "Nhật Chủ" if is_day_pillar else ten_god_name(day_master, stem)
    return PillarView(
        stem=stem,
        branch=branch,
        hidden_stems=list(hidden),
        ten_god=ten_god,
        nap_am=nayin_lookup.get((stem, branch), ""),
        truong_sinh=truong_sinh_lookup.get((day_master, branch), ""),
    )


def build_bazi_view(chart: BaziChart) -> BaziView:
    """
    Build the authoritative BaziView from a BaziEngine chart.

    This is the only enrichment path for nap_am / truong_sinh / per-pillar
    hidden stems / ten_god labels in the production API.
    """
    day_master = chart.day_master
    hidden_groups = _slice_hidden_stems(chart)
    nayin_lookup = _load_nayin_lookup()
    truong_sinh_lookup = _load_truong_sinh_lookup()
    pillars = chart.pillars
    views = [
        _pillar_view(
            pillars[i],
            hidden_groups[i] if i < len(hidden_groups) else [],
            day_master,
            i == 2,
            nayin_lookup,
            truong_sinh_lookup,
        )
        for i in range(4)
    ]
    return BaziView(
        year_pillar=views[0],
        month_pillar=views[1],
        day_pillar=views[2],
        hour_pillar=views[3],
        day_master=day_master,
        day_master_element=day_master_element(day_master),
        day_master_yin_yang=day_master_yin_yang(day_master),
        gender=chart.gender,
        hidden_stems=list(chart.hidden_stems or []),
        ten_gods=[view.ten_god for view in views],
        shensha=list(chart.shensha or []),
    )


def sync_chart_from_view(chart: BaziChart, view: BaziView) -> BaziChart:
    """
    Align compact chart lists with authoritative BaziView for downstream engines.

    Does not recalculate pillars — only syncs derived lists.
    """
    chart.ten_gods = view.pillar_ten_gods()
    chart.shensha = list(view.shensha)
    chart.gender = view.gender
    return chart


def bazi_source_fingerprint() -> dict[str, str]:
    """Provenance block for API meta."""
    return {
        "engine": "engines.bazi_engine.engine.BaziEngine",
        "method": "build",
        "contract": "li_chun_jdn_v1",
        "view": "applications.api.services.bazi_truth.build_bazi_view",
    }
