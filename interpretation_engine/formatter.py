"""
interpretation_engine/formatter.py

Ghép toàn bộ InterpretationItem thành báo cáo.
"""

from __future__ import annotations

from .context import InterpretationItem


class Formatter:

    SECTION_TITLE = {
        "overview": "I. Tổng quan",
        "personality": "II. Tính cách",
        "five_elements": "III. Ngũ hành",
        "career": "IV. Công việc",
        "wealth": "V. Tài vận",
        "marriage": "VI. Hôn nhân",
        "health": "VII. Sức khỏe",
        "children": "VIII. Tử tức",
        "luck": "IX. Đại vận",
        "fengshui": "X. Phong thủy",
        "summary": "XI. Tổng kết",
    }

    def build(
        self,
        groups: dict[str, list[InterpretationItem]],
    ) -> str:

        lines: list[str] = []

        for section in self.SECTION_TITLE:

            if section not in groups:
                continue

            lines.append(self.SECTION_TITLE[section])
            lines.append("")

            for item in groups[section]:

                lines.append(f"### {item.title}")
                lines.append(item.content)
                lines.append("")

        return "\n".join(lines)
