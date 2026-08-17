"""Machine-readable diagnostic codes for Interpretation Foundation."""

from __future__ import annotations

# Domain truth missing
STRENGTH_TRUTH_MISSING = "strength_truth_missing"
PATTERN_TRUTH_MISSING = "pattern_truth_missing"
USEFUL_GOD_TRUTH_MISSING = "useful_god_truth_missing"
USEFUL_GOD_CANDIDATES_MISSING = "useful_god_candidates_missing"
USEFUL_GOD_EVIDENCE_MISSING = "useful_god_evidence_missing"
TEMPERATURE_TRUTH_MISSING = "temperature_truth_missing"
TEN_GOD_POSITIONS_MISSING = "ten_god_positions_missing"
SHENSHA_EVIDENCE_UNAVAILABLE = "shensha_evidence_unavailable"
LUCK_CYCLES_MISSING = "luck_cycles_missing"
FIVE_ELEMENTS_TRUTH_MISSING = "five_elements_truth_missing"
INTERACTION_TRUTH_MISSING = "interaction_truth_missing"
CURRENT_PERIOD_MISSING = "current_period_missing"
NEXT_PERIOD_MISSING = "next_period_missing"
USEFUL_GOD_MISSING = "useful_god_missing"
HY_MISSING = "hy_missing"
KY_MISSING = "ky_missing"
PATTERN_MISSING = "pattern_missing"
STRENGTH_MISSING = "strength_missing"
PERIOD_STEM_UNPUBLISHED = "period_stem_unpublished"
PERIOD_BRANCH_UNPUBLISHED = "period_branch_unpublished"
EMPTY_IDENTITY_OVERLAP = "empty_identity_overlap"

# Score-as-truth violations
SCORE_USED_AS_STRENGTH_TRUTH = "score_used_as_strength_truth"
SCORE_USED_AS_WUXING_TRUTH = "score_used_as_wuxing_truth"
SCORE_USED_AS_TEN_GOD_TRUTH = "score_used_as_ten_god_truth"
SCORE_USED_AS_USEFUL_GOD_TRUTH = "score_used_as_useful_god_truth"
SCORE_USED_AS_LUCK_TRUTH = "score_used_as_luck_truth"

# Wrong-field contamination
TEMPERATURE_CONTAMINATED_BY_PATTERN = "temperature_contaminated_by_pattern"
TEMPERATURE_CONTAMINATED_BY_TRUONG_SINH = "temperature_contaminated_by_truong_sinh"

# Generic
ANALYTICAL_DISTRIBUTION_UNAVAILABLE = "analytical_distribution_unavailable"
USEFUL_GOD_NOT_AVAILABLE = "useful_god_not_available"
SILENT_FALLBACK_DETECTED = "silent_fallback_detected"
