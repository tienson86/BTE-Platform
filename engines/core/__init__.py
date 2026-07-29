"""
===============================================================================
BTE Platform - Core Framework
===============================================================================

Module:
    engines.core

Description:
    Core Framework dùng chung cho toàn bộ BTE Platform.

Bao gồm:

    • Constants
    • Enums
    • Exceptions
    • Validators
    • Utilities
    • Registry

Các Engine sử dụng:

    ✓ Calendar Engine
    ✓ Bazi Engine
    ✓ Interpretation Engine
    ✓ Report Engine
    ✓ Export Engine

Author:
    BTE Platform

Version:
    1.0.0
===============================================================================
"""

__version__ = "1.0.0"
__author__ = "BTE Platform"
__license__ = "MIT"

from .constants import *
from .enums import *
from .exceptions import *
from .validator import *
from .utils import *
from .registry import *

__all__ = [
    "__version__",
    "__author__",
    "__license__",
]
