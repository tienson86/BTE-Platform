"""
Interpretation Context
=====================

Quản lý dữ liệu đầu vào cho Interpretation Engine.

Nhiệm vụ:

- Lưu thông tin lá số.
- Chuẩn hóa context.
- Cung cấp dữ liệu cho Rule Engine.

Không chứa logic luận giải.
"""


from dataclasses import dataclass, field
from typing import Dict, Any, Optional





@dataclass
class InterpretationContext:


    # dữ liệu tứ trụ

    bazi: Dict[str, Any] = field(
        default_factory=dict
    )


    # ngũ hành

    elements: Dict[str, Any] = field(
        default_factory=dict
    )


    # thập thần

    ten_gods: Dict[str, Any] = field(
        default_factory=dict
    )


    # cách cục

    patterns: Dict[str, Any] = field(
        default_factory=dict
    )


    # dụng thần

    useful_god: Dict[str, Any] = field(
        default_factory=dict
    )


    # đại vận

    luck_cycles: Dict[str, Any] = field(
        default_factory=dict
    )


    # lưu niên

    annual_cycles: Dict[str, Any] = field(
        default_factory=dict
    )


    # thần sát

    shen_sha: Dict[str, Any] = field(
        default_factory=dict
    )


    # dữ liệu mở rộng

    extra: Dict[str, Any] = field(
        default_factory=dict
    )



    def to_dict(self):

        return {

            "bazi": self.bazi,

            "elements": self.elements,

            "ten_gods": self.ten_gods,

            "patterns": self.patterns,

            "useful_god": self.useful_god,

            "luck_cycles": self.luck_cycles,

            "annual_cycles": self.annual_cycles,

            "shen_sha": self.shen_sha,

            "extra": self.extra

        }




def create_context(
    data: Optional[Dict[str,Any]]=None
):


    if data is None:

        return InterpretationContext()



    return InterpretationContext(

        **data

    )
