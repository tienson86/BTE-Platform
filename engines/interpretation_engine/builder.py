from .models import InterpretationReport


class InterpretationBuilder:
    def build(self, context):
        return InterpretationReport(text="BTE interpretation")
