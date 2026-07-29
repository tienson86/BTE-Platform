from dataclasses import dataclass
from .rule import Rule

@dataclass
class RuleResult:
    rule: Rule
    matched: bool = False
    score: float = 0
    @property
    def priority(self): return self.rule.priority

    @property
    def topic(self): return self.rule.topic

    @property
    def section(self): return self.rule.section

    @property
    def category(self): return self.rule.category

    @property
    def text(self): return self.rule.result
