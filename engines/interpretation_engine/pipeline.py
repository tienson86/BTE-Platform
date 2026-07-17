"""
Interpretation Pipeline

Điều phối toàn bộ quy trình sinh báo cáo.
"""

from __future__ import annotations


class InterpretationPipeline:

    def __init__(
        self,
        schema_loader,
        validator,
        registry,
        plugin_manager,
        engine_validator
    ):

        self.schema_loader = schema_loader
        self.validator = validator
        self.registry = registry
        self.plugin_manager = plugin_manager
        self.engine_validator = engine_validator

    def initialize(self):

        """
        Khởi tạo Engine.
        """

        return True

    def validate(self):

        """
        Kiểm tra Database.
        """

        return self.engine_validator

    def execute(
        self,
        chart
    ):

        """
        Điều phối toàn bộ quá trình diễn giải.

        1. Match Rule

        2. Chọn Template

        3. Sinh Sentence

        4. Ghép Paragraph

        5. Ghép Chapter

        6. Trả Report
        """

        return chart
