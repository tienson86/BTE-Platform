"""
Test Interpretation Context

Kiểm tra:
- Khởi tạo context
- Lưu dữ liệu
- Truy xuất dữ liệu
- Cập nhật dữ liệu
- Metadata
"""


from interpretation_engine.context import InterpretationContext



def test_create_context():

    ctx = InterpretationContext()

    assert ctx is not None



def test_set_and_get_value():

    ctx = InterpretationContext()


    ctx.set(
        "nhat_chu",
        "Canh Kim"
    )


    result = ctx.get(
        "nhat_chu"
    )


    assert result == "Canh Kim"



def test_update_value():

    ctx = InterpretationContext()


    ctx.set(
        "ngu_hanh",
        "Kim"
    )


    ctx.set(
        "ngu_hanh",
        "Thuy"
    )


    assert ctx.get(
        "ngu_hanh"
    ) == "Thuy"



def test_missing_value():

    ctx = InterpretationContext()


    result = ctx.get(
        "khong_ton_tai"
    )


    assert result is None



def test_context_contains():

    ctx = InterpretationContext()


    ctx.set(
        "thang_lenh",
        "Sửu"
    )


    assert ctx.has(
        "thang_lenh"
    )
