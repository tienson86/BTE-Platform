"""
Test Sentence Generator

Kiểm tra:
- Sinh câu diễn giải
- Thay biến template
- Xử lý dữ liệu thiếu
"""


from interpretation_engine.sentence_generator import SentenceGenerator



def test_sentence_generator_create():

    generator = SentenceGenerator()

    assert generator is not None



def test_generate_simple_sentence():

    generator = SentenceGenerator()


    data = {

        "element":
        "Kim",

        "strength":
        "mạnh"

    }


    result = generator.generate(
        data
    )


    assert isinstance(
        result,
        str
    )


    assert len(result) > 0



def test_generate_contains_keyword():

    generator = SentenceGenerator()


    data = {

        "element":
        "Mộc"

    }


    result = generator.generate(
        data
    )


    assert "Mộc" in result



def test_generate_empty_data():

    generator = SentenceGenerator()


    result = generator.generate(
        {}
    )


    assert isinstance(
        result,
        str
    )
