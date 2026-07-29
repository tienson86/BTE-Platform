"""
Pattern Context Model.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class PatternContextModel:

    pillars: Dict = field(default_factory=dict)

    ten_gods: Dict = field(default_factory=dict)

    hidden_stems: Dict = field(default_factory=dict)

    wuxing: Dict = field(default_factory=dict)

    strength: Dict = field(default_factory=dict)

    shensha: List[str] = field(default_factory=list)

    useful_god: str = ""

    extra: Dict = field(default_factory=dict)
