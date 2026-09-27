"""Approved prose selection follows published Ten Gods and pillar locations."""

from applications.api.services.ten_gods_editorial import _catalog, ten_gods_editorial_paragraphs


def test_catalog_has_ten_gods_and_customer_address() -> None:
    catalog = _catalog()
    assert len(catalog) == 10
    assert all(set(entry["pillar_copy"]) == {"year", "month", "day", "hour"}
               for entry in catalog.values())
    assert all("thầy" not in copy.lower() for entry in catalog.values()
               for copy in entry["pillar_copy"].values())


def test_prefers_visible_role_and_does_not_invent_unpublished_gods() -> None:
    four_layer = {"layers": [
        {"pillar": "year", "visible": [{"ten_god": "Thất Sát"}],
         "hidden": [{"ten_god": "Thất Sát"}, {"ten_god": "Thiên Tài"}]},
        {"pillar": "month", "visible": [], "hidden": []},
        {"pillar": "day", "visible": [{"ten_god": "Nhật Chủ"}], "hidden": []},
        {"pillar": "hour", "visible": [], "hidden": [{"ten_god": "Thất Sát"}]},
    ]}
    paragraphs = ten_gods_editorial_paragraphs(four_layer)
    assert len(paragraphs) == 2
    assert paragraphs[0].startswith("Thất Sát tại trụ năm (lộ can):")
    assert paragraphs[1].startswith("Thiên Tài tại trụ năm (tàng chi):")
    assert not any("Nhật Chủ tại" in paragraph for paragraph in paragraphs)
