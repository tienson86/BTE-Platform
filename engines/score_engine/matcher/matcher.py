class RuleMatcher:

    def match(self, rules, context):

        if rules is None:
            return []

        if hasattr(rules, "iterrows"):
            matched = []

            for _, rule in rules.iterrows():
                if self.evaluate_rule(rule, context):
                    matched.append(rule.to_dict())

            return matched

        if isinstance(rules, list):
            return [
                rule
                for rule in rules
                if self.evaluate_rule(rule, context)
            ]

        return self.evaluate_rule(rules, context)

    def evaluate_rule(self, rule, context):

        condition = str(
            rule.get("condition", "")
        ).strip()

        if condition == "":
            return True

        return self.evaluate(condition, context)

    def evaluate(self, expression, context):

        values = vars(context) if hasattr(context, "__dict__") else context

        try:
            return bool(
                eval(expression, {"__builtins__": {}}, values)
            )
        except (NameError, SyntaxError, TypeError, ValueError):
            return False
