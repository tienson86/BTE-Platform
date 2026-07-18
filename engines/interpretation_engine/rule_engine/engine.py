from ..models import RuleResult


class RuleEngine:
    def run_matched(self, context, rules):
        return [RuleResult(rule=rule, matched=True, score=getattr(rule, "priority", 0)) for rule in rules if getattr(rule, "enabled", True)]
