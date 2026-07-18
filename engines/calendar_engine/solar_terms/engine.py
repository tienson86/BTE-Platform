from dataclasses import dataclass


@dataclass(slots=True)
class SolarTerm:
    name: str
    index: int


class SolarTermEngine:
    _names = ("Lập Xuân", "Vũ Thủy", "Kinh Trập", "Xuân Phân", "Thanh Minh", "Cốc Vũ", "Lập Hạ", "Tiểu Mãn", "Mang Chủng", "Hạ Chí", "Tiểu Thử", "Đại Thử", "Lập Thu", "Xử Thử", "Bạch Lộ", "Thu Phân", "Hàn Lộ", "Sương Giáng", "Lập Đông", "Tiểu Tuyết", "Đại Tuyết", "Đông Chí", "Tiểu Hàn", "Đại Hàn")

    def list_terms(self, year: int) -> list[SolarTerm]:
        return [SolarTerm(name, i) for i, name in enumerate(self._names)]

    def get_current_term(self, year: int, month: int, day: int) -> SolarTerm:
        return self.list_terms(year)[((month - 1) * 2 + (day >= 16)) % 24]

    get_term = get_current_term
