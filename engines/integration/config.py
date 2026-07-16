"""
Pipeline Config.
"""

from dataclasses import dataclass


@dataclass
class PipelineConfig:

    stop_on_error: bool = True

    enable_logging: bool = True

    enable_hooks: bool = True

    enable_validation: bool = True

    enable_cache: bool = True

    debug: bool = False
