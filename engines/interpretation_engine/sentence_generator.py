
class SentenceGenerator:



    def generate_sentence(
        self,
        rule
    ):


        template = rule.get(
            "sentence",
            ""
        )


        return template



    def generate(
        self,
        grouped_rules
    ):


        output={}



        for category,rules in grouped_rules.items():


            sentences=[]


            for rule in rules:

                sentence=self.generate_sentence(
                    rule
                )

                if sentence:

                    sentences.append(
                        sentence
                    )


            output[category]=sentences



        return output
