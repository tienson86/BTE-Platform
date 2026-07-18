class SentenceGenerator:
    def generate(self, interpretation_result):
        if isinstance(interpretation_result, dict):
            return "BTE interpretation"
        return "BTE interpretation"


def generate_sentences(interpretation_result):
    return SentenceGenerator().generate(interpretation_result)
