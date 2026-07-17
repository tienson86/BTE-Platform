"""
Score Engine

Chức năng:
- Chấm điểm toàn bộ lá số Bát Tự.
- Tổng hợp điểm từ các module:
    + Ngũ hành
    + Thân vượng nhược
    + Thập thần
    + Cách cục
    + Dụng thần
    + Thần sát
    + Đại vận
- Xuất kết quả cho Interpretation Engine.
"""

from .score_engine import ScoreEngine
from .score_service import ScoreService
from .score_context import ScoreContext
from .score_result import ScoreResult

__all__ = [
    "ScoreEngine",
    "ScoreService",
    "ScoreContext",
    "ScoreResult"
]
