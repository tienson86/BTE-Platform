
class InterpretationBuilder:



    def build(
        self,
        scored_rules
    ):


        result={}



        for rule in scored_rules:


            category = rule.get(
                "category",
                "general"
            )


            if category not in result:

                result[category]=[]



            result[category].append(
                rule
            )



        return result
