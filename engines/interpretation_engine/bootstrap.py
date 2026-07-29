"""
BTE Platform
Interpretation Engine

Bootstrap

Khởi tạo toàn bộ Interpretation Engine.
"""

from __future__ import annotations

from pathlib import Path

from .core.schema_loader import SchemaLoader
from .core.data_loader import DataLoader
from .core.validator import DataValidator
from .core.registry import Registry
from .core.plugin_manager import PluginManager
from .core.engine_validator import EngineValidator

from .pipeline import InterpretationPipeline
from .engine import InterpretationEngine


class Bootstrap:

    def __init__(self, root_directory: str | Path):

        self.root = Path(root_directory)

    def build(self):

        schema_loader = SchemaLoader(
            self.root / "schema"
        )

        validator = DataValidator(
            schema_loader
        )

        registry = Registry()

        plugins = PluginManager()

        engine_validator = EngineValidator(
            self.root / "schema"
        )

        pipeline = InterpretationPipeline(
            schema_loader=schema_loader,
            validator=validator,
            registry=registry,
            plugin_manager=plugins,
            engine_validator=engine_validator
        )

        engine = InterpretationEngine(
            pipeline=pipeline
        )

        return engine
