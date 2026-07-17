"""
BTE Platform
=============================

Interpretation Engine

Rule Matcher

Điều phối toàn bộ quá trình lựa chọn Rule.

Author : BTE Project
Version : 1.0.0
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any
from typing import Iterable

from .cache import MatcherCache
from .context import MatchContext
from .result import MatchResult

from .condition_evaluator import ConditionEvaluator
from .priority_resolver import PriorityResolver
from .conflict_resolver import ConflictResolver


class RuleMatcher:
    """
    Rule Matcher trung tâm.

    Trách nhiệm

    - Quản lý Rule
    - Match Rule
    - Cache
    - Priority
    - Conflict
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        evaluator: ConditionEvaluator,
        priority_resolver: PriorityResolver,
        conflict_resolver: ConflictResolver,
        cache: MatcherCache | None = None,
    ) -> None:

        self._evaluator = evaluator

        self._priority = priority_resolver

        self._conflict = conflict_resolver

        self._cache = cache or MatcherCache()

        # -----------------------------
        # Rule Storage
        # -----------------------------

        self._rules: list[dict[str, Any]] = []

        self._rule_index: dict[str, dict[str, Any]] = {}

        # chapter -> rules
        self._chapter_index: dict[
            str,
            list[dict]
        ] = defaultdict(list)

        # tag -> rules
        self._tag_index: dict[
            str,
            list[dict]
        ] = defaultdict(list)

        # template -> rules
        self._template_index: dict[
            str,
            list[dict]
        ] = defaultdict(list)

        self._statistics = {

            "rule_count": 0,

            "chapter_count": 0,

            "tag_count": 0,

            "template_count": 0,

        }

    # =====================================================
    # Rule Management
    # =====================================================

    def clear(self) -> None:
        """
        Xóa toàn bộ Rule.
        """

        self._rules.clear()

        self._rule_index.clear()

        self._chapter_index.clear()

        self._tag_index.clear()

        self._template_index.clear()

        self._cache.clear()

        self._update_statistics()

    def load_rules(
        self,
        rules: Iterable[dict],
    ) -> None:
        """
        Load toàn bộ Rule.
        """

        self.clear()

        for rule in rules:

            self.add_rule(rule)

    def add_rule(
        self,
        rule: dict,
    ) -> None:
        """
        Thêm một Rule.
        """

        rule_id = rule["rule_id"]

        self._rules.append(rule)

        self._rule_index[rule_id] = rule

        chapter = rule.get("chapter")

        if chapter:

            self._chapter_index[
                chapter
            ].append(rule)

        template = rule.get(
            "template_id"
        )

        if template:

            self._template_index[
                template
            ].append(rule)

        for tag in rule.get(
            "tags",
            [],
        ):

            self._tag_index[
                tag
            ].append(rule)

        self._update_statistics()

    def remove_rule(
        self,
        rule_id: str,
    ) -> bool:
        """
        Xóa Rule.

        Returns
        -------
        bool
        """

        if rule_id not in self._rule_index:

            return False

        rule = self._rule_index.pop(rule_id)

        if rule in self._rules:

            self._rules.remove(rule)

        chapter = rule.get("chapter")

        if chapter:

            if rule in self._chapter_index[chapter]:

                self._chapter_index[
                    chapter
                ].remove(rule)

        template = rule.get(
            "template_id"
        )

        if template:

            if rule in self._template_index[
                template
            ]:

                self._template_index[
                    template
                ].remove(rule)

        for tag in rule.get(
            "tags",
            [],
        ):

            if rule in self._tag_index[tag]:

                self._tag_index[tag].remove(
                    rule
                )

        self._update_statistics()

        return True

    # =====================================================
    # Query
    # =====================================================

    def has_rule(
        self,
        rule_id: str,
    ) -> bool:

        return rule_id in self._rule_index

    def get_rule(
        self,
        rule_id: str,
    ) -> dict | None:

        return self._rule_index.get(rule_id)

    def get_rules(self) -> list[dict]:

        return self._rules

    def get_rules_by_chapter(
        self,
        chapter: str,
    ) -> list[dict]:

        return self._chapter_index.get(
            chapter,
            [],
        )

    def get_rules_by_template(
        self,
        template_id: str,
    ) -> list[dict]:

        return self._template_index.get(
            template_id,
            [],
        )

    def get_rules_by_tag(
        self,
        tag: str,
    ) -> list[dict]:

        return self._tag_index.get(
            tag,
            [],
        )

    def count(self) -> int:

        return len(self._rules)
          # =====================================================
    # Statistics
    # =====================================================

    @property
    def statistics(self) -> dict[str, int]:
        """
        Thống kê hiện tại của Rule Matcher.
        """

        return self._statistics.copy()

    def _update_statistics(self) -> None:

        self._statistics = {

            "rule_count": len(self._rules),

            "chapter_count": len(
                self._chapter_index
            ),

            "tag_count": len(
                self._tag_index
            ),

            "template_count": len(
                self._template_index
            ),

        }

    # =====================================================
    # Filters
    # =====================================================

    def filter_by_enabled(
        self,
        rules: Iterable[dict],
    ) -> list[dict]:
        """
        Chỉ lấy Rule đang bật.
        """

        return [

            rule

            for rule in rules

            if rule.get(
                "enabled",
                True,
            )

        ]

    def filter_by_priority(
        self,
        rules: Iterable[dict],
        minimum: int,
    ) -> list[dict]:
        """
        Lọc theo Priority.
        """

        return [

            rule

            for rule in rules

            if rule.get(
                "priority",
                0,
            ) >= minimum

        ]

    def filter_by_chapter(
        self,
        chapter: str,
    ) -> list[dict]:

        return self.get_rules_by_chapter(
            chapter
        )

    def filter_by_template(
        self,
        template_id: str,
    ) -> list[dict]:

        return self.get_rules_by_template(
            template_id
        )

    def filter_by_tag(
        self,
        tag: str,
    ) -> list[dict]:

        return self.get_rules_by_tag(
            tag
        )

    # =====================================================
    # Context
    # =====================================================

    def build_context(
        self,
        chart: dict[str, Any],
        variables: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> MatchContext:
        """
        Khởi tạo MatchContext.
        """

        return MatchContext(

            chart=chart,

            variables=variables or {},

            metadata=metadata or {},

        )

    # =====================================================
    # Cache
    # =====================================================

    @property
    def cache(self) -> MatcherCache:

        return self._cache

    def clear_cache(self) -> None:

        self._cache.clear()

    def has_cache(
        self,
        key: str,
    ) -> bool:

        return self._cache.has(key)

    def get_cache(
        self,
        key: str,
    ):

        return self._cache.get(key)

    def put_cache(
        self,
        key: str,
        value: Any,
    ) -> None:

        self._cache.put(
            key,
            value,
        )

    # =====================================================
    # Helper
    # =====================================================

    def make_cache_key(
        self,
        context: MatchContext,
    ) -> str:
        """
        Sinh Cache Key.

        Có thể override ở phiên bản sau.
        """

        birth = context.chart.get(
            "birth_id",
            "",
        )

        version = self.VERSION

        return f"{version}:{birth}"

    def reset(self) -> None:
        """
        Reset Rule Matcher.
        """

        self.clear()

        self.clear_cache()

    # =====================================================
    # Match API
    # =====================================================

    def match(
        self,
        chart: dict[str, Any],
        use_cache: bool = True,
    ) -> list[MatchResult]:
        """
        Match toàn bộ Rule.

        Hoàn thiện ở Part 2.
        """

        raise NotImplementedError(
            "RuleMatcher.match() sẽ được triển khai ở Part 2."
        )

    def match_context(
        self,
        context: MatchContext,
        use_cache: bool = True,
    ) -> list[MatchResult]:
        """
        Match từ MatchContext.

        Hoàn thiện ở Part 2.
        """

        raise NotImplementedError(
            "RuleMatcher.match_context() sẽ được triển khai ở Part 2."
        )

    def match_one(
        self,
        rule: dict[str, Any],
        context: MatchContext,
    ) -> MatchResult:
        """
        Match một Rule.

        Hoàn thiện ở Part 2.
        """

        raise NotImplementedError(
            "RuleMatcher.match_one() sẽ được triển khai ở Part 2."
        )
          # =====================================================
    # Internal Validation
    # =====================================================

    REQUIRED_FIELDS = (
        "rule_id",
        "priority",
        "condition",
        "template_id",
    )

    def validate_rule(
        self,
        rule: dict[str, Any],
    ) -> bool:
        """
        Kiểm tra Rule có đủ dữ liệu tối thiểu.
        """

        if not isinstance(rule, dict):
            return False

        for field in self.REQUIRED_FIELDS:

            if field not in rule:
                return False

        return True

    def validate_rules(
        self,
        rules: Iterable[dict[str, Any]],
    ) -> bool:

        for rule in rules:

            if not self.validate_rule(rule):

                return False

        return True

    # =====================================================
    # Iterators
    # =====================================================

    def iter_rules(self):
        """
        Iterator toàn bộ Rule.
        """

        yield from self._rules

    def iter_enabled_rules(self):
        """
        Iterator Rule đang bật.
        """

        for rule in self._rules:

            if rule.get("enabled", True):

                yield rule

    def iter_chapter(
        self,
        chapter: str,
    ):

        yield from self._chapter_index.get(
            chapter,
            [],
        )

    def iter_tag(
        self,
        tag: str,
    ):

        yield from self._tag_index.get(
            tag,
            [],
        )

    # =====================================================
    # Batch
    # =====================================================

    def chunk(
        self,
        size: int,
    ):
        """
        Chia Rule thành từng Batch.
        """

        if size <= 0:

            raise ValueError(
                "Batch size phải lớn hơn 0."
            )

        for index in range(
            0,
            len(self._rules),
            size,
        ):

            yield self._rules[
                index:index + size
            ]

    # =====================================================
    # Debug
    # =====================================================

    def dump_rules(self):

        return list(self._rules)

    def dump_indexes(self):

        return {

            "rule_index":
                self._rule_index,

            "chapter_index":
                self._chapter_index,

            "tag_index":
                self._tag_index,

            "template_index":
                self._template_index,

        }

    def dump_statistics(self):

        return self.statistics

    # =====================================================
    # Export
    # =====================================================

    def export(self):

        return {

            "version": self.VERSION,

            "statistics":
                self.statistics,

            "rules":
                self._rules,

        }

    # =====================================================
    # Hooks
    # =====================================================

    def before_match(
        self,
        context: MatchContext,
    ) -> None:
        """
        Hook trước khi Match.

        Có thể Override.
        """

        return None

    def after_match(
        self,
        context: MatchContext,
        results: list[MatchResult],
    ) -> None:
        """
        Hook sau khi Match.

        Có thể Override.
        """

        return None

    def before_rule(
        self,
        rule: dict[str, Any],
        context: MatchContext,
    ) -> None:

        return None

    def after_rule(
        self,
        rule: dict[str, Any],
        result: MatchResult,
    ) -> None:

        return None

    # =====================================================
    # Magic Methods
    # =====================================================

    def __len__(self):

        return len(self._rules)

    def __iter__(self):

        return iter(self._rules)

    def __contains__(
        self,
        rule_id: str,
    ):

        return rule_id in self._rule_index

    def __getitem__(
        self,
        rule_id: str,
    ):

        return self._rule_index[rule_id]

    def __repr__(self):

        return (
            f"<RuleMatcher "
            f"rules={len(self._rules)} "
            f"chapters={len(self._chapter_index)} "
            f"templates={len(self._template_index)}>"
        )
          # =====================================================
    # Index Management
    # =====================================================

    def rebuild_indexes(self) -> None:
        """
        Xây dựng lại toàn bộ Index.
        """

        self._rule_index.clear()
        self._chapter_index.clear()
        self._tag_index.clear()
        self._template_index.clear()

        for rule in self._rules:

            rule_id = rule["rule_id"]

            self._rule_index[rule_id] = rule

            chapter = rule.get("chapter")

            if chapter:
                self._chapter_index[chapter].append(rule)

            template = rule.get("template_id")

            if template:
                self._template_index[
                    template
                ].append(rule)

            for tag in rule.get(
                "tags",
                [],
            ):

                self._tag_index[tag].append(rule)

        self._update_statistics()

    # =====================================================
    # Optimizer
    # =====================================================

    def optimize(self) -> None:
        """
        Chuẩn hóa dữ liệu Rule.
        """

        self.rebuild_indexes()

    def sort_by_priority(
        self,
        reverse: bool = True,
    ) -> None:
        """
        Sắp xếp Rule theo Priority.
        """

        self._rules.sort(

            key=lambda rule: rule.get(
                "priority",
                0,
            ),

            reverse=reverse,

        )

        self.rebuild_indexes()

    # =====================================================
    # Cache Warmup
    # =====================================================

    def warmup(
        self,
        contexts: Iterable[MatchContext],
    ) -> None:
        """
        Sinh trước Cache cho các Context.
        """

        for context in contexts:

            key = self.make_cache_key(
                context
            )

            if self._cache.has(key):
                continue

            self._cache.put(
                key,
                [],
            )

    # =====================================================
    # Lifecycle
    # =====================================================

    def initialize(self) -> None:
        """
        Khởi tạo Rule Matcher.
        """

        self.optimize()

    def shutdown(self) -> None:
        """
        Giải phóng tài nguyên.
        """

        self.clear_cache()

    # =====================================================
    # Information
    # =====================================================

    @property
    def version(self) -> str:

        return self.VERSION

    @property
    def rule_count(self) -> int:

        return len(self._rules)

    @property
    def chapter_count(self) -> int:

        return len(self._chapter_index)

    @property
    def tag_count(self) -> int:

        return len(self._tag_index)

    @property
    def template_count(self) -> int:

        return len(self._template_index)

    # =====================================================
    # Health Check
    # =====================================================

    def health(self) -> dict[str, Any]:
        """
        Kiểm tra trạng thái Rule Matcher.
        """

        return {

            "version": self.VERSION,

            "rules": self.rule_count,

            "chapters": self.chapter_count,

            "templates": self.template_count,

            "tags": self.tag_count,

            "cache_enabled": self._cache is not None,

            "ready": (
                self.rule_count > 0
            ),

        }

    # =====================================================
    # End of Part 1
    # =====================================================
