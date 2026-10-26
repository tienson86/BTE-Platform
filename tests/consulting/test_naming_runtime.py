import pytest

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.naming.models import NamingRequest
from consulting.naming.service import analyze_naming


@pytest.fixture(scope="module")
def adapter():
    return CanonicalOrchestratorAdapter()


@pytest.mark.parametrize("gender,birth_date,birth_time", [
    ("male", "2020-05-10", "08:30"),
    ("female", "2024-02-29", "00:00"),
    ("female", "1990-01-15", None),
])
def test_naming_runs_with_existing_canonical_engines(adapter, gender, birth_date, birth_time):
    request = NamingRequest(
        family_name="Trần", gender=gender, birth_date=birth_date,
        birth_time=birth_time, count=10,
    )
    result = analyze_naming(request, adapter=adapter)
    assert len(result["recommendations"]) == 10
    assert result["signals"]["nap_am"]
    assert result["signals"]["nap_am_element"]
    assert result["signals"]["cung_phi"]
    assert result["signals"]["cung_phi_element"]
    if birth_time is None:
        assert result["signals"]["useful_elements"] == []
        assert result["signals"]["pillars"]["hour"] is None
        assert result["quality"] == "preliminary"
    else:
        assert result["signals"]["useful_elements"]
        assert result["signals"]["pillars"]["hour"]
