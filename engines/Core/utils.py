"""
===============================================================================
BTE Platform - Core Utilities
===============================================================================

Các hàm tiện ích dùng chung cho toàn bộ Framework.

Author : BTE Platform
Version: 1.0.0
===============================================================================
"""

import csv
import json
import copy
import unicodedata
from pathlib import Path


# =============================================================================
# Safe Convert
# =============================================================================

def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_str(value, default=""):
    if value is None:
        return default
    return str(value)


# =============================================================================
# Text
# =============================================================================

def normalize_text(text: str) -> str:
    if text is None:
        return ""

    return " ".join(str(text).strip().split())


def remove_accents(text: str) -> str:

    text = unicodedata.normalize("NFD", text)

    return "".join(
        c for c in text
        if unicodedata.category(c) != "Mn"
    )


def slugify(text):

    text = remove_accents(text)

    text = text.lower()

    text = text.replace(" ", "_")

    return text


# =============================================================================
# CSV
# =============================================================================

def load_csv(filepath):

    filepath = Path(filepath)

    with filepath.open(
        encoding="utf-8",
        newline=""
    ) as f:

        return list(csv.DictReader(f))


def save_csv(filepath, rows, fieldnames):

    filepath = Path(filepath)

    with filepath.open(
        "w",
        encoding="utf-8",
        newline=""
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(rows)


# =============================================================================
# JSON
# =============================================================================

def load_json(filepath):

    filepath = Path(filepath)

    with filepath.open(
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_json(filepath, data):

    filepath = Path(filepath)

    with filepath.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


# =============================================================================
# Dict
# =============================================================================

def deep_copy(obj):
    return copy.deepcopy(obj)


def merge_dict(a, b):

    result = deep_copy(a)

    result.update(b)

    return result


# =============================================================================
# List
# =============================================================================

def chunk_list(data, size):

    for i in range(0, len(data), size):

        yield data[i:i + size]


def unique_list(data):

    return list(dict.fromkeys(data))


# =============================================================================
# Score
# =============================================================================

def clamp_score(score):

    score = safe_float(score)

    if score < 0:
        return 0

    if score > 100:
        return 100

    return score


def average_score(scores):

    if not scores:
        return 0

    return sum(scores) / len(scores)


# =============================================================================
# File
# =============================================================================

def ensure_directory(path):

    Path(path).mkdir(
        parents=True,
        exist_ok=True
    )


def file_exists(path):

    return Path(path).exists()


# =============================================================================
# Object
# =============================================================================

def object_to_dict(obj):

    if hasattr(obj, "__dict__"):

        return obj.__dict__

    return obj


# =============================================================================
# Debug
# =============================================================================

def pretty_print(title, value):

    print("=" * 60)

    print(title)

    print("-" * 60)

    print(value)

    print("=" * 60)
