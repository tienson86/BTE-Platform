"""Versioned business rubric projected from the existing compatibility evidence."""

from dataclasses import replace
from math import isfinite

from consulting.business.models import BusinessScoreAudit, BusinessScoreGroup
from consulting.marriage.models.matrix import MarriageCompatibilityMatrix, MarriageMatrixRow

MODEL_VERSION = "business.compatibility.v1"
GROUP_WEIGHTS = (
    ("useful_god", "Dụng thần và Ngũ Hành", 35.0),
    ("stem_branch", "Can Chi", 30.0),
    ("day_master", "Nhật Chủ", 25.0),
    ("cung_phi", "Cung Phi", 10.0),
    ("pattern", "Mệnh Cục", 0.0),
)
STATUS_POINTS = {"supportive": 82.0, "balanced": 65.0, "mixed": 50.0, "pressured": 35.0}
METHODOLOGY = (
    "Quy ước mô hình: hỗ trợ 82 điểm, cân bằng 65, hai chiều 50, áp lực 35. "
    "Mỗi nhóm lấy trung bình điểm các hàng theo độ tin cậy dữ liệu. "
    "Trọng số: Dụng thần 35%, Can Chi 30%, Nhật Chủ 25%, Cung Phi 10%. "
    "Trọng số nhóm thiếu một phần dữ liệu giảm theo tỷ lệ hàng chấm được; "
    "điểm tổng là trung bình có trọng số của các nhóm còn dữ liệu, làm tròn một chữ số thập phân. "
    "Mệnh Cục chỉ làm bối cảnh, không cộng hoặc trừ điểm. "
    "Các trọng số và ngưỡng là quy ước tư vấn, chưa được kiểm định bằng kết quả kinh doanh thực tế."
)
DISCLAIMER = (
    "Điểm tương hợp Bát Tự là chỉ số tham khảo, không phải phần trăm thành công hoặc lợi nhuận. "
    "Không quyết định hợp tác hay góp vốn chỉ dựa vào lá số; cần kiểm chứng năng lực, "
    "uy tín, nguồn lực, thị trường và thỏa thuận giữa hai bên."
)


def score_rows(matrix: MarriageCompatibilityMatrix | None, key: str) -> list[MarriageMatrixRow]:
    sections = {section.key: section.rows for section in matrix.sections} if matrix else {}
    if key in {"useful_god", "cung_phi"}:
        return list(sections.get(key, ()))
    return [row for row in sections.get("structure", ()) if (row.key.startswith("stem_branch") if key == "stem_branch" else row.key == key)]


def recommendation_for_score(score: float) -> tuple[str, str]:
    if score >= 75:
        return "recommended", "Có thể hợp tác"
    if score >= 60:
        return "conditional", "Nên hợp tác có điều kiện"
    if score >= 45:
        return "trial", "Chỉ nên hợp tác thử, quy mô nhỏ"
    return "not_recommended", "Chưa nên hợp tác dài hạn"


def project_business_score(matrix: MarriageCompatibilityMatrix | None) -> BusinessScoreAudit:
    groups = []
    for key, title, weight in GROUP_WEIGHTS:
        rows = score_rows(matrix, key)
        valid = [row for row in rows if weight and row.available and row.status in STATUS_POINTS and isfinite(row.confidence) and 0 < row.confidence <= 1]
        mass = sum(row.confidence for row in valid)
        points = sum(STATUS_POINTS[row.status] * row.confidence for row in valid) / mass if mass else None
        # Missing rows reduce coverage, never create a zero-point penalty.
        expected = max(len(rows), {"useful_god": 2, "cung_phi": 5}.get(key, 1))
        active_weight = weight * len(valid) / expected
        explanation = "Chỉ dùng làm bối cảnh; không quy đổi thành điểm." if not weight else (
            f"Chấm {len(valid)}/{expected} hàng theo độ tin cậy; phần thiếu dữ liệu không bị chấm 0."
            if valid else "Chưa đủ dữ liệu có độ tin cậy để chấm nhóm này."
        )
        groups.append(BusinessScoreGroup(key, title, weight, active_weight, points, 0, mass / len(valid) if valid else 0, len(valid), expected if weight else len(rows), explanation))
    coverage = sum(group.effective_weight for group in groups)
    core = [group for group in groups if group.key in {"useful_god", "stem_branch", "day_master"}]
    has_core = any(group.score is not None for group in core)
    raw_score = round(sum((group.score or 0) * group.effective_weight for group in groups) / coverage, 1) if coverage and has_core else None
    confidence = sum(group.confidence * group.effective_weight for group in groups) / coverage if coverage else 0
    provisional = coverage < 100 - 1e-6 or confidence < 0.7
    reasons = []
    insufficient = raw_score is None or coverage < 80 or confidence < 0.5 or any(group.score is None for group in core)
    if insufficient:
        key, recommendation = "insufficient", "Chưa đủ dữ liệu để khuyến nghị hợp tác"
        reasons.append("Thiếu nhóm đối chiếu lõi, độ phủ dưới 80% hoặc độ tin cậy dữ liệu dưới 50%.")
    else:
        key, recommendation = recommendation_for_score(raw_score)
        # A strong secondary score cannot erase a weak core group.
        weak = [group.title for group in core if group.score is not None and group.score < 40]
        if weak:
            reasons.append(f"Nhóm lõi có áp lực nổi trội: {', '.join(weak)}; điểm tổng không loại bỏ rủi ro này.")
            if key in {"recommended", "conditional"}:
                key, recommendation = "trial", "Chỉ nên hợp tác thử, quy mô nhỏ"
        if confidence < 0.7 and key == "recommended":
            key, recommendation = "conditional", "Nên hợp tác có điều kiện"
            reasons.append("Độ tin cậy dữ liệu dưới 70%, chưa đủ căn cứ cho khuyến nghị thuận lợi hơn.")
    if provisional:
        reasons.append("Điểm tạm tính trên phần dữ liệu hiện có; bổ sung thông tin có thể làm thay đổi điểm và khuyến nghị.")
    advice = {
        "recommended": "Theo đối chiếu Bát Tự, hai người có nền tảng hỗ trợ để cân nhắc hợp tác. Chỉ triển khai sau khi kiểm chứng năng lực, uy tín và thống nhất vai trò, vốn góp, lợi ích, quyền quyết định và cơ chế rút lui.",
        "conditional": "Có thể cân nhắc hợp tác khi có phân công và thỏa thuận rõ bằng văn bản. Nên làm thử trước, đặt giới hạn nguồn lực và đánh giá kết quả thực tế trước khi mở rộng.",
        "trial": "Mô hình còn ghi nhận điểm cần thỏa thuận hoặc áp lực ở nhóm lõi. Chỉ nên thử một dự án nhỏ với trách nhiệm, giới hạn nguồn lực và tiêu chí dừng rõ ràng; chưa nên cam kết dài hạn chỉ từ kết quả này.",
        "not_recommended": "Theo mô hình, các điểm áp lực đang trội hơn phần bổ trợ. Chưa nên cam kết hợp tác dài hạn nếu chưa xử lý được bất đồng và kiểm chứng bằng công việc thực tế; điểm thấp không có nghĩa hai người chắc chắn thất bại.",
        "insufficient": "Chưa kết luận nên hay không nên hợp tác. Bổ sung thông tin lá số và đánh giá năng lực, uy tín, nguồn lực cùng điều kiện kinh doanh trước khi ra quyết định.",
    }[key]
    normalized = tuple(replace(group, score=round(group.score, 1) if group.score is not None else None, effective_weight=round(group.effective_weight / coverage * 100, 4) if coverage and has_core else 0, contribution=round((group.score or 0) * group.effective_weight / coverage, 2) if coverage and has_core else 0, confidence=round(group.confidence, 4)) for group in groups)
    return BusinessScoreAudit(MODEL_VERSION, round(raw_score, 1) if raw_score is not None else None, round(coverage, 1), round(confidence, 4), provisional, key, recommendation, advice, tuple(reasons), normalized, METHODOLOGY, DISCLAIMER)
