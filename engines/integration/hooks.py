"""
Pipeline Hooks.
"""

from __future__ import annotations


class PipelineHooks:

    def before_stage(

        self,

        stage,

        context,

    ):

        pass

    def after_stage(

        self,

        stage,

        result,

    ):

        pass

    def on_success(

        self,

        result,

    ):

        pass

    def on_error(

        self,

        stage,

        exception,

    ):

        pass
