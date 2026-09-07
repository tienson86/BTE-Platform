"""Score projection status for TV1-B03.

04_SCORE_ENGINE defines domain weights but does not specify the
state-to-numeric transformation constants required for a faithful
projection. TV1-B03 does not invent those constants.
"""

from __future__ import annotations

from consulting.marriage.policy.versions import SCORE_MODEL_VERSION

SCORE_PROJECTION_STATUS = SCORE_MODEL_VERSION
