from .ten_god import TenGod, TenGodResult


class TenGodService:
    def calculate(self, day_master: str, target: str | None = None):
        if target is None:
            target = day_master
        return TenGodResult(day_master, target, TenGod(name="Tỷ Kiên", code="ty_kien"))
