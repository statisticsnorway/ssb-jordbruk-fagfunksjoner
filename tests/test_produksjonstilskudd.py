from collections.abc import Generator

import pytest

from ssb_jordbruk_fagfunksjoner.produksjonstilskudd import VALID_MEASUREMENT_UNITS
from ssb_jordbruk_fagfunksjoner.produksjonstilskudd import Produksjonskode
from ssb_jordbruk_fagfunksjoner.produksjonstilskudd import Produksjonstilskudd


@pytest.fixture(autouse=True)
def clear_produksjonskode_registry() -> Generator[None, None, None]:
    """Automatically clears the Produksjonskode registry before each test.

    This ensures that each test starts with an empty codelist (so Produksjonstilskudd
    sees no codes unless the test explicitly creates some). After yielding to
    the test, it clears the registry again.

    Yields:
        None: Control is yielded to the test, after which the registry is cleared.
    """
    Produksjonskode._registry.clear()
    yield
    Produksjonskode._registry.clear()


def test_empty_registry_at_start() -> None:
    """Tests that the Produksjonskode registry is empty at the beginning.

    Verifies that the autouse fixture has cleared the registry so we have
    no codes at the start of this test.
    """
    assert len(Produksjonskode._registry) == 0

    # We create a Produksjonstilskudd instance.
    # It should see 0 codes because none have been created.
    pt = Produksjonstilskudd()
    assert len(pt.codes) == 0


def test_add_one_code() -> None:
    """Tests that adding one code populates the registry.

    After adding a single Produksjonskode, this test checks:
    1) The code is actually in the registry.
    2) Produksjonstilskudd sees exactly one code.
    """
    code = Produksjonskode(
        code="001", label="Epler", groups=["frukt"], measured_in="kilo"
    )
    assert len(Produksjonskode._registry) == 1
    assert code in Produksjonskode._registry

    pt = Produksjonstilskudd()
    assert len(pt.codes) == 1
    assert pt.codes[0].code == "001"


def test_no_codes_again() -> None:
    """Tests that a subsequent test sees an empty registry again.

    Verifies that after the previous test which added codes, the autouse fixture
    clears the registry so we start this test with zero codes.
    """
    assert len(Produksjonskode._registry) == 0
    pt = Produksjonstilskudd()
    assert len(pt.codes) == 0


def test_produksjonskode_init_valid() -> None:
    """Tests that a valid Produksjonskode initializes and registers correctly.

    Checks:
    1) The code has correct attributes.
    2) It appears in the registry.
    """
    code = Produksjonskode(
        code="001",
        label="Epler",
        groups=["frukt", "frukt_avling"],
        measured_in="kilo",
        description="Avling av epler",
    )

    assert code.code == "001"
    assert code.label == "Epler"
    assert code.groups == ["frukt", "frukt_avling"]
    assert code.measured_in == "kilo"
    assert code.description == "Avling av epler"

    # Check it was added to the registry
    assert code in Produksjonskode._registry
    assert len(Produksjonskode._registry) == 1


def test_produksjonskode_code_validation() -> None:
    """Tests that a Produksjonskode must have exactly 3 digits.

    Attempts to create codes of incorrect length (2 and 4 digits)
    and expects ValueError.
    """
    with pytest.raises(ValueError, match="Must be exactly 3 digits"):
        Produksjonskode(
            code="12",  # too short
            label="Test",
            groups=["test"],
            measured_in="kilo",
        )

    with pytest.raises(ValueError, match="Must be exactly 3 digits"):
        Produksjonskode(
            code="1234",  # too long
            label="Test",
            groups=["test"],
            measured_in="kilo",
        )

    assert len(Produksjonskode._registry) == 0


def test_produksjonskode_groups_validation() -> None:
    """Tests that the 'groups' attribute must be a list of strings.

    Attempts to create Produksjonskode instances with incorrect group
    data types and expects errors.
    """
    with pytest.raises(TypeError, match="groups must be a list"):
        Produksjonskode(
            code="123",
            label="InvalidGroups",
            groups="notalist",  # type: ignore[arg-type]
            measured_in="kilo",
        )

    with pytest.raises(ValueError, match="All values in groups must be strings"):
        Produksjonskode(
            code="123",
            label="InvalidGroups2",
            groups=[1, 2],  # type: ignore[list-item]
            measured_in="kilo",
        )

    assert len(Produksjonskode._registry) == 0


def test_produksjonskode_measurement_validation() -> None:
    """Tests that 'measured_in' must be one of the VALID_MEASUREMENT_UNITS.

    Attempts to create a code with an invalid measurement unit and expects
    a ValueError.
    """
    invalid_unit = "liter"
    assert invalid_unit not in VALID_MEASUREMENT_UNITS

    with pytest.raises(ValueError, match="Invalid measurement unit"):
        Produksjonskode(
            code="123",
            label="TestMeasurement",
            groups=["some_group"],
            measured_in=invalid_unit,
        )

    assert len(Produksjonskode._registry) == 0


def test_produksjonstilskudd_init() -> None:
    """Tests that Produksjonstilskudd correctly retrieves codes and compiles categories.

    Adds several Produksjonskode instances, then checks:
    1) The correct number of codes appear in Produksjonstilskudd.
    2) The categories are as expected.
    """
    # Create a few codes
    Produksjonskode(code="001", label="Epler", groups=["frukt"], measured_in="kilo")
    Produksjonskode(code="002", label="Pærer", groups=["frukt"], measured_in="kilo")
    Produksjonskode(
        code="101", label="Melkeku", groups=["storfe"], measured_in="antall"
    )

    pt = Produksjonstilskudd()
    assert len(pt.codes) == 3
    assert sorted(pt.categories) == ["frukt", "storfe"]


def test_produksjonstilskudd_get_codes() -> None:
    """Tests filtering codes by category and optional prefix application.

    1) No categories => all codes.
    2) Single category => codes in that category.
    3) Multiple categories => combined result.
    4) Prefix => add 'pk_' to returned codes.
    """
    # Create codes in two different categories
    Produksjonskode(code="001", label="Epler", groups=["frukt"], measured_in="kilo")
    Produksjonskode(code="002", label="Pærer", groups=["frukt"], measured_in="kilo")
    Produksjonskode(
        code="101", label="Melkeku", groups=["storfe"], measured_in="antall"
    )

    pt = Produksjonstilskudd()

    # 1) No categories specified => returns all codes
    all_codes = pt.get_codes()
    assert sorted(all_codes) == sorted(["001", "002", "101"])

    # 2) Single category, as string
    frukt_codes = pt.get_codes(categories="frukt")
    assert sorted(frukt_codes) == sorted(["001", "002"])

    # 3) Multiple categories, as list
    frukt_storfe = pt.get_codes(categories=["frukt", "storfe"])
    assert frukt_storfe == ["001", "002", "101"]

    # 4) With prefix
    frukt_codes_prefixed = pt.get_codes(categories="frukt", prefix=True)
    assert frukt_codes_prefixed == ["pk_001", "pk_002"]


def test_produksjonstilskudd_get_codes_type_errors() -> None:
    """Tests type validations for 'prefix' and 'categories' in get_codes().

    1) 'prefix' must be a bool.
    2) 'categories' must be either a str, a list, or None.
    """
    # No codes needed for this
    pt = Produksjonstilskudd()

    # prefix should be bool
    with pytest.raises(TypeError, match="prefix should be either True or False"):
        pt.get_codes(prefix="yes")  # type: ignore[arg-type] # Intentionally invalid

    # categories should be str or list
    with pytest.raises(TypeError, match="expected type str or list"):
        pt.get_codes(categories=123)  # type: ignore[arg-type] # Intentionally invalid


def test_produksjonstilskudd_get_codes_by_measurement() -> None:
    """Tests retrieval of codes by measurement unit, plus optional prefix.

    1) Filter by 'kilo' measurement unit.
    2) Filter by 'antall' measurement unit.
    3) Invalid measurement => raises ValueError.
    4) 'prefix' => add 'pk_' to each code.
    """
    # Create codes with different measurement units
    Produksjonskode(code="001", label="Epler", groups=["frukt"], measured_in="kilo")
    Produksjonskode(code="002", label="Pærer", groups=["frukt"], measured_in="kilo")
    Produksjonskode(
        code="101", label="Melkeku", groups=["storfe"], measured_in="antall"
    )

    pt = Produksjonstilskudd()

    # 1) Retrieve codes measured in 'kilo'
    kilo_codes = pt.get_codes_by_measurement("kilo")
    assert kilo_codes == ["001", "002"]

    # 2) Retrieve codes measured in 'antall'
    antall_codes = pt.get_codes_by_measurement("antall")
    assert antall_codes == ["101"]

    # 3) Invalid measurement
    with pytest.raises(ValueError, match="Invalid measurement unit"):
        pt.get_codes_by_measurement("liter")

    # 4) With prefix
    kilo_codes_prefixed = pt.get_codes_by_measurement("kilo", prefix=True)
    assert kilo_codes_prefixed == ["pk_001", "pk_002"]


def test_produksjonstilskudd_str_representation() -> None:
    """Tests that __str__ doesn't raise and contains expected info.

    Creates two codes, checks the string representation for:
    1) The number of registered codes.
    2) The number of categories.
    """
    # Create a couple of codes
    Produksjonskode(code="001", label="Epler", groups=["frukt"], measured_in="kilo")
    Produksjonskode(code="002", label="Pærer", groups=["frukt"], measured_in="kilo")
    pt = Produksjonstilskudd()

    string_repr = str(pt)
    # Basic check: the string should mention number of codes & categories
    assert "with 2 Produksjonskoder registered" in string_repr
    assert "1 categories" in string_repr
