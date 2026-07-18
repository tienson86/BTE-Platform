from dataclasses import dataclass, field

@dataclass
class ReportParagraph:
    title: str = ""
    sentences: list = field(default_factory=list)

@dataclass
class ReportSection:
    title: str = ""
    paragraphs: list = field(default_factory=list)

@dataclass
class InterpretationReport:
    success: bool = True
    sections: list = field(default_factory=list)
    text: str = ""
    @property
    def section_count(self): return len(self.sections)
