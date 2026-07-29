"""
Model Factory

Chuyển Dict thành Python Model.
"""

from __future__ import annotations


class ModelFactory:

    @staticmethod
    def create(model_cls, data: dict):

        return model_cls(**data)
