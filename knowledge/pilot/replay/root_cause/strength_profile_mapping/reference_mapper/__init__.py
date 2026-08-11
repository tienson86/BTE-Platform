"""PILOT-1J read-only Strength Profile reference mapper.

REFERENCE_ONLY = True
PRODUCTION_READY = False
TAXONOMY_IMPLEMENTED = False
CALIBRATION_IMPLEMENTATION = False

Does not modify Strength Engine behavior. Does not calculate Strength.
"""

from .mapper import ReferenceProfileMapper, map_all_cases

REFERENCE_ONLY = True
PRODUCTION_READY = False
TAXONOMY_IMPLEMENTED = False
CALIBRATION_IMPLEMENTATION = False

__all__ = [
    "REFERENCE_ONLY",
    "PRODUCTION_READY",
    "TAXONOMY_IMPLEMENTED",
    "CALIBRATION_IMPLEMENTATION",
    "ReferenceProfileMapper",
    "map_all_cases",
]
