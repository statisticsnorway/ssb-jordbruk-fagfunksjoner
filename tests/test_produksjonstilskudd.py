import pytest

from ssb_jordbruk_fagfunksjoner.produksjonstilskudd import Produksjonskode
from ssb_jordbruk_fagfunksjoner.produksjonstilskudd import Produksjonstilskudd


@pytest.fixture()
def produksjonstilskudd_instance() -> Produksjonstilskudd:
    return Produksjonstilskudd()


def test_add_new_code():  # Test at den også havner i Produksjonstilskudd
    Produksjonskode(
        code="123",
        label="test",
        description="",
        groups=[""],
        measured_in="antall",
    )


def test_get_codes_with_prefix(
    produksjonstilskudd_instance: Produksjonstilskudd,
) -> None:
    """Test that get_codes correctly adds 'pk_' prefix."""
    prefixed_codes = produksjonstilskudd_instance.get_codes("frukt_avling", prefix=True)
    for code in prefixed_codes:
        assert code.startswith("pk_"), "All codes should be prefixed with 'pk_'"


def test_get_codes_without_prefix(
    produksjonstilskudd_instance: Produksjonstilskudd,
) -> None:
    """Test that get_codes returns codes without prefix by default."""
    codes = produksjonstilskudd_instance.get_codes("frukt_avling")
    for code in codes:
        assert not code.startswith(
            "pk_"
        ), "Codes should not have 'pk_' prefix by default"


def test_get_codes_all(produksjonstilskudd_instance: Produksjonstilskudd) -> None:
    """Test that get_codes returns all codes when no attributes are specified."""
    all_codes = produksjonstilskudd_instance.get_codes()
    assert len(all_codes) == len(
        produksjonstilskudd_instance.codes
    ), "Should return all codes"
