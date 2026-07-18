from ..engine import HIDDEN


class HiddenStemService:
    def get(self, branch: str) -> list[str]:
        return list(HIDDEN.get(branch, []))
