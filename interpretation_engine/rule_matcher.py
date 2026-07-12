
class RuleMatcher:


    def match(
        self,
        rule,
        chart_data
    ):


        condition_type = rule.get(
            "condition_type"
        )


        key = rule.get(
            "condition_key"
        )


        value = rule.get(
            "condition_value"
        )


        if condition_type=="equal":


            return (
                chart_data.get(key)
                ==
                value
            )


        elif condition_type=="contains":


            data = chart_data.get(key,[])

            return value in data



        elif condition_type=="exist":


            return key in chart_data



        return False



    def match_rules(
        self,
        rules,
        chart_data
    ):

        matched=[]


        for rule in rules:

            if self.match(
                rule,
                chart_data
            ):

                matched.append(rule)


        return matched
