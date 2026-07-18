from dataclasses import dataclass

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
