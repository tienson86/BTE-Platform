"""Template Engine architecture and runtime package.

Infrastructure for template *reference* loading, resolution, validation,
and binding shells. No template library. No hard-coded templates.
"""

from __future__ import annotations

from engines.interpretation_engine.template_engine.interface import (
    TemplateEngine,
    TemplateEngineInterface,
)
from engines.interpretation_engine.template_engine.loader import Loader
from engines.interpretation_engine.template_engine.metadata import (
    Metadata,
    TemplateBinding,
    TemplateRef,
    TemplateRenderShell,
)
from engines.interpretation_engine.template_engine.renderer import Renderer
from engines.interpretation_engine.template_engine.resolver import Resolver
from engines.interpretation_engine.template_engine.validator import Validator

__all__ = [
    "Loader",
    "Metadata",
    "Renderer",
    "Resolver",
    "TemplateBinding",
    "TemplateEngine",
    "TemplateEngineInterface",
    "TemplateRef",
    "TemplateRenderShell",
    "Validator",
]
