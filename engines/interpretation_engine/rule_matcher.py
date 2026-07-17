def check_condition(
    self,
    context,
    condition,
):
    """
    Kiểm tra một điều kiện Rule.

    Hỗ trợ:

    - dict
    - JSON string
    - key=value
    - chuỗi đơn
    """

    if condition is None:
        return True

    if condition == "":
        return True

    # ------------------------------
    # String
    # ------------------------------

    if isinstance(condition, str):

        condition = condition.strip()

        if condition == "":
            return True

        # JSON
        if condition.startswith("{"):

            import json

            try:
                condition = json.loads(condition)

            except Exception:
                return False

        # key=value
        elif "=" in condition:

            key, value = condition.split("=", 1)

            condition = {
                key.strip(): value.strip()
            }

        else:

            return False

    # ------------------------------
    # Dict
    # ------------------------------

    if not isinstance(condition, dict):
        return False

    # ------------------------------
    # Compare
    # ------------------------------

    for key, expected in condition.items():

        actual = None

        # tra trong bazi
        if hasattr(context, "bazi"):

            actual = context.bazi.get(key)

        # tra trong elements
        if actual is None and hasattr(context, "elements"):

            actual = context.elements.get(key)

        # tra trong ten_gods
        if actual is None and hasattr(context, "ten_gods"):

            actual = context.ten_gods.get(key)

        # tra trong pattern
        if actual is None and hasattr(context, "patterns"):

            actual = context.patterns.get(key)

        if str(actual) != str(expected):
            return False

    return True
