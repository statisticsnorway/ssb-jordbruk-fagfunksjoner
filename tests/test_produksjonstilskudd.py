import pytest

from ssb_jordbruk_fagfunksjoner.produksjonstilskudd import Produksjonstilskudd


def test_direct_import() -> None:
    try:
        from ssb_jordbruk_fagfunksjoner import Produksjonstilskudd

        assert isinstance(Produksjonstilskudd(), Produksjonstilskudd)
    except ImportError:
        pytest.fail("Failed to import 'Produksjonstilskudd' module")


@pytest.fixture()
def produksjonstilskudd_instance() -> Produksjonstilskudd:
    return Produksjonstilskudd()


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


def test_dynamic_attributes_creation(
    produksjonstilskudd_instance: Produksjonstilskudd,
) -> None:
    """Test that dynamic attributes are correctly set up."""
    assert hasattr(
        produksjonstilskudd_instance, "frukt_avling"
    ), "Instance should have 'frukt_avling' attribute"
    assert isinstance(
        produksjonstilskudd_instance.frukt_avling, dict
    ), "'frukt_avling' should be a dictionary"


def test_dynamic_combinations_creation(
    produksjonstilskudd_instance: Produksjonstilskudd,
) -> None:
    """Test that dynamic combination attributes are correctly set up."""
    assert hasattr(
        produksjonstilskudd_instance, "frukt"
    ), "Instance should have 'frukt' combination attribute"
    combination = produksjonstilskudd_instance.frukt
    assert (
        "001" in combination and "271" in combination
    ), "'frukt' combination should contain codes from its groups"


def test_dynamic_tabell_creation(
    produksjonstilskudd_instance: Produksjonstilskudd,
) -> None:
    assert hasattr(
        produksjonstilskudd_instance, "tabell_storfe"
    ), "Instance should have 'tabell_storfe' attribute"
    assert isinstance(
        produksjonstilskudd_instance.tabell_storfe, dict
    ), "'tabell_storfe' should be a dictionary"
