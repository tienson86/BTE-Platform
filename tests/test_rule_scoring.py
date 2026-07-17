"""
Test Rule Scoring

Kiểm tra:
- Khởi tạo RuleScoring
- Tính tổng điểm rule
- Xử lý điểm âm
- Xử lý rule thiếu score
- Tính điểm từ danh sách rule
"""


from interpretation_engine.rule_scoring import RuleScoring
from interpretation_engine.rule_loader import RuleLoader



# ==================================================
# Khởi tạo
# ==================================================

def test_rule_scoring_create():

    scorer = RuleScoring()

    assert scorer is not None



# ==================================================
# Một rule có điểm
# ==================================================

def test_single_rule_score():

    scorer = RuleScoring()


    rules = [

        {
            "score": 10
        }

    ]


    result = scorer.calculate(
        rules
    )


    assert result == 10



# ==================================================
# Nhiều rule cộng điểm
# ==================================================

def test_multiple_rule_score():

    scorer = RuleScoring()


    rules = [

        {
            "score": 10
        },

        {
            "score": 5
        },

        {
            "score": 3
        }

    ]


    result = scorer.calculate(
        rules
    )


    assert result == 18



# ==================================================
# Có điểm âm
# ==================================================

def test_negative_score():

    scorer = RuleScoring()


    rules = [

        {
            "score": 10
        },

        {
            "score": -5
        }

    ]


    result = scorer.calculate(
        rules
    )


    assert result == 5



# ==================================================
# Danh sách rỗng
# ==================================================

def test_empty_rules():

    scorer = RuleScoring()


    result = scorer.calculate(
        []
    )


    assert result == 0



# ==================================================
# Rule thiếu score
# ==================================================

def test_missing_score_field():

    scorer = RuleScoring()


    rules = [

        {
            "rule_id": "R001"
        }

    ]


    result = scorer.calculate(
        rules
    )


    assert result == 0



# ==================================================
# Score dạng chuỗi từ CSV
# ==================================================

def test_string_score_conversion():

    scorer = RuleScoring()


    rules = [

        {
            "score": "10"
        },

        {
            "score": "5"
        }

    ]


    result = scorer.calculate(
        rules
    )


    assert result == 15



# ==================================================
# Test với RuleLoader
# ==================================================

def test_score_loaded_rules():

    loader = RuleLoader()


    rules = loader.load(
        "tests/data/test_rules.csv"
    )


    scorer = RuleScoring()


    result = scorer.calculate(
        rules
    )


    assert result != 0
