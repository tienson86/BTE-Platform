"""Canonical pipeline duration metrics. No timing hooks."""

from __future__ import annotations

from typing import Final

from applications.metrics.metric_contract import MetricDefinition

PIPELINE_METRICS: Final[tuple[MetricDefinition, ...]] = (
    MetricDefinition(
        name="analysis_duration",
        domain="pipeline",
        kind="histogram",
        unit="ms",
        description="Canonical analysis pipeline duration.",
    ),
    MetricDefinition(
        name="decision_duration",
        domain="pipeline",
        kind="histogram",
        unit="ms",
        description="Canonical decision pipeline duration.",
    ),
    MetricDefinition(
        name="luck_duration",
        domain="pipeline",
        kind="histogram",
        unit="ms",
        description="Canonical luck pipeline duration.",
    ),
    MetricDefinition(
        name="interpretation_duration",
        domain="pipeline",
        kind="histogram",
        unit="ms",
        description="Canonical interpretation pipeline duration.",
    ),
    MetricDefinition(
        name="report_duration",
        domain="pipeline",
        kind="histogram",
        unit="ms",
        description="Canonical report pipeline duration.",
    ),
)
