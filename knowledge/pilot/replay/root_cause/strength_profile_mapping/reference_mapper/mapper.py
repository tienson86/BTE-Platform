"""Top-level read-only reference mapper orchestration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .profile_mapper import map_profile
from .source_reader import RuntimeBundle, from_calibration_case, from_synthetic_result

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[4]
SYN_RESULTS = REPO / "knowledge" / "pilot" / "replay" / "synthetic_strength" / "results"
CAL_CASES = (
    REPO
    / "knowledge"
    / "pilot"
    / "replay"
    / "root_cause"
    / "strength_taxonomy_v2"
    / "calibration"
    / "cases"
)
CAL_EVIDENCE = (
    REPO
    / "knowledge"
    / "pilot"
    / "replay"
    / "root_cause"
    / "strength_taxonomy_v2"
    / "calibration"
    / "evidence"
)
RESULTS = ROOT / "results"
EXAMPLES = ROOT / "examples"

REFERENCE_META = {
    "reference_only": True,
    "production_ready": False,
    "taxonomy_implemented": False,
    "calibration_implementation": False,
    "mapper_status": "REFERENCE_ONLY",
}


class ReferenceProfileMapper:
    """Read-only mapper from existing runtime evidence to StrengthProfile."""

    def map_bundle(self, bundle: RuntimeBundle) -> dict[str, Any]:
        """Map one normalized runtime bundle to a mapped-profile envelope."""
        profile = map_profile(bundle)
        envelope: dict[str, Any] = {
            **REFERENCE_META,
            "case_id": bundle.case_id,
            "population": bundle.population,
            "source_paths": bundle.source_paths,
            "saturation_source": profile["score_reference"].get("saturation_type"),
            "profile": profile,
            "expert_review_reference": None,
        }
        # Expert metadata stays outside StrengthProfile runtime fields.
        if bundle.expert_external:
            envelope["expert_review_reference"] = {
                "expert_review_1": bundle.expert_external.get("expert_review_1"),
                "expert_review_2": bundle.expert_external.get("expert_review_2"),
                "agreement": bundle.expert_external.get("agreement"),
                "note": "external calibration metadata only; does not overwrite runtime profile",
            }
        return envelope

    def map_synthetic_file(self, path: Path) -> dict[str, Any]:
        doc = json.loads(path.read_text(encoding="utf-8"))
        return self.map_bundle(from_synthetic_result(doc))

    def map_calibration(self, case_id: str) -> dict[str, Any]:
        case = json.loads((CAL_CASES / f"{case_id}.json").read_text(encoding="utf-8"))
        evidence = json.loads((CAL_EVIDENCE / f"{case_id}.json").read_text(encoding="utf-8"))
        return self.map_bundle(from_calibration_case(case, evidence))


def map_all_cases(*, write: bool = True) -> list[dict[str, Any]]:
    """Map CAL-000001/000006 and SYN-STR-000001..000021."""
    mapper = ReferenceProfileMapper()
    RESULTS.mkdir(parents=True, exist_ok=True)
    EXAMPLES.mkdir(parents=True, exist_ok=True)
    outputs: list[dict[str, Any]] = []

    for case_id in ("CAL-000001", "CAL-000006"):
        mapped = mapper.map_calibration(case_id)
        outputs.append(mapped)
        if write:
            _write(RESULTS / f"REAL_{case_id}.json", mapped)

    for n in range(1, 22):
        case_id = f"SYN-STR-{n:06d}"
        mapped = mapper.map_synthetic_file(SYN_RESULTS / f"{case_id}.json")
        outputs.append(mapped)
        if write:
            _write(RESULTS / f"{case_id}.json", mapped)

    if write:
        _write(EXAMPLES / "real_cal_000001_profile.json", outputs[0])
        _write(EXAMPLES / "real_cal_000006_profile.json", outputs[1])
        # synthetic examples by case id
        by_id = {o["case_id"]: o for o in outputs}
        _write(EXAMPLES / "synthetic_000001_profile.json", by_id["SYN-STR-000001"])
        _write(EXAMPLES / "synthetic_000010_profile.json", by_id["SYN-STR-000010"])
        _write(EXAMPLES / "synthetic_000019_profile.json", by_id["SYN-STR-000019"])
    return outputs


def _write(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    outputs = map_all_cases(write=True)
    print(f"mapped={len(outputs)}")


if __name__ == "__main__":
    main()
