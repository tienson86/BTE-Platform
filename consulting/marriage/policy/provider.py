"""Marriage Policy provider for marriage.policy.v1."""

from __future__ import annotations

from consulting.marriage.decision.context import MarriageDecisionContext
from consulting.marriage.exceptions import MarriageDecisionError
from consulting.marriage.policy.contract import MarriagePolicyDescriptor, MarriagePolicyProvider
from consulting.marriage.policy.v1 import MarriagePolicyV1, load_marriage_policy_v1
from consulting.marriage.policy.versions import POLICY_ID, POLICY_VERSION, policy_version_token


class MarriagePolicyV1Provider(MarriagePolicyProvider):
    """Loads marriage.policy.v1. Does not evaluate evidence."""

    def __init__(self, policy: MarriagePolicyV1 | None = None) -> None:
        self._policy = policy or load_marriage_policy_v1()

    def descriptor(self) -> MarriagePolicyDescriptor:
        """Return the bound policy identity."""
        return MarriagePolicyDescriptor(policy_id=POLICY_ID, version=POLICY_VERSION)

    def provide(self, context: MarriageDecisionContext) -> MarriagePolicyDescriptor:
        """Confirm the context is bound to this policy version."""
        expected = policy_version_token()
        bound = context.versions.decision_profile_version
        if bound not in (expected, POLICY_VERSION, POLICY_ID):
            raise MarriageDecisionError(f"policy_version_mismatch:{bound}")
        return self.descriptor()

    def policy(self) -> MarriagePolicyV1:
        """Return the executable policy object."""
        return self._policy
