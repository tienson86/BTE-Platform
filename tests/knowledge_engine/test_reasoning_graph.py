"""Unit tests for Reasoning Graph Engine (Epic 03 Milestone 04)."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.knowledge_engine import (
    KNOWLEDGE_FILES,
    REQUIRED_COLUMNS,
    KnowledgeHit,
    KnowledgeLoader,
    KnowledgeRecord,
    KnowledgeRepository,
    KnowledgeResult,
    KnowledgeRetriever,
    ReasoningGraphEngine,
)

SCHEMA = ",".join(REQUIRED_COLUMNS)


def _officer_context() -> dict:
    return {
        "ten_gods": {"items": ["chính quan", "thực thần"], "status": "ok"},
        "pattern": {"main_pattern": "chinh_quan", "name": "chính quan"},
        "shensha": {"stars": ["hoa cái"], "status": "ok"},
        "useful_god": {"element": "kim", "status": "ok"},
        "strength": {"level": "strong"},
    }


def _write_corpus(root: Path, rows: list[str]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    for name in KNOWLEDGE_FILES:
        lines = [SCHEMA]
        if name == "03_ten_gods.csv":
            lines.extend(rows)
        (root / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return root


class TestReasoningGraphEngine:
    def test_officer_chain_evidence_to_conclusion(self) -> None:
        engine = ReasoningGraphEngine()
        graph = engine.build(_officer_context())

        labels = {node.label for node in graph.nodes}
        assert "Strong Officer" in labels
        assert "Career Leadership" in labels
        assert "Management Potential" in labels
        assert "Suitable Career" in labels
        assert "Suitable Career" in graph.conclusions

        # Find evidence → conclusion path labels
        evidence = next(node for node in graph.nodes if node.label == "Strong Officer")
        paths = graph.path_labels(evidence.id)
        assert any(
            path[:4]
            == [
                "Strong Officer",
                "Career Leadership",
                "Management Potential",
                "Suitable Career",
            ]
            for path in paths
        )

    def test_edges_store_required_fields(self) -> None:
        graph = ReasoningGraphEngine().build(_officer_context())
        assert graph.edges
        for edge in graph.edges:
            assert edge.reason
            assert isinstance(edge.priority, int)
            assert 0.0 <= edge.confidence <= 1.0
            assert edge.source
            assert edge.source_id
            assert edge.target_id

    def test_node_kinds_follow_pipeline(self) -> None:
        graph = ReasoningGraphEngine().build(
            {"ten_gods": {"items": ["chính quan"]}}
        )
        kinds_by_chain = [
            node.kind
            for node in graph.nodes
            if node.payload.get("template_id") == "career_officer_strong"
            or node.id.startswith("ev:career_officer_strong")
        ]
        assert "evidence" in kinds_by_chain
        assert "intermediate_rule" in kinds_by_chain
        assert "reasoning" in kinds_by_chain
        assert "conclusion" in kinds_by_chain

    def test_metadata_trace(self) -> None:
        graph = ReasoningGraphEngine().build(_officer_context())
        assert "trace" in graph.metadata
        assert graph.trace
        accepted = [row for row in graph.trace if row.get("accepted")]
        rejected = [row for row in graph.trace if not row.get("accepted")]
        assert accepted
        assert any(row["template_id"] == "career_officer_strong" for row in accepted)
        assert rejected  # unused templates traced as rejected
        assert graph.metadata["fired_count"] >= 1
        assert graph.metadata["edge_count"] == len(graph.edges)

    def test_no_fire_without_evidence(self) -> None:
        graph = ReasoningGraphEngine().build({"ten_gods": {"items": []}, "strength": {}})
        assert graph.metadata["fired_count"] == 0
        assert graph.nodes == []
        assert graph.edges == []
        assert graph.conclusions == []

    def test_wealth_and_weak_strength_templates(self) -> None:
        graph = ReasoningGraphEngine().build(
            {
                "ten_gods": {"items": ["chính tài"]},
                "strength": {"level": "weak"},
            }
        )
        labels = {node.label for node in graph.nodes}
        assert "Direct Wealth Present" in labels
        assert "Wealth Outlook" in labels
        assert "Day Master Weak" in labels
        assert "Strength Outlook" in graph.conclusions

    def test_knowledge_attachment_edges(self, tmp_path: Path) -> None:
        db = _write_corpus(
            tmp_path / "kb",
            [
                "KNW-TG-001,ten_gods,chính quan;officer,ten_gods.items contains chính quan,"
                "classical,modern officer text,30,0.9,SRC-000001"
            ],
        )
        repo = KnowledgeRepository(KnowledgeLoader(db)).load()
        retriever = KnowledgeRetriever(repo, min_relevance=0.1)
        knowledge = retriever.retrieve({"ten_gods": {"items": ["chính quan"]}})
        engine = ReasoningGraphEngine(retriever=retriever)
        graph = engine.build(
            {"ten_gods": {"items": ["chính quan"]}},
            knowledge_result=knowledge,
        )
        assert graph.metadata["knowledge_attached"] is True
        knowledge_nodes = [node for node in graph.nodes if node.id.startswith("knowledge:")]
        assert knowledge_nodes
        assert any(edge.source.startswith("knowledge:") for edge in graph.edges)

    def test_retrieve_knowledge_flag(self, tmp_path: Path) -> None:
        db = _write_corpus(
            tmp_path / "kb2",
            [
                "KNW-TG-002,ten_gods,chính quan,ten_gods.items contains chính quan,"
                "classical,modern,20,0.9,SRC-000001"
            ],
        )
        retriever = KnowledgeRetriever(
            KnowledgeRepository(KnowledgeLoader(db)).load(), min_relevance=0.1
        )
        graph = ReasoningGraphEngine(retriever).build(
            {"ten_gods": {"items": ["chính quan"]}, "useful_god": {"element": "kim", "status": "ok"}},
            retrieve_knowledge=True,
        )
        assert graph.metadata["fired_count"] >= 1

    def test_to_dict_and_helpers(self) -> None:
        graph = ReasoningGraphEngine().build({"ten_gods": {"items": ["chính quan"]}})
        payload = graph.to_dict()
        assert "nodes" in payload and "edges" in payload and "metadata" in payload
        node_map = graph.node_map()
        evidence = next(node for node in graph.nodes if node.kind == "evidence")
        outgoing = graph.edges_from(evidence.id)
        assert evidence.id in node_map
        assert outgoing
        assert evidence.to_dict()["kind"] == "evidence"
        assert outgoing[0].to_dict()["reason"]

    def test_qi_sha_and_hoa_cai(self) -> None:
        graph = ReasoningGraphEngine().build(
            {
                "ten_gods": {"items": ["thất sát"]},
                "shensha": {"stars": ["hoa cái"]},
            }
        )
        labels = {node.label for node in graph.nodes}
        assert "Seven Killings Present" in labels
        assert "Hoa Cái Present" in labels
        assert "Suitable Career" in graph.conclusions
