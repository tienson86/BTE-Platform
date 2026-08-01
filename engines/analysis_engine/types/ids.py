"""Shared identifier type aliases."""

from __future__ import annotations

from typing import NewType, TypeAlias

ContextId: TypeAlias = str
PipelineId: TypeAlias = str
StageId: TypeAlias = str
AnalyzerId: TypeAlias = str
ModuleId: TypeAlias = str
ResultId: TypeAlias = str
DecisionId: TypeAlias = str
ScoreId: TypeAlias = str
EvidenceId: TypeAlias = str
RegistryEntryId: TypeAlias = str
ReferenceId: TypeAlias = str
RuleId: TypeAlias = str
SchemaId: TypeAlias = str
TraceId: TypeAlias = str
PackId: TypeAlias = str
ChartId: TypeAlias = str
ExecutionId: TypeAlias = str
SnapshotId: TypeAlias = str

ContextIdNT = NewType("ContextIdNT", str)
PipelineIdNT = NewType("PipelineIdNT", str)
StageIdNT = NewType("StageIdNT", str)
ResultIdNT = NewType("ResultIdNT", str)
RegistryEntryIdNT = NewType("RegistryEntryIdNT", str)
