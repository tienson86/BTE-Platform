"""Pack boundary contract for Pack 03."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PackBoundaryContract:
    """Declare Pack 03 dependency boundaries."""

    pack_id: str = "PACK_03"
    depends_on_packs: tuple[str, ...] = ("PACK_02",)
    read_only_packs: tuple[str, ...] = ("PACK_01",)
    sole_runtime_input: str = "PACK_02.FinalAnalysisResult"
    may_mutate_pack01: bool = False
    may_bypass_pack02_final_result: bool = False
