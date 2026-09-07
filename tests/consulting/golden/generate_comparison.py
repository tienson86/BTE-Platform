"""Write TV1-R01 Golden comparison signatures. Testing helper only."""

from __future__ import annotations

import json
from pathlib import Path

from tests.consulting.golden.cases import GOLDEN_CASES, run_golden_case

EXPECTED_DIR = Path(__file__).resolve().parent / "comparison"


def main() -> None:
    """Generate one comparison JSON file per Golden case."""
    EXPECTED_DIR.mkdir(parents=True, exist_ok=True)
    for case in GOLDEN_CASES:
        bundle = run_golden_case(case.case_id)
        path = EXPECTED_DIR / f"{case.case_id}.json"
        path.write_text(
            json.dumps(bundle["signature"]["comparison"], indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        comparison = bundle["signature"]["comparison"]
        print(
            f"{case.case_id} overall={bundle['signature']['overall_state']} "
            f"level={comparison['compatibility_level']} d1={comparison['d1_mutual']} -> {path.name}"
        )


if __name__ == "__main__":
    main()
