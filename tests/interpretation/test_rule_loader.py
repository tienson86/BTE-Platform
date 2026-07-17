"""
Test Rule Loader

Kiểm tra:
- Khởi tạo RuleLoader
- Load file rule CSV
- Parse dữ liệu rule
- Validate cấu trúc rule
- Xử lý lỗi
"""


import pytest


from interpretation_engine.rule_loader import RuleLoader



# ==================================================
# Test khởi tạo
# ==================================================

def test_rule_loader_create():

    loader = RuleLoader()

    assert loader is not None



# ==================================================
# Test load rule database
# ==================================================

def test_load_rule_file():


    loader = RuleLoader()


    rules = loader.load(
        "tests/data/test_rules.csv"
    )


    assert isinstance(
        rules,
        list
    )


    assert len(rules) > 0



# ==================================================
# Test cấu trúc Rule
# ==================================================

def test_rule_structure():


    loader = RuleLoader()


    rules = loader.load(
        "tests/data/test_rules.csv"
    )


    rule = rules[0]


    assert "rule_id" in rule

    assert "rule_name" in rule

    assert "condition" in rule

    assert "score" in rule

    assert "message" in rule



# ==================================================
# Test nhiều Rule
# ==================================================

def test_load_multiple_rules():


    loader = RuleLoader()


    rules = loader.load(
        "tests/data/test_rules.csv"
    )


    assert len(rules) >= 2



# ==================================================
# Test file rỗng
# ==================================================

def test_empty_rule_file():


    loader = RuleLoader()


    rules = loader.load(
        "tests/data/empty_rules.csv"
    )


    assert rules == []



# ==================================================
# Test file không tồn tại
# ==================================================

def test_missing_file():


    loader = RuleLoader()


    with pytest.raises(
        FileNotFoundError
    ):

        loader.load(
            "tests/data/not_exists.csv"
        )



# ==================================================
# Test reload
# ==================================================

def test_reload_rules():


    loader = RuleLoader()


    first_load = loader.load(
        "tests/data/test_rules.csv"
    )


    second_load = loader.load(
        "tests/data/test_rules.csv"
    )


    assert first_load == second_load
