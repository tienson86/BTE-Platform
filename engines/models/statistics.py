"""
statistics.py
=============

Statistics Model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ReportStatistics:
    """
    Thống kê báo cáo.
    """

    total_rules: int = 0

    matched_rules: int = 0

    skipped_rules: int = 0

    total_sections: int = 0

    total_paragraphs: int = 0

    total_sentences: int = 0

    average_score: float = 0.0

    execution_time: float = 0.0
