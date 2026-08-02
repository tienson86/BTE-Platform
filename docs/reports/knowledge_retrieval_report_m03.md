# Knowledge Retrieval Report — Epic 03 Milestone 03

## Summary

- Samples validated: **100**
- Total accepted hits: **580**
- Average hits / sample: **5.80**
- Total rejected candidates (sum): **2720**
- Corpus records: **33**
- Distractor leakage: **0** (KNW-CR-DIST / KNW-GL-EMPTY never accepted)

## Ranking policy

- keyword weight 0.45
- condition weight 0.35
- priority weight 0.10
- confidence weight 0.10
- non-empty conditions fail closed
- empty keyword+condition rows always rejected

## Sample digest (first 10)

```json
[
  {
    "sample_id": 0,
    "accepted": [
      "KNW-UG-001",
      "KNW-TG-001",
      "KNW-ST-001",
      "KNW-SS-001",
      "KNW-FE-001"
    ],
    "accepted_count": 5,
    "rejected_count": 28,
    "top_relevance": 0.907,
    "signals": [
      "cái",
      "hoa",
      "hoa cái",
      "kiên",
      "mộc",
      "neutral",
      "ok",
      "pattern_0",
      "present",
      "spring",
      "strong",
      "tỷ"
    ]
  },
  {
    "sample_id": 1,
    "accepted": [
      "KNW-TG-004",
      "KNW-UG-003",
      "KNW-TG-002",
      "KNW-ST-002",
      "KNW-SS-002",
      "KNW-FE-002"
    ],
    "accepted_count": 6,
    "rejected_count": 27,
    "top_relevance": 0.909,
    "signals": [
      "balanced",
      "hỏa",
      "kiếp",
      "kiếp tài",
      "neutral",
      "ok",
      "pattern_1",
      "present",
      "quan",
      "spring",
      "thiên",
      "thiên át"
    ]
  },
  {
    "sample_id": 2,
    "accepted": [
      "KNW-TG-007",
      "KNW-UG-005",
      "KNW-TG-003",
      "KNW-ST-003",
      "KNW-SS-003",
      "KNW-FE-003"
    ],
    "accepted_count": 6,
    "rejected_count": 27,
    "top_relevance": 0.912,
    "signals": [
      "chính",
      "chính quan",
      "neutral",
      "ok",
      "pattern_2",
      "present",
      "quan",
      "spring",
      "thần",
      "thổ",
      "thủy",
      "thực"
    ]
  },
  {
    "sample_id": 3,
    "accepted": [
      "KNW-TG-010",
      "KNW-TG-004",
      "KNW-UG-002",
      "KNW-ST-001",
      "KNW-SS-004",
      "KNW-FE-004"
    ],
    "accepted_count": 6,
    "rejected_count": 27,
    "top_relevance": 0.915,
    "signals": [
      "hỏa",
      "kim",
      "neutral",
      "ok",
      "pattern_3",
      "present",
      "quan",
      "quốc",
      "quốc ấn",
      "spring",
      "strong",
      "thiên"
    ]
  },
  {
    "sample_id": 4,
    "accepted": [
      "KNW-TG-005",
      "KNW-UG-004",
      "KNW-TG-003",
      "KNW-ST-002",
      "KNW-SS-005",
      "KNW-FE-005"
    ],
    "accepted_count": 6,
    "rejected_count": 27,
    "top_relevance": 0.91,
    "signals": [
      "balanced",
      "chính",
      "chính tài",
      "dịch",
      "dịch mã",
      "kim",
      "mã",
      "neutral",
      "ok",
      "pattern_4",
      "present",
      "spring"
    ]
  },
  {
    "sample_id": 5,
    "accepted": [
      "KNW-TG-006",
      "KNW-UG-001",
      "KNW-ST-003",
      "KNW-SS-006",
      "KNW-FE-001"
    ],
    "accepted_count": 5,
    "rejected_count": 28,
    "top_relevance": 0.911,
    "signals": [
      "hoa",
      "mộc",
      "neutral",
      "ok",
      "pattern_5",
      "present",
      "spring",
      "thiên",
      "thiên tài",
      "tài",
      "weak",
      "đào"
    ]
  },
  {
    "sample_id": 6,
    "accepted": [
      "KNW-TG-009",
      "KNW-TG-007",
      "KNW-UG-003",
      "KNW-ST-001",
      "KNW-SS-007",
      "KNW-FE-002"
    ],
    "accepted_count": 6,
    "rejected_count": 27,
    "top_relevance": 0.914,
    "signals": [
      "chính",
      "chính quan",
      "chính ấn",
      "cô",
      "cô thần",
      "hỏa",
      "neutral",
      "ok",
      "pattern_6",
      "present",
      "quan",
      "spring"
    ]
  },
  {
    "sample_id": 7,
    "accepted": [
      "KNW-TG-008",
      "KNW-UG-005",
      "KNW-TG-002",
      "KNW-ST-002",
      "KNW-SS-008",
      "KNW-FE-003"
    ],
    "accepted_count": 6,
    "rejected_count": 27,
    "top_relevance": 0.913,
    "signals": [
      "balanced",
      "kiếp",
      "kiếp tài",
      "neutral",
      "ok",
      "pattern_0",
      "present",
      "quả",
      "quả tú",
      "spring",
      "sát",
      "thất"
    ]
  },
  {
    "sample_id": 8,
    "accepted": [
      "KNW-TG-009",
      "KNW-TG-005",
      "KNW-UG-002",
      "KNW-ST-003",
      "KNW-SS-001",
      "KNW-FE-004"
    ],
    "accepted_count": 6,
    "rejected_count": 27,
    "top_relevance": 0.914,
    "signals": [
      "chính",
      "chính tài",
      "chính ấn",
      "cái",
      "hoa",
      "hoa cái",
      "hỏa",
      "kim",
      "neutral",
      "ok",
      "pattern_1",
      "present"
    ]
  },
  {
    "sample_id": 9,
    "accepted": [
      "KNW-TG-010",
      "KNW-TG-008",
      "KNW-UG-004",
      "KNW-ST-001",
      "KNW-SS-002",
      "KNW-FE-005"
    ],
    "accepted_count": 6,
    "rejected_count": 27,
    "top_relevance": 0.915,
    "signals": [
      "kim",
      "neutral",
      "ok",
      "pattern_2",
      "present",
      "spring",
      "strong",
      "sát",
      "thiên",
      "thiên át",
      "thiên ấn",
      "thất"
    ]
  }
]
```

## Compatibility

- Input: RuleContext only
- Output: KnowledgeResult + metadata.trace
- No calculation engine changes
