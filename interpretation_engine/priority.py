"""
interpretation_engine/priority.py

Quản lý ưu tiên, loại bỏ trùng lặp và sắp xếp
các InterpretationItem.
"""

from __future__ import annotations

from collections import defaultdict

from .context import InterpretationItem


class PriorityManager:
    """
    Quản lý ưu tiên các đoạn diễn giải.
    """

    def __init__(self) -> None:
        self._items: list[InterpretationItem] = []

    def add(self, item: InterpretationItem) -> None:
        self._items.append(item)

    def extend(self, items: list[InterpretationItem]) -> None:
        self._items.extend(items)

    def clear(self) -> None:
        self._items.clear()

    def build(self) -> list[InterpretationItem]:
        """
        Trả về danh sách đã:
            - bỏ trùng
            - sắp xếp theo priority
            - gom theo section
        """

        unique = self._remove_duplicate(self._items)

        unique.sort(
            key=lambda x: (
                x.section,
                -x.priority,
                -x.score,
                x.title,
            )
        )

        return unique

    @staticmethod
    def _remove_duplicate(
        items: list[InterpretationItem],
    ) -> list[InterpretationItem]:

        result: dict[str, InterpretationItem] = {}

        for item in items:

            key = f"{item.section}:{item.code}"

            if key not in result:
                result[key] = item
                continue

            old = result[key]

            if item.priority > old.priority:
                result[key] = item
                continue

            if (
                item.priority == old.priority
                and item.score > old.score
            ):
                result[key] = item

        return list(result.values())

    @staticmethod
    def group_by_section(
        items: list[InterpretationItem],
    ) -> dict[str, list[InterpretationItem]]:

        groups = defaultdict(list)

        for item in items:
            groups[item.section].append(item)

        return dict(groups)
