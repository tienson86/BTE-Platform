"""
BTE Platform
Interpretation Engine Constants
"""

from __future__ import annotations

# ==========================================================
# Engine
# ==========================================================

ENGINE_NAME = "Interpretation Engine"

ENGINE_VERSION = "1.0.0"

# ==========================================================
# Operations
# ==========================================================

OP_INTERPRET = "interpret"

OP_RENDER = "render"

OP_EXPORT = "export"

OP_FULL_REPORT = "full_report"

# ==========================================================
# Render Formats
# ==========================================================

FORMAT_MARKDOWN = "markdown"

FORMAT_HTML = "html"

FORMAT_PDF = "pdf"

FORMAT_JSON = "json"

FORMAT_TEXT = "text"

SUPPORTED_FORMATS = (
    FORMAT_MARKDOWN,
    FORMAT_HTML,
    FORMAT_PDF,
    FORMAT_JSON,
    FORMAT_TEXT,
)

# ==========================================================
# Chapters
# ==========================================================

CHAPTER_OVERVIEW = "Tổng quan"

CHAPTER_PERSONALITY = "Tính cách"

CHAPTER_CAREER = "Sự nghiệp"

CHAPTER_WEALTH = "Tài vận"

CHAPTER_RELATIONSHIP = "Hôn nhân"

CHAPTER_HEALTH = "Sức khỏe"

CHAPTER_LUCK = "Đại vận"

CHAPTER_SUMMARY = "Tổng kết"

DEFAULT_CHAPTERS = (
    CHAPTER_OVERVIEW,
    CHAPTER_PERSONALITY,
    CHAPTER_CAREER,
    CHAPTER_WEALTH,
    CHAPTER_RELATIONSHIP,
    CHAPTER_HEALTH,
    CHAPTER_LUCK,
    CHAPTER_SUMMARY,
)

# ==========================================================
# Template
# ==========================================================

DEFAULT_LANGUAGE = "vi"

DEFAULT_TEMPLATE = "default"

DEFAULT_STYLE = "professional"

# ==========================================================
# Cache
# ==========================================================

CACHE_PREFIX = "interpretation"

CACHE_TIMEOUT = 3600
