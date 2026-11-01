"""Strict input contracts for private support and moderated member discussions."""
from uuid import uuid4
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class Input(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

class MessageInput(Input):
    message: str = Field(min_length=1, max_length=5000)
    client_key: str = Field(default_factory=lambda: uuid4().hex, min_length=16, max_length=80)

class ThreadInput(MessageInput):
    subject: str = Field(min_length=1, max_length=180)
    recipient_user_id: str | None = Field(default=None, max_length=100)

class ReadInput(Input):
    last_message_id: int = Field(ge=0)

class TopicInput(Input):
    title: str = Field(min_length=1, max_length=180)
    body: str = Field(min_length=1, max_length=20000)
    client_key: str = Field(default_factory=lambda: uuid4().hex, min_length=16, max_length=80)
    category_id: str | None = Field(default=None, min_length=1, max_length=100)

class RevisionInput(Input):
    expected_revision: int = Field(ge=1)

class TopicEdit(RevisionInput):
    title: str = Field(min_length=1, max_length=180)
    body: str = Field(min_length=1, max_length=20000)

class ModerateInput(RevisionInput):
    decision: Literal["approve", "reject"]
    note: str = Field(default="", max_length=1000)

class CommentInput(Input):
    body: str = Field(min_length=1, max_length=5000)
    client_key: str = Field(default_factory=lambda: uuid4().hex, min_length=16, max_length=80)

class CommentEdit(RevisionInput):
    body: str = Field(min_length=1, max_length=5000)
