"""Approved prose selection follows published Ten Gods and pillar locations."""

from applications.api.services.ten_gods_editorial import _catalog, ten_gods_editorial_paragraphs


def test_catalog_has_ten_gods_and_customer_address() -> None:
    catalog = _catalog()
    assert len(catalog) == 10
    assert all(set(entry["pillar_copy"]) == {"year", "month", "day", "hour"}
               for entry in catalog.values())
    assert all("thầy" not in copy.lower() for entry in catalog.values()
               for copy in entry["pillar_copy"].values())


def test_preserves_all_pillars_and_does_not_invent_unpublished_gods() -> None:
    four_layer = {"layers": [
        {"pillar": "year", "visible": [{"ten_god": "Thất Sát"}],
         "hidden": [{"ten_god": "Thất Sát"}, {"ten_god": "Thiên Tài"}]},
        {"pillar": "month", "visible": [], "hidden": []},
        {"pillar": "day", "visible": [{"ten_god": "Nhật Chủ"}], "hidden": []},
        {"pillar": "hour", "visible": [], "hidden": [{"ten_god": "Thất Sát"}]},
    ]}
    paragraphs = ten_gods_editorial_paragraphs(four_layer)
    assert len(paragraphs) == 3
    assert paragraphs[0].startswith("Thất Sát tại trụ năm (lộ can và tàng chi):")
    assert paragraphs[1].startswith("Thiên Tài tại trụ năm (tàng chi):")
    assert paragraphs[2].startswith("Thất Sát tại trụ giờ (tàng chi):")
    assert not any("Nhật Chủ tại" in paragraph for paragraph in paragraphs)


def test_same_god_in_multiple_pillars_keeps_each_location_once():
    from copy import deepcopy
    four_layer = {"layers": [
        {"pillar": "year", "hidden": [{"ten_god": "Thiên Tài"}, {"ten_god": "Thiên Tài"}]},
        {"pillar": "month", "hidden": [{"ten_god": "Chính Ấn"}]},
        {"pillar": "day", "hidden": [{"ten_god": "Chính Ấn"}]},
        {"pillar": "hour", "hidden": [{"ten_god": "Thiên Tài"}]},
    ]}
    before = deepcopy(four_layer)
    paragraphs = ten_gods_editorial_paragraphs(four_layer)
    assert len(paragraphs) == 4
    for heading in ("Thiên Tài tại trụ năm", "Thiên Tài tại trụ giờ",
                    "Chính Ấn tại trụ tháng", "Chính Ấn tại trụ ngày"):
        assert sum(line.startswith(heading) for line in paragraphs) == 1
    assert four_layer == before


def test_identical_copy_is_grouped_without_losing_positions(monkeypatch):
    from applications.api.services import ten_gods_editorial as module
    monkeypatch.setattr(module, "_catalog", lambda: {
        "Thiên Tài": {"pillar_copy": {"year": "Bạn cân nhắc cơ hội.", "hour": "Bạn cân nhắc cơ hội."}}})
    result = module.ten_gods_editorial_paragraphs({"layers": [
        {"pillar": "year", "visible": [{"ten_god": "Thiên Tài"}]},
        {"pillar": "hour", "hidden": [{"ten_god": "Thiên Tài"}]},
    ]})
    assert len(result) == 1
    assert "trụ năm (lộ can); trụ giờ (tàng chi)" in result[0]
    assert result[0].count("Bạn cân nhắc cơ hội.") == 1


def test_invalid_or_unpublished_roles_do_not_create_copy():
    assert ten_gods_editorial_paragraphs({"layers": None}) == []
    assert ten_gods_editorial_paragraphs({"layers": [
        {"pillar": "day", "visible": [{"ten_god": "Nhật chủ"}, {"ten_god": "Unknown"}]}
    ]}) == []


def test_son_runtime_keeps_wealth_and_resource_in_all_published_positions():
    from applications.api.services.orchestrator import OrchestratorService
    from applications.api.services.bazi_analysis_contract import build_ten_gods_four_layer_view
    payload = OrchestratorService().analyze(year=1987, month=1, day=21, hour=4, minute=31,
                                          gender="male", timezone="Asia/Bangkok")
    result = ten_gods_editorial_paragraphs(build_ten_gods_four_layer_view(payload))
    for heading in ("Thiên Tài tại trụ năm", "Thiên Tài tại trụ giờ",
                    "Chính Ấn tại trụ tháng", "Chính Ấn tại trụ ngày"):
        assert any(line.startswith(heading) for line in result)
