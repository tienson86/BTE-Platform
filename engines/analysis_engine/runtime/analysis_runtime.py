"""AnalysisRuntime — public orchestration surface."""

from __future__ import annotations

import logging
from typing import Callable, Mapping

from engines.analysis_engine.runtime.cache_manager import CacheManager
from engines.analysis_engine.runtime.constants import (
    DEFAULT_DEPENDENCIES,
    RUNTIME_VERSION,
)
from engines.analysis_engine.runtime.dependency_resolver import DependencyResolver
from engines.analysis_engine.runtime.error_handler import ErrorHandler
from engines.analysis_engine.runtime.exceptions import (
    RegistrationError,
    StateError,
)
from engines.analysis_engine.runtime.execution_manager import ExecutionManager
from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    AnalysisResult,
    StageResult,
)
from engines.analysis_engine.runtime.module_executor import ModuleExecutor
from engines.analysis_engine.runtime.pipeline import RuntimePipeline
from engines.analysis_engine.runtime.protocols import (
    AnalysisModule,
    ModuleDescriptor,
)
from engines.analysis_engine.runtime.validation_manager import (
    ValidationManager,
    ValidationReport,
)

logger = logging.getLogger(__name__)

KnowledgeBinder = Callable[[AnalysisContext], None]


class AnalysisRuntime:
    """Orchestrates analysis modules for one or more Execution Units.

    Public API:
        - register(module)
        - validate(context)
        - execute(module, context=...) / execute(stage_id, context=...)
        - run(context)
        - evaluate(context)  — alias of run for Analysis Engine contract
    """

    def __init__(
        self,
        *,
        dependency_resolver: DependencyResolver | None = None,
        cache_manager: CacheManager | None = None,
        error_handler: ErrorHandler | None = None,
        validation_manager: ValidationManager | None = None,
        pipeline: RuntimePipeline | None = None,
        knowledge_binder: KnowledgeBinder | None = None,
        require_all_canonical_stages: bool = True,
        runtime_version: str = RUNTIME_VERSION,
    ) -> None:
        self._runtime_version = runtime_version
        self._require_all = require_all_canonical_stages
        self._knowledge_binder = knowledge_binder

        self._dependencies = dependency_resolver or DependencyResolver()
        self._cache = cache_manager or CacheManager()
        self._errors = error_handler or ErrorHandler()
        self._validation = validation_manager or ValidationManager()
        self._pipeline = pipeline or RuntimePipeline(
            dependency_resolver=self._dependencies,
        )
        self._executor = ModuleExecutor(
            validation_manager=self._validation,
            error_handler=self._errors,
            cache_manager=self._cache,
            runtime_version=runtime_version,
        )
        self._execution = ExecutionManager(
            module_executor=self._executor,
            validation_manager=self._validation,
            dependency_resolver=self._dependencies,
            error_handler=self._errors,
            cache_manager=self._cache,
            runtime_version=runtime_version,
        )
        self._registry: dict[str, ModuleDescriptor] = {}

    @property
    def runtime_version(self) -> str:
        """Runtime framework version."""
        return self._runtime_version

    @property
    def registered_modules(self) -> Mapping[str, ModuleDescriptor]:
        """Read-only view of registered module descriptors."""
        return dict(self._registry)

    def register(self, module: AnalysisModule) -> None:
        """Register an analysis module by stable stage_id."""
        if not isinstance(module, AnalysisModule):
            raise RegistrationError(
                "module must implement AnalysisModule protocol",
            )
        stage_id = module.stage_id
        if not stage_id:
            raise RegistrationError("module.stage_id is required")
        if stage_id in self._registry:
            raise RegistrationError(
                f"Module already registered: {stage_id}",
                stage_id=stage_id,
            )

        dependencies = tuple(module.dependencies)
        if not dependencies and stage_id in DEFAULT_DEPENDENCIES:
            # Modules may omit dependencies; runtime applies defaults.
            dependencies = DEFAULT_DEPENDENCIES[stage_id]

        self._dependencies.register(stage_id, dependencies)
        self._registry[stage_id] = ModuleDescriptor(
            module,
            dependencies=dependencies,
        )
        logger.info(
            "module_registered",
            extra={
                "stage_id": stage_id,
                "module_version": module.version,
                "dependencies": list(dependencies),
            },
        )

    def validate(self, context: AnalysisContext) -> ValidationReport:
        """Validate AnalysisContext without executing the full pipeline."""
        return self._validation.validate_context(context)

    def execute(
        self,
        module: AnalysisModule | str,
        context: AnalysisContext,
    ) -> StageResult:
        """Execute a single registered (or provided) module against context."""
        resolved = self._resolve_module(module)
        self._bind_knowledge(context)
        deps = self._dependencies.dependencies_of(resolved.stage_id)
        if resolved.stage_id in self._registry:
            deps = self._registry[resolved.stage_id].dependencies
        result, _metrics, _span = self._executor.execute(
            resolved,
            context,
            dependencies=deps,
        )
        context.publish_stage_result(result)
        return result

    def run(self, context: AnalysisContext) -> AnalysisResult:
        """Execute the full sequential pipeline and return AnalysisResult."""
        if self._require_all:
            self._pipeline.ensure_complete(tuple(self._registry.keys()))
        order = self._pipeline.resolve(tuple(self._registry.keys()))
        if not order:
            raise StateError("No modules registered for pipeline execution")

        self._bind_knowledge(context)
        logger.info(
            "pipeline_starting",
            extra={
                "request_id": context.request_id,
                "order": list(order),
                "runtime_version": self._runtime_version,
            },
        )
        return self._execution.run_pipeline(
            context,
            registry=self._registry,
            order=order,
        )

    def evaluate(self, context: AnalysisContext) -> AnalysisResult:
        """Alias of :meth:`run` for Analysis Engine public contract."""
        return self.run(context)

    def _resolve_module(self, module: AnalysisModule | str) -> AnalysisModule:
        if isinstance(module, str):
            descriptor = self._registry.get(module)
            if descriptor is None:
                raise StateError(
                    f"Module not registered: {module}",
                    stage_id=module,
                )
            return descriptor.module
        return module

    def _bind_knowledge(self, context: AnalysisContext) -> None:
        if self._knowledge_binder is None:
            return
        self._knowledge_binder(context)
