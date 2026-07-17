"""
Test Interpretation Builder

Kiểm tra:
- Tạo kết quả luận giải
- Ghép các rule
- Xử lý dữ liệu rỗng
"""


from interpretation_engine.interpretation_builder import InterpretationBuilder



def test_builder_create():

    builder = InterpretationBuilder()

    assert builder is not None



def test_build_single_rule():

    builder = InterpretationBuilder()


    rules = [

        {

            "message":
            "Nhật chủ Canh Kim có lực mạnh"

        }

    ]


    result = builder.build(
        rules
    )


    assert result is not None



def test_build_contains_message():

    builder = InterpretationBuilder()


    rules = [

        {

            "message":
            "Nhật chủ mạnh"

        }

    ]


    result = builder.build(
        rules
    )


    assert "Nhật chủ mạnh" in result.text



def test_build_multiple_rules():

    builder = InterpretationBuilder()


    rules = [

        {
            "message":
            "Kim vượng"
        },

        {
            "message":
            "Quan tinh xuất hiện"
        }

    ]


    result = builder.build(
        rules
    )


    assert "Kim vượng" in result.text

    assert "Quan tinh xuất hiện" in result.text



def test_build_empty_rules():

    builder = InterpretationBuilder()


    result = builder.build(
        []
    )


    assert result is not None
