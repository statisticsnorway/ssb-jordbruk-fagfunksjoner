import pytest

from ssb_jordbruk_fagfunksjoner.produksjonstilskudd import Produksjonstilskudd


@pytest.fixture()
def produksjonstilskudd_instance():
    return Produksjonstilskudd()


def test_get_codes_with_prefix(produksjonstilskudd_instance):
    """Test that get_codes correctly adds 'PK_' prefix."""
    prefixed_codes = produksjonstilskudd_instance.get_codes("frukt_avling", prefix=True)
    for code in prefixed_codes:
        assert code.startswith("PK_"), "All codes should be prefixed with 'PK_'"


def test_get_codes_without_prefix(produksjonstilskudd_instance):
    """Test that get_codes returns codes without prefix by default."""
    codes = produksjonstilskudd_instance.get_codes("frukt_avling")
    for code in codes:
        assert not code.startswith(
            "PK_"
        ), "Codes should not have 'PK_' prefix by default"


def test_get_codes_all(produksjonstilskudd_instance):
    """Test that get_codes returns all codes when no attributes are specified."""
    all_codes = produksjonstilskudd_instance.get_codes()
    assert len(all_codes) == len(
        produksjonstilskudd_instance.codes
    ), "Should return all codes"


def test_dynamic_attributes_creation(produksjonstilskudd_instance):
    """Test that dynamic attributes are correctly set up."""
    assert hasattr(
        produksjonstilskudd_instance, "frukt_avling"
    ), "Instance should have 'frukt_avling' attribute"
    assert isinstance(
        produksjonstilskudd_instance.frukt_avling, dict
    ), "'frukt_avling' should be a dictionary"


def test_dynamic_combinations_creation(produksjonstilskudd_instance):
    """Test that dynamic combination attributes are correctly set up."""
    assert hasattr(
        produksjonstilskudd_instance, "frukt"
    ), "Instance should have 'frukt' combination attribute"
    combination = produksjonstilskudd_instance.frukt
    assert (
        "001" in combination or "271" in combination
    ), "'frukt' combination should contain codes from its groups"
