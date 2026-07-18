from dataclasses import dataclass

@dataclass
class PatternResult:
    success: bool = True
    pattern: str = "default"
    score: float = 0.0

class PatternEngine:
    def calculate(self, context): return PatternResult()
