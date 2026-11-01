"""Validated authoring contracts for the members' knowledge library."""
from typing import Literal
from uuid import uuid4
from pydantic import BaseModel, ConfigDict, Field


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class CategoryInput(Input):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)
    position: int = Field(default=0, ge=0, le=9999)


class CategoryEdit(CategoryInput):
    expected_revision: int = Field(ge=1)


class GroupInput(CategoryInput):
    category_id: str = Field(min_length=1, max_length=100)


class GroupEdit(GroupInput):
    expected_revision: int = Field(ge=1)


class ArticleInput(Input):
    group_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(default="", max_length=600)
    body: str = Field(min_length=1, max_length=100000)
    status: Literal["draft", "published"] = "draft"
    position: int = Field(default=0, ge=0, le=9999)
    client_key: str = Field(default_factory=lambda: uuid4().hex, min_length=16, max_length=80)


class ArticleEdit(Input):
    group_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(default="", max_length=600)
    body: str = Field(min_length=1, max_length=100000)
    status: Literal["draft", "published"]
    position: int = Field(ge=0, le=9999)
    expected_revision: int = Field(ge=1)
