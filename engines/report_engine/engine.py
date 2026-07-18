from dataclasses import dataclass
from .renderer import Renderer


@dataclass(slots=True)
class ReportResult:
    success: bool = True
    content: str = ""


class ReportEngine:
    def __init__(self):
        self.renderer = Renderer()

    def generate(self, *parts) -> ReportResult:
        return ReportResult(content=self.renderer.render({}, "default"))
