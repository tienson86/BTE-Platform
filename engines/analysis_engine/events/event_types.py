"""Internal Analysis Engine event type catalog."""

from __future__ import annotations

from enum import Enum


class EventType(str, Enum):
    """Internal runtime event types for Analysis Engine lifecycle signals.

    These events are in-process only. They are not external message topics.
    """

    PIPELINE_STARTED = "pipeline.started"
    PIPELINE_COMPLETED = "pipeline.completed"
    PIPELINE_FAILED = "pipeline.failed"
    STAGE_STARTED = "stage.started"
    STAGE_COMPLETED = "stage.completed"
    STAGE_FAILED = "stage.failed"
    CONTEXT_CREATED = "context.created"
    CONTEXT_INITIALIZED = "context.initialized"
    CONTEXT_EXPANDED = "context.expanded"
    CONTEXT_VALIDATED = "context.validated"
    CONTEXT_FINALIZED = "context.finalized"
    CONTEXT_DISPOSED = "context.disposed"
    RESULT_CREATED = "result.created"
    RESULT_MERGED = "result.merged"
    RESULT_FINALIZED = "result.finalized"
    REGISTRY_LOADED = "registry.loaded"
    REGISTRY_RESOLVED = "registry.resolved"
    ERROR_OCCURRED = "runtime.error"
    CUSTOM = "custom"
