import pytest

from ssb_jordbruk_fagfunksjoner.produksjonstilskudd import VALID_MEASUREMENT_UNITS
from ssb_jordbruk_fagfunksjoner.produksjonstilskudd import Produksjonskode
from ssb_jordbruk_fagfunksjoner.produksjonstilskudd import Produksjonstilskudd


@pytest.fixture(autouse=True)
def clear_produksjonskode_registry():
    """Automatically clear the Produksjonskode registry before each test.

    This ensures that each test starts with an empty codelist
    (so Produksjonstilskudd sees no codes unless the test creates some).
    """
    Produksjonskode._registry.clear()
    yield
    Produksjonskode._registry.clear()


def test_empty_registry_at_start():
    """Because of the autouse fixture,
    we expect the registry to be empty at the start of this test.
    """
    assert len(Produksjonskode._registry) == 0

    # We create a Produksjonstilskudd instance.
    # It should see 0 codes because none have been created.
    pt = Produksjonstilskudd()
    assert len(pt.codes) == 0


def test_add_one_code():
    """This test also starts with an empty registry.
    We'll add one code and confirm it's registered.
    """
    code = Produksjonskode(
        code="001", label="Epler", groups=["frukt"], measured_in="kilo"
    )
    assert len(Produksjonskode._registry) == 1
    assert code in Produksjonskode._registry

    pt = Produksjonstilskudd()
    assert len(pt.codes) == 1
    assert pt.codes[0].code == "001"


def test_no_codes_again():
    """This test shows that after the previous test,
    the registry is automatically cleared by the fixture
    (so we have 0 codes here).
    """
    assert len(Produksjonskode._registry) == 0
    pt = Produksjonstilskudd()
    assert len(pt.codes) == 0


def test_produksjonskode_init_valid():
    """Check that a valid Produksjonskode initializes and registers correctly."""
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


def test_produksjonskode_code_validation():
    """Check that a Produksjonskode must have exactly 3 digits."""
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


def test_produksjonskode_groups_validation():
    """Check that the groups attribute must be a list of strings."""
    with pytest.raises(TypeError, match="groups must be a list"):
        Produksjonskode(
            code="123",
            label="InvalidGroups",
            groups="notalist",  # should be list[str], not str
            measured_in="kilo",
        )

    with pytest.raises(ValueError, match="All values in groups must be strings"):
        Produksjonskode(
            code="123",
            label="InvalidGroups2",
            groups=[1, 2],  # not strings
            measured_in="kilo",
        )

    assert len(Produksjonskode._registry) == 0


def test_produksjonskode_measurement_validation():
    """Check that 'measured_in' must be in VALID_MEASUREMENT_UNITS."""
    invalid_unit = "liter"
    assert invalid_unit not in VALID_MEASUREMENT_UNITS

    with pytest.raises(ValueError, match="Invalid measurement unit"):
        Produksjonskode(
            code="123",
            label="TestMeasurement",
            groups=["some_group"],
            measured_in=invalid_unit,  # not valid
        )

    assert len(Produksjonskode._registry) == 0


def test_produksjonstilskudd_init():
    """Check that Produksjonstilskudd properly retrieves and categorizes the codes."""
    # Create a few codes
    Produksjonskode(code="001", label="Epler", groups=["frukt"], measured_in="kilo")
    Produksjonskode(code="002", label="Pærer", groups=["frukt"], measured_in="kilo")
    Produksjonskode(
        code="101", label="Melkeku", groups=["storfe"], measured_in="antall"
    )

    pt = Produksjonstilskudd()
    assert len(pt.codes) == 3
    assert sorted(pt.categories) == ["frukt", "storfe"]


def test_produksjonstilskudd_get_codes():
    """Ensure get_codes filters by categories and applies prefix if needed."""
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


def test_produksjonstilskudd_get_codes_type_errors():
    """Check type validations for prefix and categories."""
    # No codes needed for this
    pt = Produksjonstilskudd()

    # prefix should be bool
    with pytest.raises(TypeError, match="prefix should be either True or False"):
        pt.get_codes(prefix="yes")

    # categories should be str or list
    with pytest.raises(TypeError, match="expected type str or list"):
        pt.get_codes(categories=123)


def test_produksjonstilskudd_get_codes_by_measurement():
    """Check measurement filtering and prefix in get_codes_by_measurement."""
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


def test_produksjonstilskudd_str_representation():
    """Just a quick check that __str__ doesn't raise and includes expected info."""
    # Create a couple of codes
    Produksjonskode(code="001", label="Epler", groups=["frukt"], measured_in="kilo")
    Produksjonskode(code="002", label="Pærer", groups=["frukt"], measured_in="kilo")
    pt = Produksjonstilskudd()

    string_repr = str(pt)
    # Basic check: the string should mention number of codes & categories
    assert "with 2 Produksjonskoder registered" in string_repr
    assert "1 categories" in string_repr
