"""
BTE Integration Pipeline.

Pipeline tổng điều phối toàn bộ quy trình:

Input
    ↓
Calendar Engine
    ↓
Bazi Engine
    ↓
Score Engine
    ↓
Pattern Engine
    ↓
Interpretation Engine
    ↓
Report Engine
    ↓
Output
"""

from __future__ import annotations

from typing import Optional

from .context import IntegrationContext
from .result import IntegrationResult
from .orchestrator import IntegrationOrchestrator


class Pipeline:
    """
    Pipeline tổng của BTE Platform.

    Chỉ chịu trách nhiệm điều phối.
    Không chứa thuật toán nghiệp vụ.
    """

    def __init__(
        self,
        orchestrator: Optional[IntegrationOrchestrator] = None,
    ):

        self.orchestrator = (
            orchestrator
            if orchestrator is not None
            else IntegrationOrchestrator()
        )

    def execute(
        self,
        context: IntegrationContext,
    ) -> IntegrationResult:
        """
        Thực thi toàn bộ Pipeline.

        Calendar
            ↓
        Bazi
            ↓
        Score
            ↓
        Pattern
            ↓
        Interpretation
            ↓
        Report
        """

        return self.orchestrator.execute(context)

    def execute_until(
        self,
        context: IntegrationContext,
        stage: str,
    ) -> IntegrationResult:
        """
        Chạy Pipeline đến một giai đoạn xác định.

        Ví dụ:

            execute_until(..., "score")
            execute_until(..., "pattern")
        """

        return self.orchestrator.execute_until(
            context,
            stage,
        )

    def reset(self) -> None:
        """
        Reset trạng thái Pipeline.
        """

        self.orchestrator.reset()

    @property
    def stages(self):

        return self.orchestrator.stages
