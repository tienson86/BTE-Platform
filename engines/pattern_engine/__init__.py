"""
Pattern Engine

Chịu trách nhiệm:

- Nhận diện Cách Cục
- Kiểm tra Tòng Cách
- Kiểm tra Chuyên Cách
- Đánh giá thành cách/phá cách
- Cung cấp dữ liệu cho Interpretation Engine
"""

from .engine import PatternEngine
from .service import PatternService
from .context import PatternContext

__version__ = "1.0.0"

__all__ = [
    "PatternEngine",
    "PatternService",
    "PatternContext",
]
