"""
Pipeline Exception Handler.
"""

from __future__ import annotations

import traceback


class ExceptionHandler:

    @staticmethod
    def handle(exception: Exception):

        return {

            "success": False,

            "error": str(exception),

            "traceback": traceback.format_exc(),

        }
