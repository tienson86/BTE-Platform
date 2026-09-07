"""Write TV1-R02 Assessment Golden files. Decision Golden is not rewritten."""

from __future__ import annotations

import json
from pathlib import Path

from tests.consulting.golden.assessment_signature import assessment_signature
from tests.consulting.golden.cases import GOLDEN_CASES, run_golden_case

EXPECTED_DIR = Path(__file__).resolve().parent / "assessment"


def main() -> None:
    """Generate one Assessment JSON file per Golden case."""
    EXPECTED_DIR.mkdir(parents=True, exist_ok=True)
    for case in GOLDEN_CASES:
        bundle = run_golden_case(case.case_id)
        payload = assessment_signature(bundle["decision"])
        path = EXPECTED_DIR / f"{case.case_id}.json"
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{case.case_id} cards={len(payload['cards'])} -> {path.name}")


if __name__ == "__main__":
    main()
