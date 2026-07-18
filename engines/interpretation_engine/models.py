from dataclasses import dataclass, field
from typing import Any


@dataclass
class InterpretationContext:
    bazi_result: Any = None
    options: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    data: dict[str, Any] = field(default_factory=dict)

    def set(self, key, value): self.data[key] = value
    def get(self, key, default=None): return self.data.get(key, default)
    def update(self, values): self.data.update(values)
    def resolve(self, path, default=None):
        current = self.data
        for part in path.split("."):
            current = current.get(part, default) if isinstance(current, dict) else getattr(current, part, default)
            if current is default: break
        return current


@dataclass
class Rule:
    id: str = ""
    name: str = ""
    module: str = ""
    category: str = ""
    topic: str = ""
    section: str = ""
    condition: str = ""
    result: str = ""
    priority: int = 0
    enabled: bool = True


@dataclass
class RuleResult:
    rule: Rule
    matched: bool = False


@dataclass
class InterpretationReport:
    success: bool = True
    sections: list[Any] = field(default_factory=list)
    text: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def section_count(self): return len(self.sections)


InterpretationResult = InterpretationReport
