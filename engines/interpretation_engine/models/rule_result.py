from dataclasses import dataclass
from .rule import Rule

@dataclass
class RuleResult:
    rule: Rule
    matched: bool = False
    score: float = 0
    @property
    def priority(self): return self.rule.priority
