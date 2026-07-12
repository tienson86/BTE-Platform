
class RuleScoring:



    def score(self,rule):


        score=0



        try:

            score += int(
                rule.get(
                    "base_score",
                    0
                )
            )

        except:

            pass



        try:

            score *= float(
                rule.get(
                    "weight",
                    1
                )
            )

        except:

            pass



        priority = rule.get(
            "priority",
            ""
        )


        if priority=="HIGH":

            score*=1.5


        elif priority=="LOW":

            score*=0.8



        return score



    def scoring_rules(
        self,
        rules
    ):

        result=[]


        for rule in rules:

            s=self.score(rule)


            item=rule.copy()

            item["score"]=s


            result.append(item)



        result.sort(
            key=lambda x:x["score"],
            reverse=True
        )


        return result
