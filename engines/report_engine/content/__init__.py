"""Report Engine Content Analysis Layer (WP7A–WP7E)."""

from __future__ import annotations

import importlib

from .content_engine import ContentEngine
from .models import ContentContext

_analysis = importlib.import_module("engines.report_engine.content.01_analysis")
_paragraph = importlib.import_module("engines.report_engine.content.02_paragraph")
_style = importlib.import_module("engines.report_engine.content.03_style")
_consistency = importlib.import_module("engines.report_engine.content.04_consistency")
_output = importlib.import_module("engines.report_engine.content.05_output")

ContextAnalyzer = _analysis.ContextAnalyzer
ImportanceRanker = _analysis.ImportanceRanker
KeywordExtractor = _analysis.KeywordExtractor
SectionOptimizer = _analysis.SectionOptimizer

ParagraphBuilder = _paragraph.ParagraphBuilder
ParagraphContext = _paragraph.ParagraphContext
Paragraph = _paragraph.Paragraph
SentenceUnit = _paragraph.SentenceUnit
Transition = _paragraph.Transition
SentenceMerger = _paragraph.SentenceMerger
ParagraphSplitter = _paragraph.ParagraphSplitter
TransitionSelector = _paragraph.TransitionSelector

StyleBuilder = _style.StyleBuilder
StyledParagraphContext = _style.StyledParagraphContext
StyledParagraph = _style.StyledParagraph
StyledSentence = _style.StyledSentence
RedundancyReducer = _style.RedundancyReducer
SynonymRewriter = _style.SynonymRewriter
EmphasisController = _style.EmphasisController
ToneController = _style.ToneController

ConsistencyBuilder = _consistency.ConsistencyBuilder
ConsistentParagraphContext = _consistency.ConsistentParagraphContext
DuplicateChecker = _consistency.DuplicateChecker
ContradictionChecker = _consistency.ContradictionChecker
CoherenceChecker = _consistency.CoherenceChecker
PolarityChecker = _consistency.PolarityChecker

OutputBuilder = _output.OutputBuilder
ContentOutput = _output.ContentOutput
HtmlOptimizer = _output.HtmlOptimizer
MarkdownOptimizer = _output.MarkdownOptimizer
PdfOptimizer = _output.PdfOptimizer
ApiSerializer = _output.ApiSerializer

__all__ = [
    "ContentContext",
    "ContentEngine",
    "ContextAnalyzer",
    "ImportanceRanker",
    "KeywordExtractor",
    "SectionOptimizer",
    "Paragraph",
    "ParagraphBuilder",
    "ParagraphContext",
    "ParagraphSplitter",
    "SentenceMerger",
    "SentenceUnit",
    "Transition",
    "TransitionSelector",
    "StyleBuilder",
    "StyledParagraph",
    "StyledParagraphContext",
    "StyledSentence",
    "RedundancyReducer",
    "SynonymRewriter",
    "EmphasisController",
    "ToneController",
    "ConsistencyBuilder",
    "ConsistentParagraphContext",
    "DuplicateChecker",
    "ContradictionChecker",
    "CoherenceChecker",
    "PolarityChecker",
    "OutputBuilder",
    "ContentOutput",
    "HtmlOptimizer",
    "MarkdownOptimizer",
    "PdfOptimizer",
    "ApiSerializer",
]
