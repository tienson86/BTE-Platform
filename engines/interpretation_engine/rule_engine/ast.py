"""
ast.py
======

Định nghĩa Abstract Syntax Tree (AST)
cho Rule Engine.

Tokenizer
    ↓
Parser
    ↓
AST
    ↓
Matcher
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ==========================================================
# Operator
# ==========================================================

class Operator(str, Enum):

    EQ = "=="
    NE = "!="

    GT = ">"
    LT = "<"

    GTE = ">="
    LTE = "<="

    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"

    EXISTS = "exists"
    NOT_EXISTS = "not_exists"

    IN = "in"
    NOT_IN = "not_in"


# ==========================================================
# Logic
# ==========================================================

class Logic(str, Enum):

    AND = "AND"

    OR = "OR"

    NOT = "NOT"


# ==========================================================
# Base Node
# ==========================================================

class ASTNode:
    """Base class."""


# ==========================================================
# Condition
# ==========================================================

@dataclass(slots=True)
class ConditionNode(ASTNode):

    field: str

    operator: Operator

    value: Optional[str] = None


# ==========================================================
# Unary
# ==========================================================

@dataclass(slots=True)
class UnaryNode(ASTNode):

    operator: Logic

    operand: ASTNode


# ==========================================================
# Binary
# ==========================================================

@dataclass(slots=True)
class BinaryNode(ASTNode):

    left: ASTNode

    operator: Logic

    right: ASTNode


# ==========================================================
# Function
# ==========================================================

@dataclass(slots=True)
class FunctionNode(ASTNode):

    name: str

    argument: Optional[str] = None
