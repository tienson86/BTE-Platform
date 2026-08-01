# Pack 01 Baseline Build Report

- Pack: `PACK_01`
- Version: `1.0.0`
- Timestamp: `2026-08-01T00:00:00Z`

## Artifacts

- `baseline_manifest.json`
- `compiler_snapshot.json`
- `compiler_validation_report.json`
- `dependency_snapshot.json`
- `governance_metadata.json`
- `graph_validation_report.json`
- `knowledge_graph.dot`
- `knowledge_graph.graphml`
- `knowledge_graph.json`
- `knowledge_graph.mmd`
- `known_issues.json`
- `ontology_snapshot.json`
- `ontology_validation_report.json`
- `registry_snapshot.json`
- `registry_validation_report.json`
- `statistics.json`
- `validation_snapshot.json`

## Validation Summary

| Domain | Status |
|---|---|
| compiler | PASS |
| graph | PASS |
| ontology | PASS |
| registry | PASS |

## Statistics

```json
{
  "artifact": "statistics",
  "compiler_stages": 8,
  "compiler_statistics": {
    "file_count": 9,
    "pipeline_id": "PIPE-KNO-001",
    "stage_count": 8
  },
  "context_count": 2,
  "coverage": {
    "rules_total": 112,
    "rules_with_severity": 112,
    "validator_coverage_ratio": 1.0,
    "validators_total": 7,
    "validators_with_rules": 7
  },
  "dependency_academic_edges": 33,
  "dependency_implementation_edges": 14,
  "graph_edges": 105,
  "graph_nodes": 66,
  "graph_statistics": {
    "concept_nodes": 15,
    "context_count": 2,
    "edge_count": 105,
    "mapping_count": 3,
    "node_count": 66,
    "ontology_nodes": 50,
    "relationship_types": [
      "BELONGS_TO",
      "CONTEXTUALIZES",
      "DEPENDS_ON",
      "DESCRIBES",
      "MAPS",
      "RELATED_TO",
      "RELATES",
      "SUBCLASS_OF"
    ]
  },
  "knowledge_records": 15,
  "ontology_classes": 50,
  "ontology_count": 50,
  "registry_count": 8,
  "relationship_count": 101,
  "rule_count": 112,
  "validation_stages": 9,
  "validation_statistics": {
    "coverage": {
      "rules_total": 112,
      "rules_with_severity": 112,
      "validator_coverage_ratio": 1.0,
      "validators_total": 7,
      "validators_with_rules": 7
    },
    "rule_count": 112,
    "stage_count": 9,
    "validator_count": 7
  }
}
```
