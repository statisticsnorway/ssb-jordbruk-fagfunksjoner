"""Uses a registry pattern to build the Produksjonstilskudd codelist based on all currently created Produksjonskode objects, as they add themselves to the _PRODUKSJONSKODER_REGISTRY list as they are created.
"""

import re

_PRODUKSJONSKODER_REGISTRY: list["Produksjonskode"] = []

VALID_MEASUREMENT_UNITS = {"antall", "dekar"}


class Produksjonstilskudd:
    """Should be possible to retrieve codes by measurement."""

    def __init__(self) -> None:
        self.codes = _PRODUKSJONSKODER_REGISTRY

        categories = set()
        for code in self.codes:
            for group in code.groups:
                categories.add(group)
        self.categories = list(sorted(categories))

    def get_codes(self, categories=None):
        if categories is None:
            categories = self.categories
        if isinstance(categories, str):
            categories = [categories]
        if not isinstance(categories, list):
            raise TypeError(
                f"Received object of type {type(categories)}, expected type str or list."
            )

        relevant_codes = []
        for code in self.codes:
            if any(group in categories for group in code.groups):
                relevant_codes.append(code)

        return [x.code for x in relevant_codes]

    def __str__(self):
        return f"Produksjonstilskudd object with {len(self.codes)} Produksjonskoder registered.\nCodes are organized in a total of {len(self.categories)} categories."


class Produksjonskode:
    def __init__(
        self,
        code,
        label,
        groups,
        measured_in,
        description=None,
        valid_from=None,
        valid_to=None,
        replaces=None,
        replaced_by=None,
    ):
        if not re.fullmatch(r"\d{3}", code):  # Checks that the code is 3 digits.
            raise ValueError(
                f"Invalid code: {code}. Must be exactly 3 digits (e.g., '101')."
            )

        if not isinstance(groups, list):
            raise TypeError(f"Invalid type: {type(groups)}. groups must be a list")

        _invalid_values = [value for value in groups if not isinstance(value, str)]
        if _invalid_values:
            raise ValueError(
                f"All values in groups must be strings. Invalid values: {_invalid_values}"
            )

        if measured_in not in VALID_MEASUREMENT_UNITS:
            raise ValueError(
                f"Invalid measurement unit: {measured_in}. Must be one of {VALID_MEASUREMENT_UNITS}"
            )

        self.code = code
        self.label = label
        self.description = description if description else None
        self.valid_from = valid_from if valid_from else None
        self.valid_to = valid_to if valid_to else None
        self.replaces = replaces if replaces else []
        self.replaced_by = replaced_by if replaced_by else []
        self.groups = groups if groups else []
        self.measured_in = measured_in

        _PRODUKSJONSKODER_REGISTRY.append(self)  # Registers itself in the registry

    def __str__(self):
        """Returns a human-readable string representation of the object."""
        return (
            f"Produksjonskode:\n"
            f"  Code: {self.code}\n"
            f"  Label: {self.label}\n"
            f"  Valid From: {self.valid_from}\n"
            f"  Valid To: {self.valid_to if self.valid_to else 'N/A'}\n"
            f"  Replaces: {', '.join(self.replaces) if self.replaces else 'None'}\n"
            f"  Replaced By: {', '.join(self.replaced_by) if self.replaced_by else 'None'}\n"
            f"  Groups: {', '.join(self.groups) if self.groups else 'None'}\n"
            f"  Measured In: {self.measured_in if self.measured_in else 'N/A'}"
        )

    def __repr__(self):
        """Returns a detailed string representation for debugging."""
        return (
            f"Produksjonskode("
            f"code={self.code!r}, label={self.label!r}, "
            f"valid_from={self.valid_from!r}, valid_to={self.valid_to!r}, "
            f"replaces={self.replaces!r}, replaced_by={self.replaced_by!r}, "
            f"groups={self.groups!r}, measured_in={self.measured_in!r})"
        )


"""Add the codes below by creating instances of the class Produksjonskode.

Copy paste this template and fill it with information.
Produksjonskode(
    code="",
    label="",
    description="",
    groups=[""],
    measured_in="",
)

When created they add themselves to the registry, making maintenance simpler.
"""

Produksjonskode(
    code="001",
    label="Epler",
    description="Avling av epler",
    groups=["Frukt", "Frukt avling"],
    measured_in="antall",
)


Produksjonskode(
    code="272",
    label="Epler",
    description="Areal med epler",
    groups=["Frukt", "Frukt areal"],
    measured_in="dekar",
)

Produksjonskode(
    code="002",
    label="Pærer",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="273",
    label="Pærer",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="006",
    label="Epler og pærer til press",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="003",
    label="Plommer",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="274",
    label="Plommer",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="004",
    label="Moreller",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="005",
    label="Kirsebær",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="011",
    label="Jordbær",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="012",
    label="Bringebær",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="013",
    label="Solbær",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="014",
    label="Rips",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="016",
    label="Hageblåbær",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="021",
    label="Stikkelsbær",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="022",
    label="Industribær",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="031",
    label="Tomat",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="032",
    label="Slangeagurk",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="033",
    label="Salat (også friland)",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="060",
    label="Matpoteter i Nord-Norge",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="115",
    label="Hester, under 3 år",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="116",
    label="Hester, 3 år og eldre",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="118",
    label="Ammekyr av minst 50% kjøttferase",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="119",
    label="Øvrige storfe",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="120",
    label="Melkekyr",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="121",
    label="Ammekyr",
    description="",
    groups=[""],
    measured_in="",
)


Produksjonskode(
    code="139",
    label="Melkesau",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="140",
    label="Melkegeiter",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="142",
    label="Ammegeiter",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="144",
    label="Bukker og ungdyr, medregnet kje",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="145",
    label="Søyer født i fjor eller tidligere",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="146",
    label="Værer født i fjor eller tidligere",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="154",
    label="Smågriser, levendevekt under 20kg eller alder inntil 8 uker",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="155",
    label="Avlspurker som har fått minst 1 kull",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="156",
    label="Råner som er satt inn i avl",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="157",
    label="Slaktegriser, levendevekt minst 20kg",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="158",
    label="Ungpurker bestemt for avl",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="159",
    label="Ungråner bestemt for avl",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="161",
    label="Verpehøner",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="162",
    label="Rugeegg levert til rugeri",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="168",
    label="Avlsdyr av ender, kalkuner og gjess",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="170",
    label="Minktisper",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="171",
    label="Revetisper",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="174",
    label="Ender, kalkuner og gjess for slakt",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="175",
    label="Livkyllinger",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="176",
    label="Slaktekyllinger",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="178",
    label="Hjort, 1 år og eldre",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="179",
    label="Hjort, under 1 år",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="180",
    label="Kaniner",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="181",
    label="Griser solgt som livdyr, vekt på minst 50 kg",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="183",
    label="Struts",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="185",
    label="Kyllinger og kalkuner solgt som livdyr",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="192",
    label="Esel",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="193",
    label="Hester i pensjon i beitesesongen",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="194",
    label="Bifolk",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="196",
    label="Lama",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="197",
    label="Alpakka",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="210",
    label="Fylldyrket eng",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="211",
    label="Overflatedyrket eng",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="212",
    label="Innmarksbeite",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="213",
    label="Andre grovforvekster til for",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="223",
    label="Grønngjødsling",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="230",
    label="Poteter",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="231",
    label="Annet korn og frø som er berettiget tilskudd",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="235",
    label="Engfør og annen såfrøproduksjon",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="236",
    label="Erter, bønner og andre belgvekster til modning",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="237",
    label="Oljevekster",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="238",
    label="Rug og rughvete",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="239",
    label="Korn til krossing",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="240",
    label="Vårhvete",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="242",
    label="Bygg",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="243",
    label="Havre",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="245",
    label="Erter og bønner til konserveindustri (høstet før modning)",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="247",
    label="Høsthvete",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="264",
    label="Grønnsaker på friland, inkl. matkålrot og urter",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="271",
    label="Moreller og kirsebær",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="280",
    label="Jordbær",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="282",
    label="Andre bærarter",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="283",
    label="Andre fruktarter",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="285",
    label="Planteskoleareal og blomsterdyrking på friland",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="290",
    label="Brakka areal",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="292",
    label="Fulldyrket og/eller overflatedyrket, ute av drift",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="293",
    label="Innmarksbeite, ute av drift",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="294",
    label="Areal i drift, men ikke berettiget produksjonstilskudd",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="410",
    label="Storfe på utmarksbeite - Melkekyr og ammekyr",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="411",
    label="Storfe på beite - Melkekyr og ammekyr",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="420",
    label="Storfe på utmarksbeite - Øvrige storfe",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="422",
    label="Storfe på beite - Øvrige storfe",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="431",
    label="Sauer, født i fjor eller tidligere, utmarksbeite",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="432",
    label="Lam, født i år, utmarksbeite",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="440",
    label="Geiter, voksne og kje, utmarksbeite",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="Geiter, voksne og kje, beitetilskudd",
    label="",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="450",
    label="Hester på utmarksbeite",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="455",
    label="Hester på beite",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="480",
    label="Lama på beite",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="481",
    label="Alpakka på beite",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="486",
    label="Hjort på beite",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="487",
    label="Sauer, født i fjor eller tidligere, beitetilskudd",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="488",
    label="Lam, født i år, beitetilskudd",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="521",
    label="Salg av høy",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="522",
    label="Salg av surfor",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="523",
    label="Salg av høyensilasje",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="720",
    label="Storfe på utmarksbeite - Kyr av bevaringsverdig rase",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="721",
    label="Storfe på utmarksbeite - Okser av bevaringsverdig rase",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="722",
    label="Søyer av bevaringsverdig rase",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="723",
    label="Værer av bevaringsverdig rase",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="724",
    label="Ammegeiter av bevaringsverdig rase",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="725",
    label="Unghester under 3 år av bevaringsverdig rase",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="801",
    label="Økologiske melkekyr",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="802",
    label="Økologiske ammekyr",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="803",
    label="Økologiske øvrige storfe",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="810",
    label="Økologiske melkegeiter",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="811",
    label="Økologiske ammegeiter",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="821",
    label="Økologiske sauer",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="830",
    label="Økologiske avlsgriser",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="833",
    label="Økologiske griser solgt som livdyr",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="841",
    label="Økologiske verpehøner",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="852",
    label="Grønngjødsling, 2. års karens",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="855",
    label="Korn til modning og krossing, økologisk samt 2.års karens",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="861",
    label="Poteter, økologisk areal samt 2.års karens",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="863",
    label="Frukt og bær, økologisk areal samt 2. og 3. års karens",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="864",
    label="Grønnsaker, økologisk areal samt 2. års karens",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="870",
    label="Annet areal (grovfôr), økologisk areal samt 2. års karens",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="871",
    label="Innmarksbeite, økologisk areal",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="875",
    label="Grønngjødsling, økologisk areal",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="876",
    label="Areal brakka for å bekjempe ugras, økologisk eller 2. års karens",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="880",
    label="Innmarksbeite i 1 års karens",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="881",
    label="Grovforareal i 1 års karens",
    description="",
    groups=[""],
    measured_in="",
)

Produksjonskode(
    code="882",
    label="Annet areal (enn grovfor) i 1 års karens",
    description="",
    groups=[""],
    measured_in="",
)


print(Produksjonstilskudd())

print(Produksjonstilskudd().categories)

print("get_codes testing")
print(1)
print(Produksjonstilskudd().get_codes())
print(2)
print(Produksjonstilskudd().get_codes("Frukt"))
print(3)
print(Produksjonstilskudd().get_codes("Frukt avling"))
